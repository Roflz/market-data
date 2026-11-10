"""
Get a video into a form Claude can read: still frames (images) and the transcript (captions).

  PYTHONPATH=./pylib python3 video_tool.py URL_OR_FILE [--every 10] [--out videos/<name>] [--no-video]

- URL (YouTube and most video sites): downloads the captions (manual if present, else automatic) as plain text,
  and the video at up to 720p, using yt-dlp.
- Local file: uses it as is.
- Frames: one image every --every seconds (default 10) into <out>/frames/, numbered with the time in the video,
  e.g. frame_00h05m30s.jpg, so a frame can be matched to what is said at that moment in transcript.txt.
- --no-video: transcript only (fast, small).
Output folder: videos/<video title or file name>/ with transcript.txt (timestamped), frames/ and info.txt.
Tools: yt-dlp and imageio-ffmpeg (bundled ffmpeg) in ./pylib.
"""
import argparse
import glob
import os
import re
import subprocess
import sys

import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def safe(name):
    return re.sub(r"[^\w\-. ]+", "_", name).strip()[:80] or "video"


def vtt_to_text(path):
    """Captions (.vtt) -> 'hh:mm:ss  text' lines, with the repeated rolling lines of auto-captions removed."""
    out, last = [], None
    t = "00:00:00"
    for line in open(path, encoding="utf-8", errors="ignore"):
        line = line.strip()
        m = re.match(r"(\d\d:\d\d:\d\d)\.\d+ -->", line)
        if m:
            t = m.group(1)
            continue
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")) or line.isdigit():
            continue
        text = re.sub(r"<[^>]+>", "", line).strip()
        if text and text != last:
            out.append(f"{t}  {text}")
            last = text
    return "\n".join(out)


def download(url, out_dir, video):
    import yt_dlp
    opts = {"outtmpl": os.path.join(out_dir, "video.%(ext)s"), "writesubtitles": True, "writeautomaticsub": True,
            "subtitleslangs": ["en.*", "en"], "subtitlesformat": "vtt", "quiet": True, "no_warnings": True,
            "format": "bv*[height<=720]+ba/b[height<=720]/b", "merge_output_format": "mp4",
            "ffmpeg_location": FFMPEG, "skip_download": not video}
    with yt_dlp.YoutubeDL(opts) as y:
        info = y.extract_info(url, download=True)
    with open(os.path.join(out_dir, "info.txt"), "w") as f:
        f.write(f"title: {info.get('title')}\nchannel: {info.get('uploader')}\nurl: {url}\n"
                f"duration_s: {info.get('duration')}\nupload_date: {info.get('upload_date')}\n\n{info.get('description') or ''}\n")
    subs = sorted(glob.glob(os.path.join(out_dir, "video*.vtt")))
    if subs:
        with open(os.path.join(out_dir, "transcript.txt"), "w") as f:
            f.write(vtt_to_text(subs[0]))
    vids = [p for p in glob.glob(os.path.join(out_dir, "video.*")) if not p.endswith((".vtt", ".txt"))]
    return info.get("title"), (vids[0] if vids else None), bool(subs)


def frames(video_path, out_dir, every):
    fdir = os.path.join(out_dir, "frames")
    os.makedirs(fdir, exist_ok=True)
    subprocess.run([FFMPEG, "-loglevel", "error", "-i", video_path, "-vf", f"fps=1/{every},scale='min(1280,iw)':-2",
                    "-q:v", "3", os.path.join(fdir, "tmp_%05d.jpg")], check=True)
    for p in sorted(glob.glob(os.path.join(fdir, "tmp_*.jpg"))):
        k = int(re.search(r"tmp_(\d+)", p).group(1)) - 1
        s = int(round(k * every))
        os.replace(p, os.path.join(fdir, f"frame_{s // 3600:02d}h{s % 3600 // 60:02d}m{s % 60:02d}s.jpg"))
    return len(os.listdir(fdir))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("source")
    ap.add_argument("--every", type=float, default=10.0, help="seconds between frames")
    ap.add_argument("--out", help="output folder (default videos/<title>)")
    ap.add_argument("--no-video", action="store_true", help="transcript only")
    a = ap.parse_args()
    is_url = re.match(r"https?://", a.source) is not None
    vid = re.search(r"(?:v=|youtu\.be/|/shorts/)([\w-]{6,})", a.source)
    name = safe(os.path.splitext(os.path.basename(a.source))[0]) if not is_url else "download_" + (vid.group(1) if vid else safe(a.source)[-20:])
    out = a.out or os.path.join("videos", name)
    os.makedirs(out, exist_ok=True)
    if is_url:
        title, vpath, has_subs = download(a.source, out, not a.no_video)
        if not a.out and title:
            new = os.path.join("videos", safe(title))
            if new != out and not os.path.exists(new):
                os.rename(out, new)
                out = new
                vpath = vpath and os.path.join(out, os.path.basename(vpath))
        print(f"{title}\n  transcript: {'yes' if has_subs else 'no captions available'}")
    else:
        vpath = a.source
    if vpath and not a.no_video:
        n = frames(vpath, out, a.every)
        print(f"  frames: {n} (one every {a.every:g} s)")
    print(f"  saved in {out}/")


if __name__ == "__main__":
    sys.exit(main())

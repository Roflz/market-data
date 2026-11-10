"""
Extract the distinct slides of a downloaded video and pair each with what is said while it is on screen.
  PYTHONPATH=./pylib python3 video_slides.py "videos/<title>" [--every 1] [--threshold 6]
1. One frame per --every seconds (ffmpeg, from video.mp4/webm in the folder).
2. A frame starts a new slide when it differs from the current slide's first frame by more than --threshold
   (mean absolute difference of 64x36 grayscale thumbnails, 0-255 scale). Gradual animations still produce a few
   slides; raise the threshold to merge them, lower it to split more.
3. slides/slide_NNN_<mm:ss>.jpg plus slides.html (each slide full width, with its transcript lines) and slides.md
   (the transcript per slide, for reading/notes).
"""
import argparse
import glob
import html
import os
import re
import shutil
import subprocess

import imageio_ffmpeg
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("folder")
ap.add_argument("--every", type=float, default=1.0)
ap.add_argument("--threshold", type=float, default=6.0)
a = ap.parse_args()
vids = [p for p in glob.glob(os.path.join(a.folder, "video.*")) if p.endswith((".mp4", ".webm", ".mkv"))]
assert vids, "no video file in the folder"
tmp = os.path.join(a.folder, "_all_frames")
shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", vids[0], "-vf", f"fps=1/{a.every}",
                "-q:v", "2", os.path.join(tmp, "f_%05d.jpg")], check=True)
frames = sorted(glob.glob(os.path.join(tmp, "f_*.jpg")))


def thumb(p):
    return np.asarray(Image.open(p).convert("L").resize((64, 36)), dtype=np.float32)


slides = []                                  # (start_seconds, frame_path)
ref = None
for i, p in enumerate(frames):
    t = thumb(p)
    if ref is None or np.abs(t - ref).mean() > a.threshold:
        slides.append((i * a.every, p)); ref = t
out = os.path.join(a.folder, "slides")
shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
# transcript lines "hh:mm:ss  text"
lines = []
for ln in open(os.path.join(a.folder, "transcript.txt"), encoding="utf-8"):
    m = re.match(r"(\d\d):(\d\d):(\d\d)\s+(.*)", ln.strip())
    if m:
        lines.append((int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]), m[4]))
dur = len(frames) * a.every
items = []
for k, (s, p) in enumerate(slides):
    e = slides[k + 1][0] if k + 1 < len(slides) else dur
    name = f"slide_{k + 1:03d}_{int(s) // 60:02d}m{int(s) % 60:02d}s.jpg"
    Image.open(p).save(os.path.join(out, name), quality=88)
    said = " ".join(t for ts, t in lines if s - 0.5 <= ts < e - 0.5)
    items.append((k + 1, s, e, name, said))
shutil.rmtree(tmp, ignore_errors=True)
title = os.path.basename(os.path.normpath(a.folder))
h = [f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)} - slides</title><style>"
     "body{font-family:system-ui,sans-serif;margin:16px;background:#fcfcfb;color:#0b0b0b;max-width:1300px}"
     "img{width:100%;border:1px solid #e1e0d9;margin:6px 0}p.t{color:#52514e;font-size:15px;margin:0 0 28px}"
     "h3{margin:22px 0 4px;font-size:15px}</style></head><body>",
     f"<h1>{html.escape(title)}</h1><p>{len(items)} distinct slides; under each, what is said while it is on screen.</p>"]
md = [f"# {title}: slides with transcript\n"]
for n, s, e, name, said in items:
    span = f"{int(s) // 60}:{int(s) % 60:02d}-{int(e) // 60}:{int(e) % 60:02d}"
    h.append(f"<h3>Slide {n} ({span})</h3><img src='slides/{name}'><p class='t'>{html.escape(said)}</p>")
    md.append(f"## Slide {n} ({span}) - slides/{name}\n{said}\n")
h.append("</body></html>")
open(os.path.join(a.folder, "slides.html"), "w").write("\n".join(h))
open(os.path.join(a.folder, "slides.md"), "w").write("\n".join(md))
print(f"{len(frames)} frames -> {len(items)} slides in {out}/; slides.html and slides.md written")

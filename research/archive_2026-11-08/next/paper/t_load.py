import time, resource, io, contextlib
import lit_p5_orb as p5, lit_p2_lasthalfhour as p2
t=time.time()
with contextlib.redirect_stdout(io.StringIO()):
    dates,g,inst=p5.load_market("NQ")
print("p5", time.time()-t, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6)
t=time.time(); log=[]
raw=p2.load_market("NQ",log)
print("p2", time.time()-t, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6)

from __future__ import print_function, division, absolute_import
from pylab import *
import time

import matplotlib.backends
import matplotlib.pyplot as p
import os.path


def is_backend_module(fname):
    """Identifies if a filename is a matplotlib backend module"""
    return fname.startswith('backend_') and fname.endswith('.py')

def backend_fname_formatter(fname): 
    """Removes the extension of the given filename, then takes away the leading 'backend_'."""
    return os.path.splitext(fname)[0][8:]

# get the directory where the backends live
backends_dir = os.path.dirname(matplotlib.backends.__file__)

# filter all files in that directory to identify all files which provide a backend
backend_fnames = filter(is_backend_module, os.listdir(backends_dir))

backends = [backend_fname_formatter(fname) for fname in backend_fnames]

print("supported backends: \t" + str(backends))

# validate backends
backends_valid = []
for b in backends:
    try:
        p.switch_backend(b)
        backends_valid += [b]
    except:
        continue

print("valid backends: \t" + str(backends_valid))


# try backends performance
for b in backends_valid:

    ion()
    try:
        p.switch_backend(b)


        clf()
        tstart = time.time()               # for profiling
        x = arange(0,2*pi,0.01)            # x-array
        line, = plot(x,sin(x))
        for i in arange(1,200):
            line.set_ydata(sin(x+i/10.0))  # update the data
            draw()                         # redraw the canvas

        print(b + ' FPS: \t' , 200/(time.time()-tstart))
        ioff()

    except:
        print(b + " error :(")

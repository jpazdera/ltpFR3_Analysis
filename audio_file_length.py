import wave
import contextlib
import numpy as np
from glob import glob

files = glob('/Users/jessepazdera/AtomProjects/ltpFR3_MTurk/static/audio/wordpool/*.wav')

duration = np.empty(len(files))
for i, fname in enumerate(files):
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration[i] = frames / float(rate)

pass

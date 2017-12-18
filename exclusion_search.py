import os
import json
import numpy as np
from glob import glob


# Find behavioral matrix files from all participants
datafiles = glob('/data/eeg/scalp/ltp/ltpFR3_MTurk/data/MTK*.json')

# Initialize data arrays
subj = np.empty(len(datafiles), dtype='U7')
math_total = np.empty(len(datafiles), dtype=int)
math_perc = np.empty(len(datafiles), dtype=float)
zrecs = np.empty(len(datafiles), dtype=float)
recs = np.empty(len(datafiles), dtype=float)

# Get math and recall info from each participant
for i, df in enumerate(datafiles):
    with open(df, 'r') as f:
        d = json.load(f)

    subj[i] = os.path.splitext(os.path.basename(df))[0]
    math_total[i] = np.array(d['math_correct'][2:]).sum()
    math_perc[i] = np.array(d['math_correct'][2:]).mean()
    zrecs[i] = (np.array(d['recalled'][2:]).sum(axis=1) == 0).sum()
    recs[i] = np.nansum(d['recalled'][2:])

# Exclude participants averaging fewer than 3 correct math problems per trial
low_math = subj[np.where(math_total < 48)]

# Exlcude participants with low math accuracy (in case they have a high math score from entering lots of random numbers)
low_acc = subj[np.where(((math_perc - np.nanmean(math_perc)) / np.nanstd(math_perc)) < -3)]

# Exclude participants who made 0 recalls on more than 1 trial
zrec_trial = subj[np.where(zrecs > 1)]

# Exclude participants who missed fewer than 1 word per list on average
high_rec = subj[np.where(recs > 272)]

# Get combined list of excluded participants
exclude = np.union1d(np.union1d(np.union1d(low_math, low_acc), zrec_trial), high_rec)

print 'Participants Marked for Exclusion: ', exclude
print 'Total Excluded: ', exclude.shape[0]
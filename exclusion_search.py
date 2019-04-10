import os
import json
import numpy as np
from glob import glob


V = 2

# Find behavioral matrix files from all participants
datafiles = glob('/data/eeg/scalp/ltp/ltpFR3_MTurk/data/MTK*.json') + \
            glob('/data/eeg/scalp/ltp/ltpFR3_MTurk/data/excluded/MTK*.json')

datafiles = [df for df in datafiles if (int(df[-9:-5]) < 1309 and V == 1) or (int(df[-9:-5]) >= 1309 and V == 2)]
# Initialize data arrays
subj = np.empty(len(datafiles), dtype='U7')
math_total = np.empty(len(datafiles), dtype=int)
math_perc = np.empty(len(datafiles), dtype=float)
zrecs = np.empty(len(datafiles), dtype=float)
recs = np.empty(len(datafiles), dtype=float)

# Get math and recall info from each participant
for i, df in enumerate(datafiles):
    snum = int(df[-9:-5])
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
low_acc = subj[np.where(((math_perc - np.nanmean(math_perc)) / np.nanstd(math_perc)) < -2)]

# Exclude participants who made 0 recalls on more than 1 trial
zrec_trial = subj[np.where(zrecs > 1)]

# Exclude participants who missed fewer than 1 word per list on average
high_rec = subj[np.where(recs > 272)]

# Get combined list of excluded participants
exclude = np.union1d(np.union1d(np.union1d(low_math, low_acc), zrec_trial), high_rec)

# Unique exclusion
wrote_notes = [x for x in np.loadtxt('/data/eeg/scalp/ltp/ltpFR3_MTurk/WROTE_NOTES.txt', dtype=str) if x in subj]
un_zt = len([x for x in zrec_trial if x not in np.union1d(np.union1d(np.union1d(wrote_notes, low_math), low_acc), high_rec)])
un_hr = len([x for x in high_rec if x not in np.union1d(np.union1d(np.union1d(wrote_notes, low_math), low_acc), zrec_trial)])
un_lm = len([x for x in low_math if x not in np.union1d(np.union1d(np.union1d(wrote_notes, high_rec), low_acc), zrec_trial)])
un_la = len([x for x in low_acc if x not in np.union1d(np.union1d(np.union1d(wrote_notes, high_rec), low_math), zrec_trial)])
un_wn = len([x for x in wrote_notes if x not in np.union1d(np.union1d(np.union1d(low_acc, high_rec), low_math), zrec_trial)])

print sorted(low_math)
print sorted(low_acc)
print sorted(zrec_trial)
print sorted(high_rec)
#print 'Participants Marked for Exclusion: ', exclude
print 'Total Excluded: ', exclude.shape[0]

for s in np.unique(low_math.tolist() + low_acc.tolist() + zrec_trial.tolist() + high_rec.tolist()):
    print str(s)



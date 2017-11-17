import os
import json
import numpy as np
import pyvttbl as pt
from glob import glob
from collections import namedtuple


stat_list = ['spc', 'crp_early', 'crp_late', 'pfr', 'psr', 'ptr', 'pli_recency', 'elis', 'plis', 'reps']
prs = ['s', 'f']
mods = ['a', 'v']
lls = ['12', '24']
condis = ['sa12', 'fa12', 'sv12', 'fv12', 'sa24', 'fa24', 'sv24', 'fv24']

s = {}
for stat_file in glob('/data/eeg/scalp/ltp/ltpFR3_MTurk/stats/*.json'):
    subj = os.path.splitext(os.path.basename(stat_file))[0]
    if subj != 'all':
        with open(stat_file, 'r') as f:
            s[subj] = json.load(f)

EXCLUDED = ['MTK0019', 'MTK0181']
for subj in EXCLUDED:
    del s[subj]


"""
# SPC (Aligned at Serial Position 1)
df = pt.DataFrame()
for subj in s:
    for c in condis:
        for pos, score in enumerate(s[subj]['spc'][c]):
            entry = dict(ID=subj, Pres_Rate=prs.index(c[0]), Modality=mods.index(c[1]), List_Length=lls.index(c[2:4]), Serial_Pos=pos+1, PRec=score)
            df.insert(entry)

print df.anova('PRec', sub='ID', wfactors=['Pres_Rate', 'Modality', 'List_Length', 'Serial_Pos'])
"""
# Forward asymmetry early
df = pt.DataFrame()
for subj in s:
    skip_subj = False
    for c in condis:  # Exclude people that don't have a response probability for all both lag +1 and -1
        if np.sum(np.isnan(s[subj]['crp_early'][c][2:5])) > 1:
            skip_subj = True
    if skip_subj:
        continue
    for c in condis:
        score = s[subj]['crp_early'][c][4] - s[subj]['crp_early'][c][2]
        entry = dict(ID=subj, Pres_Rate=prs.index(c[0]), Modality=mods.index(c[1]), List_Length=lls.index(c[2:4]), CRP_Asym_Early=score)
        df.insert(entry)
print df.anova('CRP_Asym_Early', sub='ID', wfactors=['Pres_Rate', 'Modality', 'List_Length'])


# Forward asymmetry late
df = pt.DataFrame()
for subj in s:
    skip_subj = False
    for c in condis:  # Exclude people that don't have a response probability for all both lag +1 and -1
        if np.sum(np.isnan(s[subj]['crp_late'][c][2:5])) > 1:
            skip_subj = True
    if skip_subj:
        continue
    for c in condis:
        score = s[subj]['crp_late'][c][4] - s[subj]['crp_late'][c][2]
        entry = dict(ID=subj, Pres_Rate=prs.index(c[0]), Modality=mods.index(c[1]), List_Length=lls.index(c[2:4]), CRP_Asym_Late=score)
        df.insert(entry)
print df.anova('CRP_Asym_Late', sub='ID', wfactors=['Pres_Rate', 'Modality', 'List_Length'])


# Temporal Clustering Factor
df = pt.DataFrame()
for subj in s:
    for c in condis:
        entry = dict(ID=subj, Pres_Rate=prs.index(c[0]), Modality=mods.index(c[1]), List_Length=lls.index(c[2:4]), TempFact=s[subj]['temp_fact'][c])
        df.insert(entry)

print df.anova('TempFact', sub='ID', wfactors=['Pres_Rate', 'Modality', 'List_Length'])


"""
# lag CRP Early
df = pt.DataFrame()
for subj in s:
    skip_subj = False
    for c in condis:  # Exclude people that don't have a response probability for all 6 lags
        if np.sum(np.isnan(s[subj]['crp_early'][c])) > 1:
            skip_subj = True
    if skip_subj:
        continue
    for c in condis:
        for lag, score in enumerate(s[subj]['crp_early'][c]):
            if not np.isnan(score):
                entry = dict(ID=subj, Pres_Rate=prs.index(c[0]), Modality=mods.index(c[1]), List_Length=lls.index(c[2:4]), Lag=lag-3, CRP_Early=score)
                df.insert(entry)

print df.anova('CRP_Early', sub='ID', wfactors=['Pres_Rate', 'Modality', 'List_Length', 'Lag'])


# lag CRP Late
df = pt.DataFrame()
for subj in s:
    skip_subj = False
    for c in condis:  # Exclude people that don't have a response probability for all 6 lags
        if np.sum(np.isnan(s[subj]['crp_late'][c])) > 1:
            skip_subj = True
    if skip_subj:
        continue
    for c in condis:
        for lag, score in enumerate(s[subj]['crp_late'][c]):
            if not np.isnan(score):
                entry = dict(ID=subj, Pres_Rate=prs.index(c[0]), Modality=mods.index(c[1]), List_Length=lls.index(c[2:4]), Lag=lag-3, CRP_Late=score)
                df.insert(entry)

print df.anova('CRP_Late', sub='ID', wfactors=['Pres_Rate', 'Modality', 'List_Length', 'Lag'])
"""


# PLI Recency
df = pt.DataFrame()
for subj in s:
    skip_subj = False
    for c in condis:  # Exclude people that didn't make any PLIs
        if np.any(np.isnan(s[subj]['pli_recency'][c])):
            skip_subj = True
    if skip_subj:
        continue
    for c in condis:
        for n, score in enumerate(s[subj]['pli_recency'][c]):
            if not np.isnan(score):
                entry = dict(ID=subj, Pres_Rate=prs.index(c[0]), Modality=mods.index(c[1]), List_Length=lls.index(c[2:4]), Lag=n+1, Rate=score)
                df.insert(entry)

print df.anova('Rate', sub='ID', wfactors=['Pres_Rate', 'Modality', 'List_Length', 'Lag'])


# PLI
SubjData = namedtuple('SubjData', ['ID', 'Pres_Rate', 'Modality', 'List_Length', 'PLI'])
df = pt.DataFrame()
for subj in s:
    for c in condis:
        df.insert(SubjData(subj, prs.index(c[0]), mods.index(c[1]), lls.index(c[2:]), s[subj]['plis'][c])._asdict())

print df.anova('PLI', sub='ID', wfactors=['Pres_Rate', 'Modality', 'List_Length'])


# ELI
SubjData = namedtuple('SubjData', ['ID', 'Pres_Rate', 'Modality', 'List_Length', 'ELI'])
df = pt.DataFrame()
for subj in s:
    for c in condis:
        df.insert(SubjData(subj, prs.index(c[0]), mods.index(c[1]), lls.index(c[2:]), s[subj]['elis'][c])._asdict())

print df.anova('ELI', sub='ID', wfactors=['Pres_Rate', 'Modality', 'List_Length'])


# Repetitions
SubjData = namedtuple('SubjData', ['ID', 'Pres_Rate', 'Modality', 'List_Length', 'Rep'])
df = pt.DataFrame()
for subj in s:
    for c in condis:
        df.insert(SubjData(subj, prs.index(c[0]), mods.index(c[1]), lls.index(c[2:]), s[subj]['reps'][c])._asdict())

print df.anova('Rep', sub='ID', wfactors=['Pres_Rate', 'Modality', 'List_Length'])






"""
scores = {}
for stat in stat_list:
    scores[stat] = {}
    for c in condis:
        scores[stat][c] = []
        for subj in s:
            scores[stat][c].append(s[subj][stat][c])
"""
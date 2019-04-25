import numpy as np
import pandas as pd
from glob import glob


def get_completed_subjects():
    subj_list = glob('/data/eeg/scalp/ltp/ltpFR3_MTurk/events/MTK*.json') + \
                glob('/data/eeg/scalp/ltp/ltpFR3_MTurk/events/excluded/MTK*.json') + \
                glob('/data/eeg/scalp/ltp/ltpFR3_MTurk/events/bad_sess/MTK*.json') + \
                glob('/data/eeg/scalp/ltp/ltpFR3_MTurk/events/rejected/MTK*.json')
    subj_list = np.sort([f[-12:-5] for f in subj_list])
    return subj_list


def get_accepted_subjects():
    subj_list = glob('/data/eeg/scalp/ltp/ltpFR3_MTurk/events/MTK*.json') + \
                glob('/data/eeg/scalp/ltp/ltpFR3_MTurk/events/excluded/MTK*.json') + \
                glob('/data/eeg/scalp/ltp/ltpFR3_MTurk/events/bad_sess/MTK*.json')
    subj_list = np.sort([f[-12:-5] for f in subj_list])
    return subj_list


if __name__ == "__main__":

    # Load subject database and subject lists
    subjdb = pd.read_csv('ltpFR3.csv')
    comp_subj = get_completed_subjects()
    acc_subj = get_accepted_subjects()

    # Mark subjects in database as to whether they were complete and accepted
    completed_mask = np.in1d(subjdb['workerid'], comp_subj)
    accepted_mask = np.in1d(subjdb['workerid'], acc_subj)
    subjdb['completed'] = completed_mask.astype(int)
    subjdb['accepted'] = accepted_mask.astype(int)

    # Save updated database
    subjdb.to_csv('ltpFR3.csv', index=False)

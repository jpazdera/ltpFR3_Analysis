import os
import json
import numpy as np
import matplotlib.pyplot as plt
from glob import glob


class FFRAnalyzer:
    def __init__(self):
        # Set experiment parameters
        self.EVENT_DIR = '/data/eeg/scalp/ltp/ltpFR3_MTurk/events/'
        self.DATA_DIR = '/data/eeg/scalp/ltp/ltpFR3_MTurk/data/'
        self.EXCLUDED = np.loadtxt('/data/eeg/scalp/ltp/ltpFR3_MTurk/EXCLUDED.txt', dtype='U8')
        self.FFR_DUR = 300000
        self.REC_DUR = 60000
        self.TRIALS = 18
        self.MAX_LL = 24

        # Load all event data into a subject dictionary
        self.e = {}
        ev_files = glob(os.path.join(self.EVENT_DIR, '*.json'))
        for ef in ev_files:
            subj = os.path.splitext(os.path.basename(ef))[0]
            if subj in self.EXCLUDED:
                continue
            with open(ef, 'r') as f:
                self.e[subj] = [ev['trialdata'] for ev in json.load(f)['data']]

        # Load all behavioral matrices into a subject dictionary
        self.d = {}
        data_files = glob(os.path.join(self.DATA_DIR, '*.json'))
        for df in data_files:
            subj = os.path.splitext(os.path.basename(df))[0]
            if subj in self.EXCLUDED:
                continue
            with open(df, 'r') as f:
                self.d[subj] = json.load(f)

    def find_FFR_endtime(self, subj):
        for ev in self.e[subj]:
            if 'type' in ev and ev['type'] == 'FFR':
                return ev['time_elapsed']
        raise Exception('No FFR period found for %s' % subj)

    def get_pres_times(self, subj):
        pres_times = np.array((self.TRIALS, self.MAX_LL))
        for ev in self.e[subj]:
            if 'type' in ev and 'PRES_' in ev['type']:
                pres_times[ev['trial'], ev['serialpos']] = ev['time_elapsed']
        return pres_times

    def find_pres_time(self, subj, word):
        for ev in self.e[subj]:
            if 'type' in ev and 'PRES_' in ev['type'] and ev['word'] == word:
                return ev['time_elapsed']
        raise Exception('Presentation event not found for %s word %s' % (subj, word))

    def find_last_rectime(self, subj, trial, pos):
        for ev in self.e[subj]:
            if 'type' in ev and ev['type'] == 'FREE_RECALL' and ev['trial'] == trial:
                return ev['time_elapsed'] - (self.REC_DUR - ev['rt'][pos])
        raise Exception('No free recall period found for %s trial %d' % (subj, trial))

    def run(self):
        all_ffr_recalled = []
        all_delays = []
        for subj in self.d:
            print subj
            # Get the time at which FFR ended (relative to the start of the study); skip if no FFR is detected
            try:
                ffr_endtime = self.find_FFR_endtime(subj)
            except Exception as e:
                print e
                continue
            # Get all presented words as an array in serial order
            pres_words = np.array(self.d[subj]['pres_words'])
            pres_words = pres_words[pres_words != '0']
            # Get an array of 0s and 1s indicating whether each presented word was recalled during FFR
            ffr_recalled = np.array(self.d[subj]['ffr_recalled'], dtype=bool)
            ffr_recalled = ffr_recalled[np.logical_not(np.isnan(ffr_recalled))]
            # Initialize an array to hold the time delays between presentation/last recall and the FFR period
            delays = np.empty_like(pres_words, dtype=int)
            delays.fill(np.nan)
            # Get array of all recalled words
            recwords = np.array(self.d[subj]['rec_words'])
            recalled = np.zeros_like(pres_words, dtype=bool)
            for i, word in enumerate(pres_words):
                when_recalled = np.where(recwords == word)
                if len(when_recalled[0]) > 0:
                    last_trial_recalled = when_recalled[0][-1]
                    last_pos_recalled = when_recalled[1][-1]
                    last_time_seen = self.find_last_rectime(subj, last_trial_recalled, last_pos_recalled)
                    recalled[i] = True
                else:
                    last_time_seen = self.find_pres_time(subj, word)
                    recalled[i] = False
                delays[i] = ffr_endtime - last_time_seen
            all_ffr_recalled.append(ffr_recalled)
            all_delays.append(delays)

        all_ffr_recalled = np.array(all_ffr_recalled).flatten()
        all_delays = np.array(all_delays).flatten()
        all_delays_pr = all_delays[recalled]
        all_delays_npr = all_delays[np.logical_not(recalled)]
        all_ffr_recalled_pr = all_ffr_recalled[recalled]
        all_ffr_recalled_npr = all_ffr_recalled[np.logical_not(recalled)]

        _, bins = np.histogram(all_delays, bins=15)
        all_delays_pr = np.searchsorted(bins, all_delays_pr)
        all_delays_npr = np.searchsorted(bins, all_delays_npr)
        bin_precs_pr = np.empty(len(bins))
        bin_precs_pr.fill(np.nan)
        bin_precs_npr = np.empty(len(bins))
        bin_precs_npr.fill(np.nan)
        for i in range(len(bins)):
            bin_precs_pr[i] = np.nanmean(all_ffr_recalled_pr[all_delays_pr == i])
            bin_precs_npr[i] = np.nanmean(all_ffr_recalled_npr[all_delays_npr == i])

        plt.plot(bin_precs_pr)
        plt.plot(bin_precs_npr)
        pass


if __name__ == "__main__":
    ana = FFRAnalyzer()
    ana.run()

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
        self.NUM_CONDITIONS = 4

        # Initialize fields that may be used across different methods
        self.all_recalled = None
        self.all_delays = None
        self.all_ffr_recalled = None
        self.all_condis = None
        self.bins = None
        self.bin_medians = None
        self.bin_precs = None

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

    def find_pres_info(self, subj, word):
        for ev in self.e[subj]:
            if 'type' in ev and 'PRES_' in ev['type'] and ev['word'] == word:
                return ev['time_elapsed'], ev['conditions']
        raise Exception('Presentation event not found for %s word %s' % (subj, word))

    def find_last_rectime(self, subj, trial, pos):
        for ev in self.e[subj]:
            if 'type' in ev and ev['type'] == 'FREE_RECALL' and ev['trial'] == trial:
                return ev['time_elapsed'] - (self.REC_DUR - ev['rt'][pos])
        raise Exception('No free recall period found for %s trial %d' % (subj, trial))

    def process_data(self):
        all_ffr_recalled = []
        all_delays = []
        all_recalled = []
        all_condis = []
        for subj in self.d:
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
            ffr_recalled = np.array(self.d[subj]['ffr_recalled'])
            ffr_recalled = ffr_recalled[np.logical_not(np.isnan(ffr_recalled))].astype(bool)
            # Initialize an array to hold the time delays between presentation/last recall and the FFR period
            delays = np.empty_like(pres_words, dtype=int)
            delays.fill(np.nan)
            # Get array of all recalled words
            recwords = np.array(self.d[subj]['rec_words'])
            recalled = np.zeros_like(pres_words, dtype=bool)
            condis = np.empty((len(pres_words), self.NUM_CONDITIONS), dtype='U8')
            # Determine whether each word was recalled prior to FFR, as well as the last time each word was seen
            for i, word in enumerate(pres_words):
                when_recalled = np.where(recwords == word)
                # If word was recalled prior to FFR, last time seen is last time recalled
                if len(when_recalled[0]) > 0:
                    last_trial_recalled = when_recalled[0][-1]
                    last_pos_recalled = when_recalled[1][-1]
                    last_time_seen = self.find_last_rectime(subj, last_trial_recalled, last_pos_recalled)
                    _, condis[i] = self.find_pres_info(subj, word)
                    recalled[i] = True
                # If word was never recalled until FFR, last time seen is during presentation
                else:
                    last_time_seen, condis[i] = self.find_pres_info(subj, word)
                    recalled[i] = False
                # Calculate delay between last time seen and the end of FFR
                delays[i] = ffr_endtime - last_time_seen
            # Add current participant's list of time delays and whether each word was recalled prior to FFR to a matrix
            all_ffr_recalled.append(ffr_recalled)
            all_delays.append(delays)
            all_recalled.append(recalled)
            all_condis.append(condis)

        # Array indicates each presented word was recalled prior to FFR
        self.all_recalled = np.array(all_recalled).flatten()
        # Array indicates whether each presented word was recalled during FFR
        self.all_ffr_recalled = np.array(all_ffr_recalled).flatten()
        # Array indicates the delay in milliseconds between when the word was last recalled/presented and the end of FFR
        self.all_delays = np.array(all_delays).flatten()
        # Array indicates the presentation conditions of each word
        self.all_condis = np.array(all_condis).reshape((len(all_recalled), self.NUM_CONDITIONS))

    def bin_recalls(self):
        # Group delays into time bins and replace the numbers in the delay arrays with their corresponding bin numbers
        # Each bin contains 1% of delay times
        self.bins = np.array([np.percentile(self.all_delays, i) for i in range(1, 100)])
        self.bin_medians = np.array([np.percentile(self.all_delays, i + .5) for i in range(1, 100)])
        self.all_delays = np.searchsorted(self.bins, self.all_delays)

        # For each bin, use all_ffr_recalled_(n)pr to calculate the overall probability of recall in each time bin
        self.bin_precs = np.empty(len(self.bins))
        self.bin_precs.fill(np.nan)
        for i in range(len(self.bins)):
            self.bin_precs[i] = np.nanmean(self.all_ffr_recalled[self.all_delays == i])

    def plot(self):
        # Plot probability of FFR recall for each time bin for previously recalled versus previously non-recalled words
        plt.plot(self.bin_medians / 60000., self.bin_precs)
        plt.title('Probability of Recall During FFR')
        plt.xlabel('Delay (Minutes)')
        plt.ylabel('Probability of Final Recall')


if __name__ == "__main__":
    ana = FFRAnalyzer()
    ana.process_data()
    ana.bin_recalls()
    ana.plot()
    plt.show()

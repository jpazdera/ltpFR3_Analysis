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
        self.binned_delays = None
        self.bin_precs = None
        self.e = {}
        self.d = {}


    def load_event_data(self):
        # Load all event data into a subject dictionary
        ev_files = glob(os.path.join(self.EVENT_DIR, '*.json'))
        for ef in ev_files:
            subj = os.path.splitext(os.path.basename(ef))[0]
            if subj in self.EXCLUDED:
                continue
            with open(ef, 'r') as f:
                self.e[subj] = [ev['trialdata'] for ev in json.load(f)['data']]
        # Load all behavioral matrices into a subject dictionary
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

    def get_pres_info(self, subj):
        pres_times = []
        condis = []
        for ev in self.e[subj]:
            if 'type' in ev and 'PRES_' in ev['type']:
                pres_times.append(ev['time_elapsed'])
                condis.append(ev['conditions'])
        return np.array(pres_times, dtype=int), np.array(condis, dtype='U8')

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
            ffr_recalled = np.array(self.d[subj]['ffr_recalled'])
            ffr_recalled = ffr_recalled[np.logical_not(np.isnan(ffr_recalled))].astype(bool)
            # Initialize an array to hold the time delays between presentation/last recall and the FFR period
            delays = np.empty_like(pres_words, dtype=int)
            delays.fill(np.nan)
            # Get array of all recalled words
            recwords = np.array(self.d[subj]['rec_words'])
            recalled = np.zeros_like(pres_words, dtype=bool)
            pres_times, condis = self.get_pres_info(subj)
            # Determine whether each word was recalled prior to FFR, as well as the last time each word was seen
            for i, word in enumerate(pres_words):
                when_recalled = np.where(recwords == word)
                # If word was recalled prior to FFR, last time seen is last time recalled
                if len(when_recalled[0]) > 0:
                    last_trial_recalled = when_recalled[0][-1]
                    last_pos_recalled = when_recalled[1][-1]
                    last_time_seen = self.find_last_rectime(subj, last_trial_recalled, last_pos_recalled)
                    recalled[i] = True
                # If word was never recalled until FFR, last time seen is during presentation
                else:
                    last_time_seen = pres_times[i]
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
        self.all_condis = np.array(all_condis)
        self.all_condis = self.all_condis.reshape((self.all_condis.shape[0]*self.all_condis.shape[1], self.all_condis.shape[2]))
        with open('ffr.json', 'w') as f:
            data = {'recalled': self.all_recalled.tolist(), 'ffr_recalled': self.all_ffr_recalled.tolist(), 'delays': self.all_delays.tolist(), 'condis': self.all_condis.tolist()}
            json.dump(data, f)

    def load_data(self):
        if os.path.exists('ffr.json'):
            with open('ffr.json', 'r') as f:
                data = json.load(f)
                try:
                    self.all_recalled = np.array(data['recalled'])
                    self.all_ffr_recalled = np.array(data['ffr_recalled'])
                    self.all_delays = np.array(data['delays'])
                    self.all_condis = np.array(data['condis'])
                except KeyError:
                    print 'Unable to load all expected data from ffr.json file!'
                else:
                    return True
        else:
            print 'Cannot load data -- ffr.json not found!'
        return False

    def bin_delays(self, perc_per_bin=1):
        # Group delays into time bins and replace the numbers in the delay arrays with their corresponding bin numbers
        # Each bin contains 1% of delay times
        self.bins = np.array([np.percentile(self.all_delays, i) for i in range(perc_per_bin, 101, perc_per_bin)])
        self.bin_medians = np.array([np.percentile(self.all_delays, i - perc_per_bin / 2.) for i in range(perc_per_bin, 101, perc_per_bin)])
        self.binned_delays = np.searchsorted(self.bins, self.all_delays)

    def filter_by_cond(self, recalled=None, ll=None, pr=None, mod=None, dd=None):
        ind = [i for i in range(len(self.all_condis)) if
               (recalled is None or self.all_recalled[i] == recalled) and
               (ll is None or int(self.all_condis[i][0]) == ll) and
               (pr is None or int(self.all_condis[i][1]) == pr) and
               (mod is None or self.all_condis[i][2] == mod) and
               (dd is None or int(self.all_condis[i][3]) == dd)]
        return self.all_ffr_recalled[ind], self.binned_delays[ind]

    def get_precs(self):
        self.bin_precs = {}
        filters = {
                    'rec': {'recalled': True}, 'nrec': {'recalled': False},
                    'sa12_rec': {'recalled': True, 'll': 12, 'pr': 1600, 'mod': 'a'},
                    'sa24_rec': {'recalled': True, 'll': 24, 'pr': 1600, 'mod': 'a'},
                    'sv12_rec': {'recalled': True, 'll': 12, 'pr': 1600, 'mod': 'v'},
                    'sv24_rec': {'recalled': True, 'll': 24, 'pr': 1600, 'mod': 'v'},
                    'fa12_rec': {'recalled': True, 'll': 12, 'pr': 800, 'mod': 'a'},
                    'fa24_rec': {'recalled': True, 'll': 24, 'pr': 800, 'mod': 'a'},
                    'fv12_rec': {'recalled': True, 'll': 12, 'pr': 800, 'mod': 'v'},
                    'fv24_rec': {'recalled': True, 'll': 24, 'pr': 800, 'mod': 'v'},
                    'sa12_nrec': {'recalled': False, 'll': 12, 'pr': 1600, 'mod': 'a'},
                    'sa24_nrec': {'recalled': False, 'll': 24, 'pr': 1600, 'mod': 'a'},
                    'sv12_nrec': {'recalled': False, 'll': 12, 'pr': 1600, 'mod': 'v'},
                    'sv24_nrec': {'recalled': False, 'll': 24, 'pr': 1600, 'mod': 'v'},
                    'fa12_nrec': {'recalled': False, 'll': 12, 'pr': 800, 'mod': 'a'},
                    'fa24_nrec': {'recalled': False, 'll': 24, 'pr': 800, 'mod': 'a'},
                    'fv12_nrec': {'recalled': False, 'll': 12, 'pr': 800, 'mod': 'v'},
                    'fv24_nrec': {'recalled': False, 'll': 24, 'pr': 800, 'mod': 'v'}
                   }
        for filt in filters:
            filtered_rec, filtered_del = self.filter_by_cond(**filters[filt])
            self.bin_precs[filt] = np.empty(len(self.bins))
            self.bin_precs[filt].fill(np.nan)
            for i in range(len(self.bins)):
                self.bin_precs[filt][i] = np.nanmean(filtered_rec[filtered_del == i])

    def plot(self):
        # Plot probability of FFR recall for each time bin for previously recalled versus previously non-recalled words
        plt.plot(self.bin_medians / 60000., (self.bin_precs['sv12_rec'] + self.bin_precs['sv24_rec']) / 2., 'ko-', label='Slow/Vis/Rec')
        plt.plot(self.bin_medians / 60000., (self.bin_precs['fv12_rec'] + self.bin_precs['fv24_rec']) / 2., 'k^-', label='Fast/Vis/Rec')
        plt.plot(self.bin_medians / 60000., (self.bin_precs['sa12_rec'] + self.bin_precs['sa24_rec']) / 2., 'ko--', markerfacecolor='white', label='Slow/Aud/Rec')
        plt.plot(self.bin_medians / 60000., (self.bin_precs['fa12_rec'] + self.bin_precs['fa24_rec']) / 2., 'k^--', markerfacecolor='white', label='Fast/Aud/Rec')

        plt.plot(self.bin_medians / 60000., (self.bin_precs['sv12_nrec'] + self.bin_precs['sv24_nrec']) / 2., 'ro-', label='Slow/Vis/NRec')
        plt.plot(self.bin_medians / 60000., (self.bin_precs['fv12_nrec'] + self.bin_precs['fv24_nrec']) / 2., 'r^-', label='Fast/Vis/NRec')
        plt.plot(self.bin_medians / 60000., (self.bin_precs['sa12_nrec'] + self.bin_precs['sa24_nrec']) / 2., 'ro--', markerfacecolor='white', label='Slow/Aud/NRec')
        plt.plot(self.bin_medians / 60000., (self.bin_precs['fa12_nrec'] + self.bin_precs['fa24_nrec']) / 2., 'r^--', markerfacecolor='white', label='Fast/Aud/NRec')

        plt.title('Probability of Recall During FFR')
        plt.xlabel('Delay (Minutes)')
        plt.ylabel('Probability of Final Recall')
        plt.legend()


if __name__ == "__main__":
    ana = FFRAnalyzer()
    if not ana.load_data():
        ana.load_event_data()
        ana.process_data()
    ana.bin_delays(4)
    ana.get_precs()
    ana.plot()

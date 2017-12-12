import os
import json
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from FFR import FFRAnalyzer


def fig2_spc(m, s):
    m = m['spc']
    s = s['spc']

    # SPCs for fast presentation
    ax = plt.subplot(121)
    ax.plot(range(1, 13), m['fv12'], 'b-')
    ax.fill_between(range(1, 13), np.add(m['fv12'], s['fv12']), np.subtract(m['fv12'], s['fv12']), color='b', alpha=.4)
    ax.plot(range(1, 13), m['fa12'], 'r-')
    ax.fill_between(range(1, 13), np.add(m['fa12'], s['fa12']), np.subtract(m['fa12'], s['fa12']), color='r', alpha=.4)
    ax.plot(range(1, 25), m['fv24'], 'b-')
    ax.fill_between(range(1, 25), np.add(m['fv24'], s['fv24']), np.subtract(m['fv24'], s['fv24']), color='b', alpha=.4)
    ax.plot(range(1, 25), m['fa24'], 'r-')
    ax.fill_between(range(1, 25), np.add(m['fa24'], s['fa24']), np.subtract(m['fa24'], s['fa24']), color='r', alpha=.4)
    ax.set_title('Fast Presentation')
    ax.set_xlabel('Serial Position')
    ax.set_ylabel('Recall Probability')
    ax.legend(labels=['Visual', 'Auditory'])
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # SPCs for slow presentation
    ax = plt.subplot(122)
    ax.plot(range(1, 13), m['sv12'], 'b-')
    ax.fill_between(range(1, 13), np.add(m['sv12'], s['sv12']), np.subtract(m['sv12'], s['sv12']), color='b', alpha=.4)
    ax.plot(range(1, 13), m['sa12'], 'r-')
    ax.fill_between(range(1, 13), np.add(m['sa12'], s['sa12']), np.subtract(m['sa12'], s['sa12']), color='r', alpha=.4)
    ax.plot(range(1, 25), m['sv24'], 'b-')
    ax.fill_between(range(1, 25), np.add(m['sv24'], s['sv24']), np.subtract(m['sv24'], s['sv24']), color='b', alpha=.4)
    ax.plot(range(1, 25), m['sa24'], 'r-')
    ax.fill_between(range(1, 25), np.add(m['sa24'], s['sa24']), np.subtract(m['sa24'], s['sa24']), color='r', alpha=.4)
    ax.set_title('Slow Presentation')
    ax.set_xlabel('Serial Position')
    ax.set_ylabel('Recall Probability')
    ax.legend(labels=['Visual', 'Auditory'])
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    plt.show()


def fig3_pfr(m, s):
    m = m['pfr']
    s = s['pfr']

    # PFR curves for fast presentation
    ax = plt.subplot(121)
    ax.plot(range(1, 13), m['fv12'], 'b-')
    ax.fill_between(range(1, 13), np.add(m['fv12'], s['fv12']), np.subtract(m['fv12'], s['fv12']), color='b', alpha=.4)
    ax.plot(range(1, 13), m['fa12'], 'r-')
    ax.fill_between(range(1, 13), np.add(m['fa12'], s['fa12']), np.subtract(m['fa12'], s['fa12']), color='r', alpha=.4)
    ax.plot(range(1, 25), m['fv24'], 'b-')
    ax.fill_between(range(1, 25), np.add(m['fv24'], s['fv24']), np.subtract(m['fv24'], s['fv24']), color='b', alpha=.4)
    ax.plot(range(1, 25), m['fa24'], 'r-')
    ax.fill_between(range(1, 25), np.add(m['fa24'], s['fa24']), np.subtract(m['fa24'], s['fa24']), color='r', alpha=.4)
    ax.set_title('Fast Presentation')
    ax.set_xlabel('Serial Position')
    ax.set_ylabel('Probability of First Recall')
    ax.legend(labels=['Visual', 'Auditory'])
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # PFR curves for slow presentation
    ax = plt.subplot(122)
    ax.plot(range(1, 13), m['sv12'], 'b-')
    ax.fill_between(range(1, 13), np.add(m['sv12'], s['sv12']), np.subtract(m['sv12'], s['sv12']), color='b', alpha=.4)
    ax.plot(range(1, 13), m['sa12'], 'r-')
    ax.fill_between(range(1, 13), np.add(m['sa12'], s['sa12']), np.subtract(m['sa12'], s['sa12']), color='r', alpha=.4)
    ax.plot(range(1, 25), m['sv24'], 'b-')
    ax.fill_between(range(1, 25), np.add(m['sv24'], s['sv24']), np.subtract(m['sv24'], s['sv24']), color='b', alpha=.4)
    ax.plot(range(1, 25), m['sa24'], 'r-')
    ax.fill_between(range(1, 25), np.add(m['sa24'], s['sa24']), np.subtract(m['sa24'], s['sa24']), color='r', alpha=.4)
    ax.set_title('Slow Presentation')
    ax.set_xlabel('Serial Position')
    ax.set_ylabel('Probability of First Recall')
    ax.legend(labels=['Visual', 'Auditory'])
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    plt.show()


def fig4_crp(m, s):
    m = m['crp_late']
    s = s['crp_late']
    for filt in s:
        s[filt][int(len(s[filt])/2)] = np.nan

    crp_range = range(-4, 5)

    # PFR curves for short list/fast presentation
    ax = plt.subplot(221)
    ax.plot(crp_range, m['fv12'], 'b-')
    ax.fill_between(crp_range, np.add(m['fv12'], s['fv12']), np.subtract(m['fv12'], s['fv12']), color='b', alpha=.4)
    ax.plot(crp_range, m['fa12'], 'r-')
    ax.fill_between(crp_range, np.add(m['fa12'], s['fa12']), np.subtract(m['fa12'], s['fa12']), color='r', alpha=.4)
    ax.legend(labels=['Visual', 'Auditory'])
    ax.set_ylim(0, .45)
    ax.set_xticks(crp_range)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_title('Fast')
    ax.set_ylabel('Cond. Resp. Prob.')

    # PFR curves for short list/slow presentation
    ax = plt.subplot(222)
    ax.plot(crp_range, m['sv12'], 'b-')
    ax.fill_between(crp_range, np.add(m['sv12'], s['sv12']), np.subtract(m['sv12'], s['sv12']), color='b', alpha=.4)
    ax.plot(crp_range, m['sa12'], 'r-')
    ax.fill_between(crp_range, np.add(m['sa12'], s['sa12']), np.subtract(m['sa12'], s['sa12']), color='r', alpha=.4)
    ax.legend(labels=['Visual', 'Auditory'])
    ax.set_ylim(0, .45)
    ax.set_xticks(crp_range)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_title('Slow')

    # PFR curves for long list/fast presentation
    ax = plt.subplot(223)
    ax.plot(crp_range, m['fv24'], 'b-')
    ax.fill_between(crp_range, np.add(m['fv24'], s['fv24']), np.subtract(m['fv24'], s['fv24']), color='b', alpha=.4)
    ax.plot(crp_range, m['fa24'], 'r-')
    ax.fill_between(crp_range, np.add(m['fa24'], s['fa24']), np.subtract(m['fa24'], s['fa24']), color='r', alpha=.4)
    ax.legend(labels=['Visual', 'Auditory'])
    ax.set_ylim(0, .45)
    ax.set_xticks(crp_range)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_ylabel('Cond. Resp. Prob.')
    ax.set_xlabel('Lag')

    # PFR curves for long list/slow presentation
    ax = plt.subplot(224)
    ax.plot(crp_range, m['sv24'], 'b-')
    ax.fill_between(crp_range, np.add(m['sv24'], s['sv24']), np.subtract(m['sv24'], s['sv24']), color='b', alpha=.4)
    ax.plot(crp_range, m['sa24'], 'r-')
    ax.fill_between(crp_range, np.add(m['sa24'], s['sa24']), np.subtract(m['sa24'], s['sa24']), color='r', alpha=.4)
    ax.legend(labels=['Visual', 'Auditory'])
    ax.set_ylim(0, .45)
    ax.set_xticks(crp_range)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xlabel('Lag')

    plt.show()


def fig5_pli(m, s):
    pass


def fig6_irt(m, s):
    pass


def fig7_ffr():
    ffr = FFRAnalyzer()
    if not ffr.load_data():
        ffr.load_event_data()
        ffr.process_data()
    ffr.bin_delays(4)
    ffr.get_precs()
    ffr.plot()


if __name__ == "__main__":
    with open('/data/eeg/scalp/ltp/ltpFR3_MTurk/stats/all.json', 'r') as f:
        s = json.load(f)

    means = s['mean']
    sems = s['sem']

    #fig2_spc(means, sems)
    #fig3_pfr(means, sems)
    #fig4_crp(means, sems)
    #fig5_pli(means, sems)
    #fig6_irt(means, sems)
    #fig7_ffr()

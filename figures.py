import json
import numpy as np
import matplotlib.pyplot as plt
from FFR import FFRAnalyzer


VIS_FMT = 'C0-'
AUD_FMT = 'C3-'
ERR_VIS = 'C0'
ERR_AUD = 'C3'
ERR_ALPHA = .4


def fig2_spc(m, s):
    m = m['spc']
    s = s['spc']

    # SPCs for fast presentation
    ax = plt.subplot(121)
    ax.plot(range(1, 13), m['fv12'], VIS_FMT)
    ax.fill_between(range(1, 13), np.add(m['fv12'], s['fv12']), np.subtract(m['fv12'], s['fv12']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 13), m['fa12'], AUD_FMT)
    ax.fill_between(range(1, 13), np.add(m['fa12'], s['fa12']), np.subtract(m['fa12'], s['fa12']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 25), m['fv24'], VIS_FMT)
    ax.fill_between(range(1, 25), np.add(m['fv24'], s['fv24']), np.subtract(m['fv24'], s['fv24']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 25), m['fa24'], AUD_FMT)
    ax.fill_between(range(1, 25), np.add(m['fa24'], s['fa24']), np.subtract(m['fa24'], s['fa24']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
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
    ax.plot(range(1, 13), m['sv12'], VIS_FMT)
    ax.fill_between(range(1, 13), np.add(m['sv12'], s['sv12']), np.subtract(m['sv12'], s['sv12']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 13), m['sa12'], AUD_FMT)
    ax.fill_between(range(1, 13), np.add(m['sa12'], s['sa12']), np.subtract(m['sa12'], s['sa12']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 25), m['sv24'], VIS_FMT)
    ax.fill_between(range(1, 25), np.add(m['sv24'], s['sv24']), np.subtract(m['sv24'], s['sv24']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 25), m['sa24'], AUD_FMT)
    ax.fill_between(range(1, 25), np.add(m['sa24'], s['sa24']), np.subtract(m['sa24'], s['sa24']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
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
    ax.plot(range(1, 13), m['fv12'], VIS_FMT)
    ax.fill_between(range(1, 13), np.add(m['fv12'], s['fv12']), np.subtract(m['fv12'], s['fv12']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 13), m['fa12'], AUD_FMT)
    ax.fill_between(range(1, 13), np.add(m['fa12'], s['fa12']), np.subtract(m['fa12'], s['fa12']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 25), m['fv24'], VIS_FMT)
    ax.fill_between(range(1, 25), np.add(m['fv24'], s['fv24']), np.subtract(m['fv24'], s['fv24']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 25), m['fa24'], AUD_FMT)
    ax.fill_between(range(1, 25), np.add(m['fa24'], s['fa24']), np.subtract(m['fa24'], s['fa24']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
    ax.set_title('Fast Presentation')
    ax.set_xlabel('Serial Position')
    ax.set_ylabel('Probability of First Recall')
    ax.legend(labels=['Visual', 'Auditory'])
    ax.set_ylim(0, .55)
    ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # PFR curves for slow presentation
    ax = plt.subplot(122)
    ax.plot(range(1, 13), m['sv12'], VIS_FMT)
    ax.fill_between(range(1, 13), np.add(m['sv12'], s['sv12']), np.subtract(m['sv12'], s['sv12']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 13), m['sa12'], AUD_FMT)
    ax.fill_between(range(1, 13), np.add(m['sa12'], s['sa12']), np.subtract(m['sa12'], s['sa12']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 25), m['sv24'], VIS_FMT)
    ax.fill_between(range(1, 25), np.add(m['sv24'], s['sv24']), np.subtract(m['sv24'], s['sv24']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(range(1, 25), m['sa24'], AUD_FMT)
    ax.fill_between(range(1, 25), np.add(m['sa24'], s['sa24']), np.subtract(m['sa24'], s['sa24']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
    ax.set_title('Slow Presentation')
    ax.set_xlabel('Serial Position')
    ax.set_ylabel('Probability of First Recall')
    ax.legend(labels=['Visual', 'Auditory'])
    ax.set_ylim(0, .55)
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
        s[filt][int(len(s[filt]) / 2)] = np.nan

    crp_range = range(-4, 5)

    # PFR curves for short list/fast presentation
    ax = plt.subplot(221)
    ax.plot(crp_range, m['fv12'], VIS_FMT)
    ax.fill_between(crp_range, np.add(m['fv12'], s['fv12']), np.subtract(m['fv12'], s['fv12']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(crp_range, m['fa12'], AUD_FMT)
    ax.fill_between(crp_range, np.add(m['fa12'], s['fa12']), np.subtract(m['fa12'], s['fa12']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
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
    ax.plot(crp_range, m['sv12'], VIS_FMT)
    ax.fill_between(crp_range, np.add(m['sv12'], s['sv12']), np.subtract(m['sv12'], s['sv12']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(crp_range, m['sa12'], AUD_FMT)
    ax.fill_between(crp_range, np.add(m['sa12'], s['sa12']), np.subtract(m['sa12'], s['sa12']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
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
    ax.plot(crp_range, m['fv24'], VIS_FMT)
    ax.fill_between(crp_range, np.add(m['fv24'], s['fv24']), np.subtract(m['fv24'], s['fv24']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(crp_range, m['fa24'], AUD_FMT)
    ax.fill_between(crp_range, np.add(m['fa24'], s['fa24']), np.subtract(m['fa24'], s['fa24']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
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
    ax.plot(crp_range, m['sv24'], VIS_FMT)
    ax.fill_between(crp_range, np.add(m['sv24'], s['sv24']), np.subtract(m['sv24'], s['sv24']), color=ERR_VIS,
                    alpha=ERR_ALPHA)
    ax.plot(crp_range, m['sa24'], AUD_FMT)
    ax.fill_between(crp_range, np.add(m['sa24'], s['sa24']), np.subtract(m['sa24'], s['sa24']), color=ERR_AUD,
                    alpha=ERR_ALPHA)
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


def fig6_irt(m, s, n):
    m = m['irt']
    s = s['irt']
    n = n['irt']
    for filt in s:
        for i, row in enumerate(s[filt]):
            for j, item in enumerate(row):
                s[filt][i][j] = np.nan if item is None or n[filt][i][j] < 30 else item
                m[filt][i][j] = np.nan if n[filt][i][j] < 30 else m[filt][i][j]

    ax = plt.subplot(221)
    ax.plot([], [], VIS_FMT)
    ax.plot([], [], AUD_FMT)
    ax.plot(range(1, 14), np.array(m['fv12']).T, VIS_FMT)
    ax.plot(range(1, 14), np.array(m['fa12']).T, AUD_FMT)
    ax.legend(labels=['Visual', 'Auditory'])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_title('Slow')
    """
    for i, row in enumerate(m['fv12']):
        ax.fill_between(range(1, 14), np.add(m['fv12'][i], s['fv12'][i]), np.subtract(m['fv12'][i], s['fv12'][i]), color=ERR_VIS, alpha=ERR_ALPHA)
    for i, row in enumerate(m['fa12']):
        ax.fill_between(range(1, 14), np.add(m['fa12'][i], s['fa12'][i]), np.subtract(m['fa12'][i], s['fa12'][i]), color=ERR_AUD, alpha=ERR_ALPHA)
    """

    ax = plt.subplot(222)
    ax.plot([], [], VIS_FMT)
    ax.plot([], [], AUD_FMT)
    ax.plot(range(1, 14), np.array(m['sv12']).T, VIS_FMT)
    ax.plot(range(1, 14), np.array(m['sa12']).T, AUD_FMT)
    ax.legend(labels=['Visual', 'Auditory'])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_title('Fast')
    """
    for i, row in enumerate(m['sv12']):
        ax.fill_between(range(1, 14), np.add(m['sv12'][i], s['sv12'][i]), np.subtract(m['sv12'][i], s['sv12'][i]), color=ERR_VIS, alpha=ERR_ALPHA)
    for i, row in enumerate(m['sa12']):
        ax.fill_between(range(1, 14), np.add(m['sa12'][i], s['sa12'][i]), np.subtract(m['sa12'][i], s['sa12'][i]), color=ERR_AUD, alpha=ERR_ALPHA)
    """

    ax = plt.subplot(223)
    ax.plot([], [], VIS_FMT)
    ax.plot([], [], AUD_FMT)
    ax.plot(range(1, 26), np.array(m['fv24']).T, VIS_FMT)
    ax.plot(range(1, 26), np.array(m['fa24']).T, AUD_FMT)
    ax.legend(labels=['Visual', 'Auditory'])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    """
    for i, row in enumerate(m['fv24']):
        ax.fill_between(range(1, 26), np.add(m['fv24'][i], s['fv24'][i]), np.subtract(m['fv24'][i], s['fv24'][i]), color=ERR_VIS, alpha=ERR_ALPHA)
    for i, row in enumerate(m['fa24']):
        ax.fill_between(range(1, 26), np.add(m['fa24'][i], s['fa24'][i]), np.subtract(m['fa24'][i], s['fa24'][i]), color=ERR_AUD, alpha=ERR_ALPHA)
    """

    ax = plt.subplot(224)
    ax.plot([], [], VIS_FMT)
    ax.plot([], [], AUD_FMT)
    ax.plot(range(1, 26), np.array(m['sv24']).T, VIS_FMT)
    ax.plot(range(1, 26), np.array(m['sa24']).T, AUD_FMT)
    ax.legend(labels=['Visual', 'Auditory'])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    """
    for i, row in enumerate(m['sv24']):
        ax.fill_between(range(1, 26), np.add(m['sv24'][i], s['sv24'][i]), np.subtract(m['sv24'][i], s['sv24'][i]), color=ERR_VIS, alpha=ERR_ALPHA)
    for i, row in enumerate(m['sa24']):
        ax.fill_between(range(1, 26), np.add(m['sa24'][i], s['sa24'][i]), np.subtract(m['sa24'][i], s['sa24'][i]), color=ERR_AUD, alpha=ERR_ALPHA)
    """

    plt.show()


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
    Ns = s['N']

    fig2_spc(means, sems)
    fig3_pfr(means, sems)
    fig4_crp(means, sems)
    #fig5_pli(means, sems)
    fig6_irt(means, sems, Ns)
    #fig7_ffr()

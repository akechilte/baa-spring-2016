import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


def plot_hist_chart(file_name):
    """
    plots the bar chart for disbursement amount spent by candidates in 2016 US election
    x-axis: candidate name
    y-axis: amount spent in millions of dollars
    :param file_name:
    :return:
    """
    df = pd.read_csv(file_name, index_col=False,sep='|')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pos = np.arange(len(df.cand_nm))
    ax = plt.axes()
    ax.set_xticks(pos)
    ax.set_xticklabels(df.cand_nm, rotation=60)
    plt.bar(pos, df.disb_amt, 1.0, color='b')
    plt.ylabel('Amount spent in millions $')
    plt.xlabel('Candidate Name')
    plt.title('2016 US Election disbursement amount spend by candidates: 2015-2016', y=1.08)
    fig.set_tight_layout(True)
    fig.savefig('./histogram.png')

if __name__ == '__main__':
    """
    entry point of the script.  invokes plot_hist with given filename
    """
    file_name = sys.argv[1]
    plot_hist_chart('./%s' %file_name)

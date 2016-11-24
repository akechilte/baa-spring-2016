import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


def plot_line_chart(file_name):
    """
    plots the bar chart for disbursement amount spent by year & month for the years 2015 & 2016
    x-axis: year & month
    y-axis: disbursement amount spent is millions of dollars
    :param file_name:
    :return:
    """
    df = pd.read_csv(file_name, index_col=False,sep=',')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pos = np.arange(len(df.spend_yr_mon))
    ax = plt.axes()
    ax.set_xticks(pos)
    ax.set_xticklabels(df.spend_yr_mon, rotation=60)
    plt.plot(pos, df.disb_amt, marker='o')
    plt.title('2016 US Election disbursement amount spend by year & month: 2015-2016', color='black', y=1.08)
    plt.xlabel('Year & Month')
    plt.ylabel('Amount spent in millions $')
    fig.set_tight_layout(True)
    fig.savefig('./linechart.png')

if __name__ == '__main__':
    """
    entry point of the script, invokes plot_line_char module with given file name
    """
    file_name = sys.argv[1]
    plot_line_chart('./%s' %file_name)

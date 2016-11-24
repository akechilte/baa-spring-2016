import urllib2
import zipfile
import pandas as pd
import numpy as np


def download():
    """
    uses ftp protocol to download the dataset
    unzips and writes into the same directory
    :return:
    """
    data_src_url = 'ftp://ftp.fec.gov/FEC/Presidential_Map/2016/P00000001/P00000001D-ALL.zip'
    request = urllib2.urlopen(data_src_url)

    with open("./data.zip", "wb") as f:
        f.write(request.read())

    with zipfile.ZipFile("./data.zip", "r") as z:
        z.extractall("./")


def cleanse_data():
    """
    reads csv file, standardizes disbursement date to yyyy-MM-dd format
    generates year-mon column in yy-MM format
    :return: processed dataframe
    """
    df = pd.read_csv('./P00000001D-ALL.csv', index_col=False, dtype={"cmte_id":object,"cand_id":object,"cand_nm":object,"recipient_nm":object,"disb_amt":float,"disb_dt":object,"recipient_city":object,"recipient_st":object,"recipient_zip":object,"disb_desc":object,"memo_cd":object,"memo_text":object,"form_tp":object,"file_num":int,"tran_id":object,"election_tp":object})
    df['spend_dt'] = pd.to_datetime(df.disb_dt,format="%d-%b-%y")
    df = df[(df.spend_dt.dt.year == 2015) | (df.spend_dt.dt.year == 2016)]
    df['spend_yr_mon'] = df.spend_dt.dt.strftime('%y-%m')
    return df


def put_line_csv(df):
    """
    aggregates disbursement amount by year & month
    :param df:
    :return:
    """
    aggregations = {
        'disb_amt': sum
    }
    df_agg = df.groupby(['spend_yr_mon']).agg(aggregations).reset_index()
    df_agg.to_csv('./data-line.csv',sep=',',index=False)


def put_hist_csv(df):
    """
    aggregates disbursement amount by candidate name, selects top 10
    candidates by amount spent in descending order and shuffles them
    :param df:
    :return:
    """
    aggregations = {
        'disb_amt': sum
    }
    df_agg = df.groupby(['cand_nm']).agg(aggregations).reset_index()
    df_top10 = df_agg.sort_values('disb_amt', ascending=False).head(10)
    df_top10 = df_top10.iloc[np.random.permutation(len(df_top10))]
    df_top10.to_csv('./data-hist.csv', sep='|',index=False)


if __name__ == '__main__':
    """
    entry point of the script and invokes the modules in sequence
    """
    download()
    df = cleanse_data()
    put_line_csv(df)
    put_hist_csv(df)



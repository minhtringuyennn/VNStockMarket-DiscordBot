from datetime import datetime 
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import re

def convert_date(text, date_type = '%Y-%m-%d'):
    return datetime.strptime(text, date_type)

def convert_text_dateformat(text, origin_type = '%Y-%m-%d', new_type = '%Y-%m-%d'):
    return convert_date(text, origin_type).strftime(new_type)

def weekday_candlestick(ax, ohlc_data, fmt='%b %d', freq=1, **kwargs):
    # Convert data to numpy array
    ohlc_data_arr = np.array(ohlc_data)
    ohlc_data_arr2 = np.hstack(
        [np.arange(ohlc_data_arr[:,0].size)[:,np.newaxis], ohlc_data_arr[:,1:]])
    ndays = ohlc_data_arr2[:,0]
    
    # Convert matplotlib date numbers to strings based on `fmt`
    dates = mdates.num2date(ohlc_data_arr[:,0])
    date_strings = []
    for date in dates:
        date_strings.append(date.strftime(fmt))

    # # Plot candlestick chart
    candlestick_ohlc(ax, ohlc_data_arr2, colorup='g', colordown='r', width=0.8, **kwargs)

    # Format x axis
    ax.set_xticks(ndays[::freq])
    ax.set_xticklabels(date_strings[::freq], rotation=45, ha='center')

def calc_break_day(data, start_date, end_date):
    dt_chart = data['date'].index
    print(dt_chart)
    dt_chart = pd.to_datetime(dt_chart).strftime("%Y-%m-%d").tolist()
    
    dt_all = []
    delta =  datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
    for i in range(delta.days + 1):
        day = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=i)
        dt_all.append(day.strftime('%Y-%m-%d'))
    
    res = [i for i in dt_chart + dt_all if i not in dt_chart or i not in dt_all]
    
    return res

def _isOHLC(data):
    try:
        cols = dict(data.columns)
    except:
        cols = list(data.columns)

    defau_cols = ['high', 'low', 'close', 'open']

    if all(col in cols for col in defau_cols):
        return True
    else:
        return False

def _isOHLCV(data):
    try:
        cols = dict(data.columns)
    except:
        cols = list(data.columns)

    defau_cols = ['high', 'low', 'close', 'open', 'volume']

    if all(col in cols for col in defau_cols):
        return True
    else:
        return False
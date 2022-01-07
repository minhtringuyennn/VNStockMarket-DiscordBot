from datetime import datetime
from datetime import datetime 
from datetime import timedelta
import pandas as pd
import re

def convert_date(text, date_type = '%Y-%m-%d'):
    return datetime.strptime(text, date_type)

def convert_text_dateformat(text, origin_type = '%Y-%m-%d', new_type = '%Y-%m-%d'):
    return convert_date(text, origin_type).strftime(new_type)

def calc_break_day(data, symbol, start_date, end_date):
    dt_chart = data['open'][symbol].index
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
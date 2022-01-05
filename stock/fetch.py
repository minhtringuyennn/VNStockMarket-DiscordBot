# Import lib
from bs4 import BeautifulSoup
from datetime import datetime

import re, time, requests

import numpy as np
import pandas as pd
import logging as logging
import stock.utils as utils

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}

# Struct
class Stocks():
    def __init__(self, symbols, start, end):
        self.symbols = symbols
        self.start = utils.convert_text_dateformat(start, new_type = '%d/%m/%Y')
        self.end = utils.convert_text_dateformat(end, new_type = '%d/%m/%Y')

# Load data from API
class DataLoader():
    def __init__(self, symbols, start, end, minimal = True):
        self.symbols = symbols
        self.start = start
        self.end = end
        self.minimal = minimal

    def download(self):
        loader = Fetch(self.symbols, self.start, self.end)
        stock_data = loader.batch_download()

        if self.minimal:
            minimal_data = stock_data[['open','close','volume']]
            return minimal_data
        else:
            return stock_data

# Fetch data from API
class Fetch(Stocks):
    def __init__(self, symbols, start, end):
        self.symbols = symbols
        self.start = start
        self.end = end
        super().__init__(symbols, start, end)

    def batch_download(self):
        stock_datas = []
        
        # Check symbols contains list of stocks or not
        if not isinstance(self.symbols, list):
            symbols = [self.symbols]
        else:
            symbols = self.symbols

        for symbol in symbols:
            stock_datas.append(self.download_new(symbol))

        data = pd.concat(stock_datas, axis=1)
        return data

    def download_new(self, symbol):
        # Convert date
        start_date = utils.convert_text_dateformat(self.start, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d')
        end_date = utils.convert_text_dateformat(self.end, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d')
        
        # API
        API_VNDIRECT = 'https://finfo-api.vndirect.com.vn/v4/stock_prices/'
        query = 'code:' + symbol + '~date:gte:' + start_date + '~date:lte:' + end_date
        
        delta = datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
        
        params = {
            "sort": "date",
            "size": delta.days + 1,
            "page": 1,
            "q": query
        }
        
        # Get reponse from API
        res = requests.get(API_VNDIRECT, params=params, headers=HEADERS)
        data = res.json()['data']  
        data = pd.DataFrame(data)
        
        # Define label
        stock_data = data[['date', 'adClose', 'close', 'pctChange', 'average', 'nmVolume',
                        'nmValue', 'ptVolume', 'ptValue', 'open', 'high', 'low']].copy()
        stock_data.columns = ['date', 'adjust', 'close', 'change_perc', 'avg',
                        'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile',
                        'open', 'high', 'low']

        # Set index by date
        stock_data = stock_data.set_index('date').apply(pd.to_numeric, errors='coerce')
        stock_data.index = list(map(utils.convert_date, stock_data.index))
        
        stock_data = stock_data.sort_index() # Sort table
        stock_data.fillna(0, inplace=True) # Fill NaN --> 0
        
        # Add volumn column
        stock_data['volume'] = stock_data.volume_match + stock_data.volume_reconcile

        # Add label
        iterables = [stock_data.columns.tolist(), [symbol]]
        mulindex = pd.MultiIndex.from_product(iterables, names=['Attributes', 'Symbols'])
        stock_data.columns = mulindex

        # Logging
        logging.info('data {} from {} to {} clone successfully!' \
                     .format(symbol,
                             utils.convert_text_dateformat(self.start, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d'),
                             utils.convert_text_dateformat(self.end, origin_type='%d/%m/%Y', new_type='%Y-%m-%d')))

        # Return data
        return stock_data
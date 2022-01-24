# Import lib
from bs4 import BeautifulSoup
from datetime import datetime

import re, time, requests

import numpy as np
import pandas as pd
import logging as logging

import stock_modules.utils as utils

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

    def fetchPrice(self):
        loader = FetchDailyPrice(self.symbols, self.start, self.end)
        stock_data = loader.batch_download()

        if self.minimal:
            minimal_data = stock_data[['date', 'high','low','open','close', 'volume']]
            return minimal_data
        else:
            return stock_data

# Fetch daily stock price from API
class FetchDailyPrice(Stocks):
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

        # Clean up data
        # stock_data = stock_data.set_index('date').apply(pd.to_numeric, errors='coerce')
        stock_data = stock_data.sort_index(ascending=False) # Sort table
        stock_data.fillna(0, inplace=True) # Fill NaN --> 0
        
        # Add volumn column
        stock_data['volume'] = stock_data.volume_match

        # Add label
        iterables = [stock_data.columns.tolist(), [symbol]]

        # Logging
        logging.info('data {} from {} to {} clone successfully!' \
                     .format(symbol,
                             utils.convert_text_dateformat(self.start, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d'),
                             utils.convert_text_dateformat(self.end, origin_type='%d/%m/%Y', new_type='%Y-%m-%d')))

        # Return data
        return stock_data

class FetchCategories():
    def __init__(self):
        super().__init__()
        
    def fetchFloor(self, floor = "HOSE"):
        if floor != "HOSE" and floor != "HNX" and floor != "UPCOM":
            logging.info('Floor is not support!'.format(floor))
            return None
        
        # API
        API_VNDIRECT = f'https://finfo-api.vndirect.com.vn/stocks?floor={floor}'
        
        # Get reponse from API
        res = requests.get(API_VNDIRECT, headers=HEADERS)
        data = res.json()['data']  
        data = pd.DataFrame(data)
        
        stock_data = data[['symbol', 'companyName', 'listedDate', 'delistedDate', 'floor', 'industryName']].copy()

        # Clean up data
        stock_data = stock_data.sort_index() # Sort table
        stock_data.fillna(0, inplace=True) # Fill NaN --> 0

        # Logging
        logging.info('data from floor {} clone successfully!'.format(floor))

        # Return data
        return stock_data
    
    def fetchVN30(self):
        # API
        API_VNDIRECT = 'https://finfo-api.vndirect.com.vn/stocks?indexCode=VN30'
        
        # Get reponse from API
        res = requests.get(API_VNDIRECT, headers=HEADERS)
        data = res.json()['data']  
        data = pd.DataFrame(data)
        
        stock_data = data[['symbol', 'companyName', 'listedDate', 'delistedDate', 'floor', 'industryName']].copy()

        # Clean up data
        stock_data = stock_data.sort_index() # Sort table
        stock_data.fillna(0, inplace=True) # Fill NaN --> 0

        # Logging
        logging.info('data VN30 clone successfully!')

        # Return data
        return stock_data
    
    def batch_download(self, symbols):
        stock_datas = []
        
        # Check symbols contains list of stocks or not
        if not isinstance(symbols, list):
            symbols = [symbols]

        for symbol in symbols:
            stock_datas.append(self.download_new(symbol))
        
        data = pd.concat(stock_datas)
        logging.info('batch clone successfully with {} stocks!'.format(len(symbols)))
        
        return data
    
    def download_new(self, symbol):
        # API
        API_VNDIRECT = f'https://finfo-api.vndirect.com.vn/stocks?symbol={symbol}'
        
        # Get reponse from API
        res = requests.get(API_VNDIRECT, headers=HEADERS)
        data = res.json()['data']  
        data = pd.DataFrame(data)
        
        stock_data = data[['symbol', 'companyName', 'listedDate', 'delistedDate', 'floor', 'industryName']].copy()
        
        # Clean up data
        stock_data.fillna(0, inplace=True) # Fill NaN --> 0

        # Logging
        logging.info('data stock {} clone successfully!'.format(symbol))

        # Return data
        return stock_data
    
def call_api_vietstock(code):
        url = "https://finance.vietstock.vn/company/tradinginfo"
        payload = "code=" + code +"&s=0&t=&__RequestVerificationToken=75slVHRS7aY7-7-JG2k93XdF5nuFv-iYOn2pwiEZLKomN9xWkmqSGtmOL1fTDvXrxVVMZTzyXpUpNhh1bld_oze2QRBNA69Sqjgebh0lW_U1"
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://finance.vietstock.vn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Cookie': '_ga=GA1.2.1707987505.1614912967; _ga=GA1.3.1707987505.1614912967; cto_bundle=8qmXGl9LWkdZMlVHUE8lMkZwaXglMkJ1SFUlMkIlMkJ1V0pMdmF1JTJGS3RCZ3poSTVoa0lzYTNxeTdldFBVVmpXUVFtNkpOdndoY0JtcXIyanJ4JTJGWmVscEFIazJCNlp1azdSRUR3UWlXQTYxalRjSTZnSDZJbDViRThXMzV4dlFHcnp2YTdxQVEyRUh4JTJGN21ySmJDZXI0UllMeEpqc2RzbzEyUSUzRCUzRA; __gpi=00000000-0000-0000-0000-000000000000:dmlldHN0b2NrLnZu:Lw==; dable_uid=93060591.1616146515585; dable_uid=93060591.1616146515585; language=vi-VN; Theme=Light; AnonymousNotification=; vst_usr_lg_token=jjez3jbP3EWZ8wYwm26JaQ==; isShowLogin=true; _gid=GA1.2.1696256141.1642730153; ASP.NET_SessionId=hzfkmzpetr231wvmgv455a5t; __RequestVerificationToken=UYwRjudgJ9H0TIP7aoV7jSJqJE55hOj5Ii-quhMDoi1o-GBlbaqpf47xqXLjns4tiXoZtOWW4dDRKsUxJXl1k0iqGl9ExzwCan7LirbnCm41; _gid=GA1.3.1696256141.1642730153; finance_viewedstock=SHB,; __gads=ID=82f158bde4b0d37d-2262a63212d00076:T=1628493476:RT=1642765519:S=ALNI_MbcsprDov24W8oeRxHObWAzyj15uQ'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
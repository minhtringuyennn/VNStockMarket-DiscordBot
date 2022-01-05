import stock.fetch as dl

print('Enter your symbol: ')
Symbol = input().upper()

loader = dl.DataLoader(Symbol, '2021-01-05','2022-01-05')
data = loader.download()

MOVING_AVERAGES_20 = 20
MOVING_AVERAGES_50 = 50
MOVING_AVERAGES_100 = 100

_MA20 = data['close'][Symbol].rolling(MOVING_AVERAGES_20, min_periods=1).mean().tolist()
_MA50 = data['close'][Symbol].rolling(MOVING_AVERAGES_50, min_periods=1).mean().tolist()
_MA100 = data['close'][Symbol].rolling(MOVING_AVERAGES_100, min_periods=1).mean().tolist()

def Message(msg, symbol, data):
    oPrice = data['open'][symbol][idx]
    cPrice = data['close'][symbol][idx]
    print(f"\n{msg} {symbol} at {data['open'][symbol].index[idx]}. Pricing is {cPrice}.")
    
idx = 0
for val in _MA20:
    oPrice = data['open'][Symbol][idx]
    cPrice = data['close'][Symbol][idx]
    
    if oPrice > cPrice and oPrice > val and cPrice < val:
        Message("Sell", Symbol, data)
    elif oPrice < cPrice and oPrice < val and cPrice > val:
        Message("Buy", Symbol, data)
        
    idx = idx + 1
import stock.fetch as fetch
import stock.indicate as indicate
import stock.figure as figure

# # TODO
# Candle plot, chart
# 30 minutes loop 100 stocks in HOSE
# Use telegram API to notify

Symbol = "REE"
start_date = "2021-01-01"
end_date = "2022-01-07"

loader = fetch.DataLoader(Symbol, start_date, end_date)
data = loader.fetchPrice()

_VOL = data['volume'][Symbol]

_MA20 = indicate.calcMovingAverage(data['close'][Symbol], 20)
_MA50 = indicate.calcMovingAverage(data['close'][Symbol], 50)
_MA100 = indicate.calcMovingAverage(data['close'][Symbol], 100)

_RSI = indicate.calcRSI(data['close'][Symbol])

_BB = indicate.calcBollingerBand(data['close'][Symbol])

_MACD = indicate.calcMACD(data['close'][Symbol])

# print(f"Moving average:\n{_MA50}\n")
# print(f"RSI:\n{_RSI}\n")
# print(f"Bollinger Band:\n{_BB}\n")
# print(f"MACD:\n{_MACD}\n")

figure.drawCandleStick(data, start_date, end_date, vol = _VOL, rsi = _RSI)
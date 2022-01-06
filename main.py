import stock.fetch as fetch
import stock.indicate as indicate

# # TODO
# Candle plot, chart
# 30 minutes loop 100 stocks in HOSE
# Use telegram API to notify

Symbol = "VIC"

loader = fetch.DataLoader(Symbol, "2021-01-01", "2022-01-07")
data = loader.fetchPrice()

_MA20 = indicate.calcMovingAverage(data['close'][Symbol], 20)
_MA50 = indicate.calcMovingAverage(data['close'][Symbol], 50)
_MA100 = indicate.calcMovingAverage(data['close'][Symbol], 100)

_RSI = indicate.calcRSI(data['close'][Symbol])

_BB = indicate.calcBollingerBand(data['close'][Symbol])

_MACD = indicate.calcMACD(data['close'][Symbol])

print(f"Moving average:\n{_MA50}\n")
print(f"RSI:\n{_RSI}\n")
print(f"Bollinger Band:\n{_BB}\n")
print(f"MACD:\n{_MACD}\n")

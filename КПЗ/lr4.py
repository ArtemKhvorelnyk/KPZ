import pandas as pd
import ta
from matplotlib import pyplot as plt
from binance import Client

# Загрузка данных с Binance
client = Client()
k_lines = client.get_historical_klines(
    symbol="BTCUSDT",
    interval=Client.KLINE_INTERVAL_1MINUTE,
    start_str="1 day ago UTC",
    end_str="now UTC"
)

# Создание DataFrame с нужными столбцами
columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
k_lines = pd.DataFrame(k_lines, columns=columns)
k_lines['time'] = pd.to_datetime(k_lines['time'], unit='ms')
k_lines[['open', 'high', 'low', 'close']] = k_lines[['open', 'high', 'low', 'close']].astype(float)

# Расчет индикаторов RSI для заданных периодов
periods = [14, 27, 100]
for period in periods:
    rsi_indicator = ta.momentum.RSIIndicator(k_lines['close'], period)
    k_lines[f'RSI_{period}'] = rsi_indicator.rsi()

# Визуализация цены закрытия и индикаторов RSI
plt.figure(figsize=(14, 14))

# График цены закрытия
plt.subplot(4, 1, 1)
plt.plot(k_lines['time'], k_lines['close'], label='Close Price')
plt.title('Close Price')
plt.legend()

# График RSI для периода 14
plt.subplot(4, 1, 2)
plt.plot(k_lines['time'], k_lines['RSI_14'], label='RSI 14', color='purple')
plt.title('RSI 14')
plt.legend()

# График RSI для периода 27
plt.subplot(4, 1, 3)
plt.plot(k_lines['time'], k_lines['RSI_27'], label='RSI 27', color='blue')
plt.title('RSI 27')
plt.legend()

# График RSI для периода 100
plt.subplot(4, 1, 4)
plt.plot(k_lines['time'], k_lines['RSI_100'], label='RSI 100', color='green')
plt.title('RSI 100')
plt.legend()

plt.tight_layout()
plt.show()

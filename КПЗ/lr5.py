import pandas as pd
import ta
from matplotlib import pyplot as plt
from binance import Client
from dataclasses import dataclass

@dataclass
class Signal:
    time: pd.Timestamp
    asset: str
    quantity: float
    side: str
    entry: float
    take_profit: float
    stop_loss: float
    result: float

def create_signals(k_lines):
    signals = []
    for i in range(len(k_lines)):
        signal = "No signal"
        take_profit_price = None
        stop_loss_price = None
        current_price = k_lines.iloc[i]['close']
        
        # Условия для сигналов покупки и продажи
        if k_lines.iloc[i]['cci'] < -100 and k_lines.iloc[i]['adx'] > 25:
            signal = 'sell'
        elif k_lines.iloc[i]['cci'] > 100 and k_lines.iloc[i]['adx'] > 25:
            signal = 'buy'
        
        # Расчет уровней take profit и stop loss
        if signal == "buy":
            stop_loss_price = round((1 - 0.02) * current_price, 1)
            take_profit_price = round((1 + 0.1) * current_price, 1)
        elif signal == "sell":
            stop_loss_price = round((1 + 0.02) * current_price, 1)
            take_profit_price = round((1 - 0.1) * current_price, 1)

        signals.append(Signal(
            k_lines.iloc[i]['time'],
            'BTCUSDT',
            100,
            signal,
            current_price,
            take_profit_price,
            stop_loss_price,
            None  # Добавили аргумент result
        ))

    return signals

# Загрузка данных с Binance
client = Client()
k_lines = client.get_historical_klines(
    symbol="BTCUSDT",
    interval=Client.KLINE_INTERVAL_1MINUTE,
    start_str="1 week ago UTC",
    end_str="now UTC"
)

# Создание DataFrame с нужными столбцами
columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
k_lines = pd.DataFrame(k_lines, columns=columns)
k_lines['time'] = pd.to_datetime(k_lines['time'], unit='ms')
k_lines[['open', 'high', 'low', 'close']] = k_lines[['open', 'high', 'low', 'close']].astype(float)

# Расчет индикаторов ADX и CCI
k_lines['adx'] = ta.trend.ADXIndicator(k_lines['high'], k_lines['low'], k_lines['close']).adx()
k_lines['cci'] = ta.trend.CCIIndicator(k_lines['high'], k_lines['low'], k_lines['close']).cci()

# Генерация сигналов
signals = create_signals(k_lines)

# Вывод сигналов
if signals:
    for sig in signals:
        print(sig)
else:
    print("No signals generated.")

# Визуализация данных
plt.figure(figsize=(12, 6))
plt.plot(k_lines['time'], k_lines['close'], label='BTCUSDT price')

for signal in signals:
    if signal.side == 'buy':
        plt.scatter(signal.time, signal.entry, color='green', label='Buy signal', marker='^', s=100)
    elif signal.side == 'sell':
        plt.scatter(signal.time, signal.entry, color='red', label='Sell signal', marker='v', s=100)

plt.title('BTCUSDT price and signals')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend(loc='best')
plt.grid(True)
plt.show()

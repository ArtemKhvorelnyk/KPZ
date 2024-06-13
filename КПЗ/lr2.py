import pandas as pd
from binance import Client

# Функция для расчета индекса относительной силы (RSI)
def calculate_rsi(prices, period):
    deltas = prices.diff().dropna()  # Вычисляем разницу между последовательными ценами и удаляем NaN
    gains = deltas.where(deltas > 0, 0)  # Прибыль (только положительные изменения)
    losses = -deltas.where(deltas < 0, 0)  # Убыток (только отрицательные изменения)
    average_gain = gains.rolling(window=period).mean()  # Средняя прибыль за период
    average_loss = losses.rolling(window=period).mean()  # Средний убыток за период
    rs = average_gain / average_loss  # Отношение средней прибыли к среднему убытку
    rsi = 100 - (100 / (1 + rs))  # Вычисляем RSI
    return rsi

# Функция для получения данных RSI для заданного актива и периодов
def get_rsi_data(asset, periods):
    client = Client()  # Инициализируем клиента Binance
    k_lines = client.get_historical_klines(
        symbol=asset,
        interval=Client.KLINE_INTERVAL_1MINUTE,
        start_str="1 day ago UTC",
        end_str="now UTC"
    )
    
    # Преобразуем данные в DataFrame и оставляем только нужные столбцы
    k_lines = pd.DataFrame(k_lines)[[0, 4]]
    k_lines[0] = pd.to_datetime(k_lines[0], unit='ms')  # Преобразуем время в datetime
    k_lines[4] = k_lines[4].astype(float)  # Преобразуем цены закрытия в float
    k_lines = k_lines.rename(columns={0: 'time', 4: 'close'})  # Переименовываем столбцы

    # Создаем DataFrame для результатов
    result = pd.DataFrame()
    result['time'] = k_lines['time']

    # Вычисляем RSI для каждого периода и добавляем в результирующий DataFrame
    for period in periods:
        rsi_values = calculate_rsi(k_lines['close'], period)
        result[f'RSI {period}'] = rsi_values

    return result

# Устанавливаем актив и периоды для расчета
asset = "BTCUSDT"
periods = [14, 27, 100]

# Получаем данные RSI и выводим их
rsi_data = get_rsi_data(asset, periods)
print(rsi_data)

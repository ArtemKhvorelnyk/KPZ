import pandas as pd
import datetime as dt

# Пытаемся загрузить данные из файла
try:
    data_frame = pd.read_csv('filename.csv')
except FileNotFoundError:
    # Если файл не найден, создаем пустой DataFrame с необходимыми колонками
    data_frame = pd.DataFrame({'year': [], 'month': [], 'day': [], 'hour': [], 'minute': [], 'second': []})

# Получаем текущее время
current_time = dt.datetime.now()

# Создаем новую строку с текущим временем
new_row = pd.DataFrame({
    'year': [current_time.year],
    'month': [current_time.month],
    'day': [current_time.day],
    'hour': [current_time.hour],
    'minute': [current_time.minute],
    'second': [current_time.second]
})

# Добавляем новую строку к существующему DataFrame
data_frame = pd.concat([data_frame, new_row], ignore_index=True)

# Сохраняем обновленный DataFrame в файл
data_frame.to_csv('filename.csv', index=False)

# Выводим DataFrame на экран
print(data_frame)

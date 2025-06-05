import pandas as pd
import numpy as np
import random, os

# Установим зерно для воспроизводимости
np.random.seed(42)
random.seed(42)

dir_path=os.path.join('Courses','1_DS','notebooks_cracked.csv')

num_entries = 10000

# Создаем базовые данные
data = {
    'Brand': np.random.choice(['Dell', 'HP', 'Lenovo', 'Apple', 'Asus', 'Acer', 'Microsoft', 'Razer'], num_entries),
    'Model': [f'Model_{i}' for i in range(num_entries)], # Модели будут уникальными для начала
    'Processor': np.random.choice(['Intel i5', 'Intel i7', 'AMD Ryzen 5', 'AMD Ryzen 7', 'Apple M1', 'Intel i9'], num_entries),
    'RAM_GB': np.random.choice([8, 16, 32, 64], num_entries),
    'Storage_GB': np.random.choice([256, 512, 1024, 2048], num_entries),
    'Screen_Size_Inches': np.round(np.random.normal(loc=15.6, scale=1.5, size=num_entries), 1),
    'Price_USD': np.random.normal(loc=1200, scale=400, size=num_entries),
    'Operating_System': np.random.choice(['Windows 10', 'Windows 11', 'macOS', 'Linux'], num_entries),
    'Weight_KG': np.round(np.random.normal(loc=1.8, scale=0.5, size=num_entries), 2),
    'Release_Year': np.random.randint(2018, 2025, num_entries)
}

df = pd.DataFrame(data)

# --- Внесение "сломанных" данных ---

# 1. Пропущенные значения (NaN)
# Примерно 10% в 'RAM_GB'
df.loc[df.sample(frac=0.1).index, 'RAM_GB'] = np.nan
# Примерно 5% в 'Processor'
df.loc[df.sample(frac=0.05).index, 'Processor'] = np.nan
# Примерно 3% в 'Price_USD'
df.loc[df.sample(frac=0.03).index, 'Price_USD'] = np.nan
# Примерно 2% в 'Weight_KG'
df.loc[df.sample(frac=0.02).index, 'Weight_KG'] = np.nan
# Примерно 1% в 'Brand'
df.loc[df.sample(frac=0.01).index, 'Brand'] = np.nan


# 2. Непоследовательные форматы данных
# Некоторые значения 'Screen_Size_Inches' как строки с " дюймами"
random_indices_str_screen = np.random.choice(df.index, size=int(num_entries * 0.07), replace=False)
for idx in random_indices_str_screen:
    df.loc[idx, 'Screen_Size_Inches'] = f"{df.loc[idx, 'Screen_Size_Inches']} inches"

# Некоторые значения 'Storage_GB' как строки с "TB" вместо "GB"
random_indices_tb_storage = np.random.choice(df.index, size=int(num_entries * 0.05), replace=False)
for idx in random_indices_tb_storage:
    if pd.notna(df.loc[idx, 'Storage_GB']): # Убедимся, что это не NaN
        df.loc[idx, 'Storage_GB'] = f"{int(df.loc[idx, 'Storage_GB'] / 1024)}TB"

# Некоторые 'Price_USD' как строки с валютными символами
random_indices_str_price = np.random.choice(df.index, size=int(num_entries * 0.08), replace=False)
for idx in random_indices_str_price:
    if pd.notna(df.loc[idx, 'Price_USD']): # Убедимся, что это не NaN
        df.loc[idx, 'Price_USD'] = f"${df.loc[idx, 'Price_USD']:.2f}"

# Непоследовательные написания ОС
random_indices_os_typo = np.random.choice(df.index, size=int(num_entries * 0.04), replace=False)
for idx in random_indices_os_typo:
    if df.loc[idx, 'Operating_System'] == 'Windows 10':
        df.loc[idx, 'Operating_System'] = 'windows 10'
    elif df.loc[idx, 'Operating_System'] == 'macOS':
        df.loc[idx, 'Operating_System'] = 'Mac OS'

# 3. Выбросы
# Экстремально высокие цены
random_indices_high_price = np.random.choice(df.index, size=int(num_entries * 0.005), replace=False)
for idx in random_indices_high_price:
    df.loc[idx, 'Price_USD'] = np.random.uniform(5000, 10000)

# Экстремально низкие цены (для сломанных, очень старых моделей)
random_indices_low_price = np.random.choice(df.index, size=int(num_entries * 0.005), replace=False)
for idx in random_indices_low_price:
    df.loc[idx, 'Price_USD'] = np.random.uniform(50, 200)

# Неправильные годы выпуска
random_indices_wrong_year = np.random.choice(df.index, size=int(num_entries * 0.005), replace=False)
for idx in random_indices_wrong_year:
    df.loc[idx, 'Release_Year'] = np.random.choice([1995, 2050])

# 4. Дублирующиеся записи
# Создадим 5% дубликатов
duplicate_rows = df.sample(frac=0.05)
df = pd.concat([df, duplicate_rows], ignore_index=True)

# 5. Некорректные типы данных (уже частично сделано с некорректными форматами, но добавим явные ошибки)
# Случайные нечисловые значения в 'RAM_GB' (там, где не NaN)
random_indices_ram_error = np.random.choice(df.index, size=int(num_entries * 0.01), replace=False)
for idx in random_indices_ram_error:
    if pd.notna(df.loc[idx, 'RAM_GB']):
        df.loc[idx, 'RAM_GB'] = random.choice(['eight GB', 'sixteen GB', 'N/A'])


# Перемешаем DataFrame, чтобы дубликаты и ошибки не были подряд
df = df.sample(frac=1).reset_index(drop=True)

# Сохраняем в CSV
df.to_csv(dir_path, index=False)

print(f"Сгенерирован 'сломанный' датасет '{dir_path}' с {len(df)} записями.")
print("\nПервые 5 строк сгенерированного датасета:")
print(df.head())
print("\nИнформация о датасете:")
df.info()
print("\nКоличество пропущенных значений:")
print(df.isnull().sum())
print("\nКоличество дубликатов:")
print(df.duplicated().sum())
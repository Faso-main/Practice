import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from collections import Counter
from imblearn.over_sampling import SMOTE
import joblib # Для сохранения предобработчиков

# 1. Выгрузка данных
print("1. Выгрузка данных")
# Создадим искусственный набор данных для примера
data = {
    'CustomerID': range(1, 1001),
    'Gender': np.random.choice(['Male', 'Female'], 1000),
    'Age': np.random.randint(18, 70, 1000),
    'MonthlyCharges': np.random.uniform(20, 150, 1000),
    'TotalCharges': np.random.uniform(50, 5000, 1000),
    'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], 1000),
    'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], 1000),
    'Churn': np.random.choice([0, 1], 1000, p=[0.7, 0.3]) # 0 - не ушел, 1 - ушел
}
df = pd.DataFrame(data)

# Искусственно добавим пропуски для демонстрации
for col in ['TotalCharges', 'MonthlyCharges']:
    df.loc[df.sample(frac=0.03).index, col] = np.nan
df.loc[df.sample(frac=0.01).index, 'Gender'] = np.nan

# Искусственно добавим выбросы для демонстрации
df.loc[df.sample(frac=0.01).index, 'MonthlyCharges'] = 1500 # Высокий выброс
df.loc[df.sample(frac=0.01).index, 'Age'] = 120 # Неправильный возраст

print("Данные успешно загружены. Первые 5 строк:")
print(df.head())
print("\n")


# 2. Просмотр данных
print("2. Просмотр данных")
print("Информация о данных:")
df.info()
print("\n")


# 3. Статистика по числовым признакам
print("3. Статистика по числовым признакам")
print(df.describe())
print("\n")


# 4. Баланс классов (для целевой переменной)
print("4. Баланс классов")
print(df['Churn'].value_counts(normalize=True))
print("\n")


# 5. Удаление/обработка пропусков
print("5. Удаление/обработка пропусков")
print("Количество пропусков до обработки:")
print(df.isnull().sum())

# Разделяем признаки на числовые и категориальные
numerical_features = df.select_dtypes(include=np.number).columns.tolist()
categorical_features = df.select_dtypes(include='object').columns.tolist()

# Исключаем 'CustomerID' из признаков, если он не является частью модели
if 'CustomerID' in numerical_features:
    numerical_features.remove('CustomerID')

# Для числовых признаков: заполняем медианой (менее чувствительна к выбросам, чем среднее)
imputer_numerical = SimpleImputer(strategy='median')
df[numerical_features] = imputer_numerical.fit_transform(df[numerical_features])

# Для категориальных признаков: заполняем модой
imputer_categorical = SimpleImputer(strategy='most_frequent')
df[categorical_features] = imputer_categorical.fit_transform(df[categorical_features])

print("\nКоличество пропусков после обработки:")
print(df.isnull().sum())
print("\n")


# 6. Обработка выбросов (для числовых признаков)
print("6. Обработка выбросов (числовые признаки)")

# Используем метод IQR (межквартильный размах) для обнаружения и ограничения выбросов
for col in numerical_features:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Ограничиваем значения в пределах IQR
    df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
    df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])

print("Выбросы обработаны. Пример статистики после обработки (MonthlyCharges):")
print(df['MonthlyCharges'].describe())
print("\n")


# 7. Кодирование категориальных признаков
print("7. Кодирование категориальных признаков")

# One-Hot Encoding для номинальных признаков
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
encoded_features = encoder.fit_transform(df[categorical_features])
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))

# Объединяем с исходным DataFrame
df = pd.concat([df.drop(columns=categorical_features), encoded_df], axis=1)

print("Категориальные признаки закодированы. Первые 5 строк после кодирования:")
print(df.head())
print("\n")


# 8. Нормализация/Стандартизация
print("8. Нормализация/Стандартизация")

# Разделяем признаки на X и целевую переменную y
X = df.drop('Churn', axis=1)
y = df['Churn']

# Выбираем числовые признаки для стандартизации (исключаем уже закодированные)
features_to_scale = [col for col in X.columns if col in numerical_features]

scaler = StandardScaler()
X[features_to_scale] = scaler.fit_transform(X[features_to_scale])

print("Числовые признаки стандартизированы. Первые 5 строк X после стандартизации:")
print(X.head())
print("\n")


# 9. Разделение данных на обучающую и тестовую выборки
print("9. Разделение данных")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Размер обучающей выборки X_train: {X_train.shape}")
print(f"Размер тестовой выборки X_test: {X_test.shape}")
print(f"Размер обучающей выборки y_train: {y_train.shape}")
print(f"Размер тестовой выборки y_test: {y_test.shape}")
print("\n")


# 10. Балансировка классов (только для обучающей выборки)
print("10. Балансировка классов")

print(f"Баланс классов в y_train до балансировки: {Counter(y_train)}")

# Используем SMOTE для увеличения миноритарного класса
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

print(f"Баланс классов в y_train после SMOTE: {Counter(y_train_res)}")
print("\n")


# 11. Сохранение предобработчиков
print("11. Сохранение предобработчиков")

# Сохраняем импьютеры, энкодер и скейлер
joblib.dump(imputer_numerical, 'Data_prep/imputer_numerical.pkl')
joblib.dump(imputer_categorical, 'Data_prep/imputer_categorical.pkl')
joblib.dump(encoder, 'Data_prep/onehot_encoder.pkl')
joblib.dump(scaler, 'Data_prep/standard_scaler.pkl')

print("Предобработчики сохранены.")

# Пример загрузки (для использования в продакшене)
# loaded_imputer_numerical = joblib.load('imputer_numerical.pkl')
# loaded_encoder = joblib.load('onehot_encoder.pkl')
# loaded_scaler = joblib.load('standard_scaler.pkl')
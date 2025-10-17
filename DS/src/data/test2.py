from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd
from Main import *

# Выбираем только числовые признаки для начала
numeric_features = df_procuremts.select_dtypes(include=['int64', 'float64']).columns

# Фильтруем категориальные признаки - берем только с разумным количеством уникальных значений
categorical_features = []
for col in df_procuremts.select_dtypes(include=['object']).columns:
    if df_procuremts[col].nunique() <= 50:  # максимум 50 уникальных значений
        categorical_features.append(col)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numeric_features),
        ('cat', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ]), categorical_features)
    ])

X_processed = preprocessor.fit_transform(df_procuremts)
feature_names = preprocessor.get_feature_names_out()
df_processed = pd.DataFrame(X_processed, columns=feature_names)
df_processed.to_csv('src/data/processed_data.csv', index=False)

print(f"Исходный размер: {df_procuremts.shape}")
print(f"После обработки: {df_processed.shape}")
print(f"Числовых признаков: {len(numeric_features)}")
print(f"Категориальных признаков: {len(categorical_features)}")
print(f"Всего признаков после кодирования: {len(feature_names)}")
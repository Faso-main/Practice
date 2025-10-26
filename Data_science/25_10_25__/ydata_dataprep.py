import pandas as pd
import numpy as np
import os
from Main import *

"""
# Import
CSV_PAth=os.path.join('DS','src','data','test.csv')

# Read
data_csv=pd.read_csv(CSV_PAth, on_bad_lines='warn')
"""


R=0;L=1100;STEP=1

data={
    'id':range(R,L),
    'name':[f'name{itr}' for itr in range(R,L,STEP)],
    'age':np.random.choice([itr*5 for itr in range(5,16,STEP)],L),
    'department':np.random.choice([f'department{itr}' for itr in range(R,L,STEP)],L),
    'married':np.random.choice([True,False],L),
    'salary':np.random.choice([itr*100 for itr in range(R,L,STEP)],L)
}

df=pd.DataFrame(data)

# Установка: pip install ydata-profiling
from ydata_profiling import ProfileReport

# Полный автоматический отчет
profile = ProfileReport(df_items, title="Полный EDA Отчет", explorative=True)
profile.to_file("eda_report.html")  # Сохраняет HTML отчет

# Минимальная версия
profile = ProfileReport(df_items, minimal=True)
profile.to_notebook_iframe()  # Показать в Jupyter

print(df.head(3))

"""
# 2. Check for nan
print('_'*100)
print(df.isnull().sum())
print('_'*100)
print(df.isna().sum())
print('_'*100)
print(df.isnull())
"""



"""# 3. Check for duplicates
print(df.duplicated())
for itr in df.columns:
    if itr:
        print(itr,':', df[itr].duplicated().sum())
        print('|'*100)
        
print('-'*100)
print(df.duplicated().sum())
"""
"""
# 1. Inspect
print('_'*100)
print(df.shape)
print('_'*100)
print(df.columns)
print('_'*100)
print(df.dtypes)
print('_'*100)
print(df.describe())
print('_'*100)
print(df.info())
"""
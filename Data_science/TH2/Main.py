import pandas as pd
import numpy as np 
import os


# Configuration
ITEMS_PATH=os.path.join('DS','src','data','344608_СТЕ.csv')
PROCUREMTNS_PATH=os.path.join('DS','src','data','Закупки_TenderHack_20251010.csv')
Proc_Cleaned_PATH=os.path.join('DS','src','data','split.csv')

# ____________________________________________________________________________________________________________________________

# Read data
df_items=pd.read_csv(ITEMS_PATH,on_bad_lines='skip')
df_items.columns=['id_items','specification']
# ____________________________________________________________________________________________________________________________


# Split data
df_items.to_csv(os.path.join('DS','src','data','split.csv'), index=False, encoding='utf-8', chunksize=100)

df_split = df_items['id_items'].str.split(';',expand=True) # разделение с ограничением по количеству строк 
df_split.columns = [f'id{itr}' for itr in range(1, len(df_split.columns)+1,1)]
df_items = pd.concat([df_split, df_items['specification']], axis=1)

df_items.to_csv(os.path.join('DS','src','data','split.csv'), index=False, encoding='utf-8', chunksize=100)
# ____________________________________________________________________________________________________________________________



#df_procuremts=pd.read_excel(os.path.join('DS','src','data','Закупки_TenderHack_20251010.xlsx'))
#df_procuremts.to_csv(PROCUREMTNS_PATH, index=False, encoding='utf-8')

df_procuremts=pd.read_csv(PROCUREMTNS_PATH,on_bad_lines='skip')
df_items=pd.read_csv(Proc_Cleaned_PATH,on_bad_lines='skip')
print(df_procuremts.head())
print(df_items.head())




# Analyze data
#print(df.head(10))
"""
print(df_items.shape)
print(df_items.head(10))
print(df_procuremts.shape)
print(df_procuremts.head(10))
"""

"""
print(df_procuremts.dtypes)
print(df_items.dtypes)
"""


#print(df_procuremts.info())
#print(df_items.info())

#print(df_items.head(10))
#print('_'*100)
#print(df_items.head())


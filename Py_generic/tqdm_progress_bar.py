import time
from tqdm import tqdm, trange


num_border=int(21) 

# 1. Обычный цикл
for itr in tqdm(range(1,num_border,1)): time.sleep(0.1) # задержка

# 2. График работы через готовый метод 'trange'
for itr in trange(1,num_border,1): time.sleep(0.1) # задержка 

# 3. Описание к прогрессу
for itr in tqdm(['abc','acb','bca'],desc='Letter handling'): time.sleep(0.5) # задержка


with tqdm(total=num_border, desc="Выполнение шагов") as pbar:
    for i in range(num_border):
        time.sleep(0.2) # задержка 
        pbar.update(1) # обновление индикатора на 1 шаг


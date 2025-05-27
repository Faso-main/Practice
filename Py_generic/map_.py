"""
Code snippet: map iterator
"""


def my_funс(x): return x*2 # Метод перемножения значений

num_array=[itr for itr in range(1,11,1)] # Array 1-10

hashmap=map(my_funс, num_array) # Пермножение через map

print(f'Result: {hashmap}') # Обычный вывод указывает на итератор
print(f'Result: {list(hashmap)}') # Преобразование сущности в список
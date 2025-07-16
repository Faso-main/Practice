import random

def generate_combinations(itr): return [{random.randint(0, 2):random.randint(0, 2)} for items in range(1,int(itr)+1,1)]

for itr in generate_combinations(6): print(f'Комбинация: {itr}')
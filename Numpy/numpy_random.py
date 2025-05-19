import numpy as np


# Равномерное распределение
uniform = np.random.uniform(0, 1, 5)  # 5 чисел от 0 до 1
print("Равномерное распределение:", uniform)

# Нормальное распределение
normal = np.random.normal(0, 1, 5)  # mean=0, std=1, 5 чисел
print("Нормальное распределение:", normal)

# Случайные целые
integers = np.random.randint(1, 100, 5)  # от 1 до 100, 5 чисел
print("Случайные целые:", integers)
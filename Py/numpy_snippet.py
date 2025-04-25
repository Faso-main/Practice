import numpy as np

# Создание массива из списка
arr1 = np.array([1, 2, 3, 4, 5])
print("Массив из списка:", arr1)

# Создание массива нулей
zeros_arr = np.zeros(5)
print("Массив нулей:", zeros_arr)

# Создание массива единиц
ones_arr = np.ones((2, 3))  # 2 строки, 3 столбца
print("Массив единиц:\n", ones_arr)

# Создание диапазона чисел
range_arr = np.arange(0, 10, 2)  # от 0 до 10 с шагом 2
print("Диапазон чисел:", range_arr)
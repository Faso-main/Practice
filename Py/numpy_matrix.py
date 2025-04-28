import numpy as np


a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Поэлементные операции
print("Сложение:", a + b)      # [5 7 9]
print("Умножение:", a * b)     # [4 10 18]
print("Возведение в степень:", a ** 2)  # [1 4 9]

# Матричное умножение
dot_product = np.dot(a, b)     # 1*4 + 2*5 + 3*6 = 32
print("Скалярное произведение:", dot_product)

arr = np.arange(6)
print("Исходный массив:", arr)  # [0 1 2 3 4 5]

# Изменение формы
reshaped = arr.reshape(2, 3)
print("Массив 2x3:\n", reshaped)
# [[0 1 2]
#  [3 4 5]]

# Преобразование в одномерный
flattened = reshaped.flatten()
print("Снова одномерный:", flattened)  # [0 1 2 3 4 5]

matrix = np.array([[3, 1], [2, 5], [4, 0]])

transposed = matrix.T
print("Транспонированная матрица:\n", transposed)
# [[3 2 4]
#  [1 5 0]]

# Сортировка
sorted_arr = np.sort(matrix, axis=0)  # сортировка по столбцам
print("Отсортированная по столбцам:\n", sorted_arr)
# [[2 0]
#  [3 1]
#  [4 5]]
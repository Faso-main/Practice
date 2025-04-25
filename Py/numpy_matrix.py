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
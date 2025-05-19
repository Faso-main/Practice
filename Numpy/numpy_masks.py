import numpy as np


arr = np.array([1, 2, 3, 4, 5, 6])

# Логические операции
mask = arr > 3
print("Маска (элементы > 3):", mask)  # [False False False True True True]

# Применение маски
print("Элементы > 3:", arr[mask])     # [4 5 6]

# Комбинированные условия
mask = (arr > 2) & (arr < 5)
print("Элементы 2 < x < 5:", arr[mask])  # [3 4]
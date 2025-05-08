import ctypes
"""
Code snippet example of universal, flexible error handling 
"""

def allocate_matrix(rows, cols, initial=0):
    return [[initial] * cols for _ in range(rows)]

matrix = allocate_matrix(2, 3)
matrix_ptr = [matrix]  # "указатель" на матрицу

# Модифицируем через "указатель"
matrix_ptr[0][1][1] = 99
print(matrix)  # [[0, 0, 0], [0, 99, 0]]
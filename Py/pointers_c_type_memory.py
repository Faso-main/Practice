import ctypes
"""
Code snippet example of universal, flexible error handling 
"""

# Выделяем память как в C
buffer = (ctypes.c_int * 3)(1, 2, 3)  # массив из 3 int
ptr = ctypes.pointer(buffer)

# Меняем значения через указатель
ptr[0] = 100
print(buffer[0])  # 100

# Получаем адрес памяти
address = ctypes.addressof(buffer)
print(f"Адрес: {address:#x}")
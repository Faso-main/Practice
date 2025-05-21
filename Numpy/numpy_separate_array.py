import numpy as np


arr = np.array([1, 2, 3, 4, 5])

# Сохранение в файл
np.save('my_array.npy', arr)

# Загрузка из файла
loaded_arr = np.load('my_array.npy')
print("Загруженный массив:", loaded_arr)

# Текстовые файлы
np.savetxt('array.txt', arr, delimiter=',')
loaded_txt = np.loadtxt('array.txt', delimiter=',')
print("Из текстового файла:", loaded_txt)
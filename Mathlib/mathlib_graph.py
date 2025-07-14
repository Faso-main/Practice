import matplotlib.pyplot as plt 
import math 
 
sizes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
times = [1400,2000,2600,2000,2200,2400,1900,2200,2800,2400,2100]  
 

 
plt.plot(sizes, times, marker='o')   
plt.title('Время поиска в зависимости от степени')   
plt.xlabel('Степень')   
plt.ylabel('Время поиска (наносек)')   
plt.grid(True)   
plt.show()
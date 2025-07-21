import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка встроенного набора данных (пример)
tips = sns.load_dataset("tips")

# 1. Точечный график (scatter plot)
plt.figure(figsize=(8, 6))
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time")
plt.title("Зависимость чаевых от суммы счета")
plt.show()

# 2. Гистограмма распределения
plt.figure(figsize=(8, 6))
sns.histplot(data=tips, x="total_bill", bins=20, kde=True)
plt.title("Распределение сумм счетов")
#plt.show()

# 3. Боксплот (boxplot)
plt.figure(figsize=(8, 6))
sns.boxplot(data=tips, x="day", y="total_bill", hue="sex")
plt.title("Распределение счетов по дням и полу")
#plt.show()

# 4. Тепловая карта корреляции
plt.figure(figsize=(8, 6))
corr = tips.corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Тепловая карта корреляции")
#plt.show()
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import matplotlib.lines as lines

# --- Настройка холста ---
fig, ax = plt.subplots(figsize=(14, 8))
# Отключаем оси, так как это не график данных
ax.set_aspect('equal', adjustable='box') # Сохраняем пропорции
ax.axis('off') # Скрываем оси координат

# --- Параметры для рисования фигур (определяются вручную!) ---
task_width = 2.5
task_height = 1.0
event_radius = 0.4
pool_padding = 0.7 # Отступ внутри пула
lane_height = task_height + 2 * pool_padding
pool_vertical_padding = 1.5 # Отступ между пулами
text_padding = 0.1 # Отступ для текста от краев фигур

# --- Определение позиций Пулов и фигур (внимание: все вручную!) ---
# Y-координаты для центров дорожек
pool1_y_center = 6.0
pool2_y_center = pool1_y_center - lane_height - pool_vertical_padding

# X-координаты для центров фигур
start_x = 1.0
task1_x = start_x + event_radius + pool_padding + task_width / 2 # Задача в пуле Врача
task2_x = task1_x + task_width / 2 + pool_padding + task_width / 2 # Задача в пуле Системы
task3_x = task2_x + task_width / 2 + pool_padding + task_width / 2 # Следующая задача в пуле Системы
task4_x = task1_x # Следующая задача в пуле Врача, разместим под первой задачей
end_x = task4_x + task_width/2 + pool_padding + event_radius # Конец в пуле Врача

# Координата для развилки (Шлюз)
gateway_x = task2_x + task_width / 2 + pool_padding + 0.5 # Где-то после task2

# Пересчитываем ширину пула на основе самой правой фигуры
max_x_coord = max(end_x + event_radius, task3_x + task_width/2)
min_x_coord = start_x - event_radius
pool_width = max_x_coord - min_x_coord + 2 * pool_padding # Общая ширина, включая отступы

pool_start_x = min_x_coord - pool_padding


# --- Рисование Пулов (прямоугольники) ---
pool1_rect = patches.Rectangle((pool_start_x, pool1_y_center - lane_height / 2),
                               pool_width, lane_height, linewidth=1, edgecolor='black', facecolor='lightblue', alpha=0.3)
ax.add_patch(pool1_rect)
# Текст названия пула
ax.text(pool_start_x + pool_padding / 2, pool1_y_center, "Медицинский работник (Врач)",
        verticalalignment='center', horizontalalignment='left', rotation=90, fontsize=10, weight='bold')

pool2_rect = patches.Rectangle((pool_start_x, pool2_y_center - lane_height / 2),
                               pool_width, lane_height, linewidth=1, edgecolor='black', facecolor='lightgreen', alpha=0.3)
ax.add_patch(pool2_rect)
# Текст названия пула
ax.text(pool_start_x + pool_padding / 2, pool2_y_center, "Интеллектуальная система",
        verticalalignment='center', horizontalalignment='left', rotation=90, fontsize=10, weight='bold')


# --- Рисование Событий (круги) ---
# Начальное событие (в пуле Врача)
start_event = patches.Circle((start_x, pool1_y_center), event_radius, linewidth=1, edgecolor='black', facecolor='white')
ax.add_patch(start_event)
ax.text(start_x, pool1_y_center, "Начало", ha='center', va='center', fontsize=8)

# Конечное событие (в пуле Врача)
end_event = patches.Circle((end_x, pool1_y_center), event_radius, linewidth=3, edgecolor='black', facecolor='white') # Толще линия для конца
ax.add_patch(end_event)
ax.text(end_x, pool1_y_center, "Конец", ha='center', va='center', fontsize=8)


# --- Рисование Задач (прямоугольники со скругленными углами) ---
# Задача 1: Загрузка/Ввод данных (в пуле Врача)
task1_rect = patches.FancyBboxPatch((task1_x - task_width/2, pool1_y_center - task_height/2), task_width, task_height,
                                   boxstyle="round,pad=0.1, rounding_size=0.2", # Слегка скругленные углы
                                   linewidth=1, edgecolor='black', facecolor='white')
ax.add_patch(task1_rect)
ax.text(task1_x, pool1_y_center, "Загрузка/Ввод\nданных врачом", ha='center', va='center', fontsize=8)

# Задача 2: Анализ данных (в пуле Системы)
task2_rect = patches.FancyBboxPatch((task2_x - task_width/2, pool2_y_center - task_height/2), task_width, task_height,
                                   boxstyle="round,pad=0.1, rounding_size=0.2",
                                   linewidth=1, edgecolor='black', facecolor='white')
ax.add_patch(task2_rect)
ax.text(task2_x, pool2_y_center, "Анализ данных\nсистемой (NLP, EDS)", ha='center', va='center', fontsize=8)

# Задача 3: Формирование отчета (в пуле Системы)
task3_rect = patches.FancyBboxPatch((task3_x - task_width/2, pool2_y_center - task_height/2), task_width, task_height,
                                   boxstyle="round,pad=0.1, rounding_size=0.2",
                                   linewidth=1, edgecolor='black', facecolor='white')
ax.add_patch(task3_rect)
ax.text(task3_x, pool2_y_center, "Формирование\nотчета", ha='center', va='center', fontsize=8)

# Задача 4: Просмотр отчета (в пуле Врача)
task4_rect = patches.FancyBboxPatch((task4_x - task_width/2, pool1_y_center - task_height/2), task_width, task_height,
                                   boxstyle="round,pad=0.1, rounding_size=0.2",
                                   linewidth=1, edgecolor='black', facecolor='white')
ax.add_patch(task4_rect)
ax.text(task4_x, pool1_y_center, "Просмотр и\nоценка отчета", ha='center', va='center', fontsize=8)


# --- Рисование Шлюза (ромб) ---
gateway_y_center = pool2_y_center # В пуле Системы
gateway_size = 1.0 # Размер ромба
gateway_points = [
    (gateway_x, gateway_y_center + gateway_size/2),
    (gateway_x + gateway_size/2, gateway_y_center),
    (gateway_x, gateway_y_center - gateway_size/2),
    (gateway_x - gateway_size/2, gateway_y_center),
    (gateway_x, gateway_y_center + gateway_size/2) # Замкнуть
]
gateway_patch = patches.Polygon(gateway_points, linewidth=1, edgecolor='black', facecolor='white')
ax.add_patch(gateway_patch)
ax.text(gateway_x, gateway_y_center, "X", ha='center', va='center', fontsize=10, weight='bold') # Знак XOR шлюза
ax.text(gateway_x, gateway_y_center - gateway_size/2 - text_padding, "Есть предупреждения?", ha='center', va='top', fontsize=8)


# --- Рисование Потоков (стрелки) ---

# Поток операций (Sequence Flow) - внутри пула Врача
# От Начального события до Задачи 1
arrow1 = patches.FancyArrowPatch((start_x + event_radius, pool1_y_center),
                                 (task1_x - task_width/2, pool1_y_center),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black')
ax.add_patch(arrow1)

# Поток сообщений (Message Flow) - между пулами (пунктирная линия)
# От Задачи 1 (Врач) до Задачи 2 (Система)
# Рисуем от нижней границы Задачи 1 до верхней границы Задачи 2
arrow2 = patches.FancyArrowPatch((task1_x, pool1_y_center - task_height/2),
                                 (task2_x, pool2_y_center + task_height/2),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black', linestyle='--') # Пунктир для Message Flow
ax.add_patch(arrow2)
ax.text((task1_x + task2_x) / 2, (pool1_y_center - task_height/2 + pool2_y_center + task_height/2) / 2,
        "Медицинские данные", ha='center', va='bottom', fontsize=8)


# Поток операций (Sequence Flow) - внутри пула Системы
# От Задачи 2 до Шлюза
arrow3 = patches.FancyArrowPatch((task2_x + task_width/2, pool2_y_center),
                                 (gateway_x - gateway_size/2, gateway_y_center),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black')
ax.add_patch(arrow3)

# От Шлюза - Ветка "Да" (к формированию предупреждений, если это отдельная задача)
# В этом упрощенном примере, пусть предупреждение просто влияет на отчет.
# Сделаем развилку, одна ветка ведет к формированию отчета, другая - через невидимую задачу "Формирование предупреждений" (или просто текст)
# Пропустим явное рисование ветки "Да" для простоты этой демонстрации.
# От Шлюза - Ветка "Нет" (или основная ветка) к Задаче 3
arrow4 = patches.FancyArrowPatch((gateway_x + gateway_size/2, gateway_y_center),
                                 (task3_x - task_width/2, pool2_y_center),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black')
ax.add_patch(arrow4)
ax.text(gateway_x + gateway_size/2 + text_padding, gateway_y_center, "Нет", ha='left', va='center', fontsize=8) # Метка ветки


# Поток операций (Sequence Flow) - внутри пула Системы
# От Задачи 3 до какой-то точки перед отправкой отчета
# (В реальной BPMN может быть слияние после шлюза, но мы упростили)
# Пусть отчет формируется после анализа и проверки
# Нарисуем стрелку от Задачи 3 до точки, откуда выходит Поток сообщений к Врачу
arrow5 = patches.FancyArrowPatch((task3_x + task_width/2, pool2_y_center),
                                 (task3_x + task_width/2 + pool_padding, pool2_y_center), # Просто небольшой сегмент
                                 arrowstyle='-', mutation_scale=20, lw=1, color='black') # Нет стрелки на конце этого сегмента
ax.add_patch(arrow5)


# Поток сообщений (Message Flow) - между пулами (пунктирная линия)
# От Задачи 3 (Система) до Задачи 4 (Врач)
# Рисуем от верхней границы Задачи 3 до нижней границы Задачи 4
arrow6 = patches.FancyArrowPatch((task3_x, pool2_y_center + task_height/2),
                                 (task4_x, pool1_y_center - task_height/2),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black', linestyle='--')
ax.add_patch(arrow6)
ax.text((task3_x + task4_x) / 2, (pool2_y_center + task_height/2 + pool1_y_center - task_height/2) / 2,
        "Отчет с диагнозами и предупреждениями", ha='center', va='bottom', fontsize=8)


# Поток операций (Sequence Flow) - внутри пула Врача
# От Задачи 4 до Конечного события
arrow7 = patches.FancyArrowPatch((task4_x + task_width/2, pool1_y_center),
                                 (end_x - event_radius, pool1_y_center),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black')
ax.add_patch(arrow7)

# --- Рисование Объектов данных (простые прямоугольники) ---
# Объект данных: Медицинские данные (ассоциирован с потоком сообщений 2)
data_input_x = (task1_x + task2_x) / 2
data_input_y = (pool1_y_center - task_height/2 + pool2_y_center + task_height/2) / 2 - task_height/2 # Примерное положение под линией

data_input_rect = patches.Rectangle((data_input_x - task_height/4, data_input_y - task_height/2), task_height/2, task_height, linewidth=1, edgecolor='black', facecolor='white')
ax.add_patch(data_input_rect)
ax.text(data_input_x, data_input_y - task_height/4, "Мед.\nданные", ha='center', va='center', fontsize=7)
# Линии ассоциации (пунктир) - вручную от фигур к объекту данных
ax.add_line(lines.Line2D([task1_x, data_input_x], [pool1_y_center - task_height/2, data_input_y], lw=1, color='black', linestyle=':'))
ax.add_line(lines.Line2D([data_input_x, task2_x], [data_input_y, pool2_y_center + task_height/2], lw=1, color='black', linestyle=':'))


# Объект данных: Отчет (ассоциирован с потоком сообщений 6)
data_output_x = (task3_x + task4_x) / 2
data_output_y = (pool2_y_center + task_height/2 + pool1_y_center - task_height/2) / 2 + task_height/2 # Примерное положение над линией

data_output_rect = patches.Rectangle((data_output_x - task_height/4, data_output_y - task_height/2), task_height/2, task_height, linewidth=1, edgecolor='black', facecolor='white')
ax.add_patch(data_output_rect)
ax.text(data_output_x, data_output_y - task_height/4, "Отчет", ha='center', va='center', fontsize=7)
# Линии ассоциации (пунктир) - вручную от фигур к объекту данных
ax.add_line(lines.Line2D([task3_x, data_output_x], [pool2_y_center + task_height/2, data_output_y - task_height/2], lw=1, color='black', linestyle=':'))
ax.add_line(lines.Line2D([data_output_x, task4_x], [data_output_y - task_height/2, pool1_y_center - task_height/2], lw=1, color='black', linestyle=':'))


# --- Установка пределов осей для отображения всех элементов ---
# Рассчитываем пределы с учетом всех фигур и их размеров
min_x = pool_start_x - pool_padding # Левая граница пула с отступом
max_x = pool_start_x + pool_width + pool_padding # Правая граница пула с отступом
min_y = pool2_y_center - lane_height / 2 - pool_padding # Нижняя граница нижнего пула с отступом
max_y = pool1_y_center + lane_height / 2 + pool_padding # Верхняя граница верхнего пула с отступом

ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)


# --- Заголовок диаграммы ---
plt.title("Упрощенная BPMN диаграмма: Врач и ИИ-система поддержки диагностики")

# --- Отображение диаграммы ---
plt.show()
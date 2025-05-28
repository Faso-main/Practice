import tkinter as tk
from tkinter import colorchooser, simpledialog, messagebox
import numpy as np
import math
from PIL import Image, ImageTk # Убедитесь, что Pillow установлен: pip install Pillow

# Класс для точки (пиксельные координаты)
class Point:
    def __init__(self, x, y):
        self.x = int(round(x)) # Координаты целые
        self.y = int(round(y))

    def to_homogeneous(self):
        # В однородные координаты для матричных операций
        return np.array([self.x, self.y, 1])

    @staticmethod
    def from_homogeneous(matrix):
        # Из однородных координат обратно в обычные
        if matrix.shape == (3,): # Если это вектор
            if matrix[2] != 0:
                return Point(matrix[0] / matrix[2], matrix[1] / matrix[2])
            else:
                return Point(matrix[0], matrix[1])
        elif matrix.shape == (1, 3): # Если это строка матрицы
            if matrix[0, 2] != 0:
                return Point(matrix[0, 0] / matrix[0, 2], matrix[0, 1] / matrix[0, 2])
            else:
                return Point(matrix[0, 0], matrix[0, 1])
        else:
            raise ValueError("Неожиданная форма матрицы для преобразования")


# Базовый класс для всех фигур
class GraphicObject:
    def __init__(self, color="#000000", fill_color="#01FF417E"):
        self.points = []
        self.color = color # Цвет контура
        self.fill_color = fill_color # Цвет заливки
        self.id = None # Не используется для пиксельной отрисовки напрямую
        self.center = Point(0, 0) # Центр фигуры
        self.calculate_center() # Определяем центр при создании

    def draw(self, editor_instance):
        # Должен быть переопределен в дочерних классах
        raise NotImplementedError

    def apply_transform(self, transform_matrix):
        # Применяем матрицу преобразования ко всем точкам
        new_points_homogeneous = []
        for p in self.points:
            hom_coords = p.to_homogeneous()
            transformed_hom_coords = np.dot(hom_coords, transform_matrix)
            new_points_homogeneous.append(Point.from_homogeneous(transformed_hom_coords))
        self.points = new_points_homogeneous
        # Пересчитываем центр после преобразования
        self.calculate_center()

    def calculate_center(self):
        # Вычисление центра объекта
        if not self.points:
            self.center = Point(0, 0)
            return

        sum_x = sum(p.x for p in self.points)
        sum_y = sum(p.y for p in self.points)
        self.center = Point(sum_x / len(self.points), sum_y / len(self.points))


# Линия (отрезок)
class Line(GraphicObject):
    def __init__(self, p1, p2, color="#000000"):
        super().__init__(color=color)
        self.points = [p1, p2]
        self.calculate_center()

    def draw(self, editor_instance):
        # Рисуем линию алгоритмом Брезенхэма
        editor_instance.bresenham_line(self.points[0], self.points[1], self.color)


# Крест (Kr)
class Cross(GraphicObject):
    def __init__(self, center_x, center_y, size, color="#000000", fill_color="#01FF417E"): 
        super().__init__(color=color, fill_color=fill_color)
        half_size = size / 2
        quarter_size = size / 4
        # Задаем точки для многоугольника, образующего крест
        self.points = [
            Point(center_x - quarter_size, center_y - half_size),
            Point(center_x + quarter_size, center_y - half_size),
            Point(center_x + quarter_size, center_y - quarter_size),
            Point(center_x + half_size, center_y - quarter_size),
            Point(center_x + half_size, center_y + quarter_size),
            Point(center_x + quarter_size, center_y + quarter_size),
            Point(center_x + quarter_size, center_y + half_size),
            Point(center_x - quarter_size, center_y + half_size),
            Point(center_x - quarter_size, center_y + quarter_size),
            Point(center_x - half_size, center_y + quarter_size),
            Point(center_x - half_size, center_y - quarter_size),
            Point(center_x - quarter_size, center_y - quarter_size)
        ]
        self.calculate_center()

    def draw(self, editor_instance):
        # Заливаем и рисуем контур с помощью Scanline
        editor_instance.scanline_fill(self.points, self.color, self.fill_color)


# Флаг (Flag)
class Flag(GraphicObject):
    def __init__(self, base_x, base_y, width, height, color="#000000", fill_color="#01FF417E"):
        super().__init__(color=color, fill_color=fill_color)
        # Задаем точки для многоугольника, образующего флаг
        self.points = [
            Point(base_x, base_y),
            Point(base_x, base_y - height),
            Point(base_x + width, base_y - height),
            Point(base_x + width, base_y - height / 2),
            Point(base_x, base_y - height / 2)
        ]
        self.calculate_center()

    def draw(self, editor_instance):
        # Заливаем и рисуем контур с помощью Scanline
        editor_instance.scanline_fill(self.points, self.color, self.fill_color)


# Класс для матричных преобразований
class Transformations:
    @staticmethod
    def translation_matrix(dx, dy):
        # Матрица для перемещения
        return np.array([
            [1, 0, 0],
            [0, 1, 0],
            [dx, dy, 1]
        ])

    @staticmethod
    def rotation_matrix(angle_degrees):
        # Матрица для поворота
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return np.array([
            [cos_a, sin_a, 0],
            [-sin_a, cos_a, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def scale_matrix(sx, sy):
        # Матрица для масштабирования
        return np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def mirror_x_axis_matrix():
        # Матрица для отражения по оси X
        return np.array([
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def mirror_y_axis_matrix():
        # Матрица для отражения по оси Y
        return np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def rotate_around_point(obj, angle_degrees, center_x, center_y):
        # Поворот объекта вокруг произвольной точки
        T1 = Transformations.translation_matrix(-center_x, -center_y)
        R = Transformations.rotation_matrix(angle_degrees)
        T2 = Transformations.translation_matrix(center_x, center_y)
        transform_matrix = np.dot(np.dot(T1, R), T2)
        obj.apply_transform(transform_matrix)

    @staticmethod
    def mirror_around_figure_center(obj):
        # Отражение относительно центра фигуры
        if not obj.center:
            obj.calculate_center()
        cx, cy = obj.center.x, obj.center.y

        T1 = Transformations.translation_matrix(-cx, -cy)
        M = Transformations.scale_matrix(-1, -1) # Отражение = масштабирование на -1
        T2 = Transformations.translation_matrix(cx, cy)
        transform_matrix = np.dot(np.dot(T1, M), T2)
        obj.apply_transform(transform_matrix)

    @staticmethod
    def mirror_vertical_line(obj, line_x):
        # Отражение относительно вертикальной линии
        T1 = Transformations.translation_matrix(-line_x, 0)
        M_y = Transformations.mirror_y_axis_matrix()
        T2 = Transformations.translation_matrix(line_x, 0)
        transform_matrix = np.dot(np.dot(T1, M_y), T2)
        obj.apply_transform(transform_matrix)

    @staticmethod
    def translate(obj, dx, dy):
        # Перемещение объекта
        T = Transformations.translation_matrix(dx, dy)
        obj.apply_transform(T)


# Класс для Теоретико-множественных операций (ТМО)
class SetOperations:
    @staticmethod
    def intersection(obj1, obj2):
        messagebox.showinfo("ТМО: Пересечение", "Пересечение многоугольников не реализовано.")
        return None

    @staticmethod
    def difference(obj1, obj2):
        messagebox.showinfo("ТМО: Разность", "Разность многоугольников не реализована.")
        return None


class GraphicEditor:
    def __init__(self, master):
        self.master = master
        master.title("Графический редактор (Вариант 70)")

        self.current_color = "#000000" # Цвет по умолчанию для контура
        self.current_fill_color = "#01FF417E" # Цвет по умолчанию для заливки
        self.objects = [] # Список всех объектов на холсте
        self.selected_object = None # Выбранный объект
        self.drawing_primitive = None # Текущий режим рисования
        self.temp_points = [] # Временные точки для рисования
        self.temp_line_id = None # ID временной линии (для трансформаций)
        self.transform_center_marker_id = None # ID маркера центра трансформации
        self.current_transformation_mode = None # Текущий режим трансформации

        self.canvas_width = 1400
        self.canvas_height = 600
        # Холст Tkinter
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white", borderwidth=2, relief="groove")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Массив пикселей для ручной отрисовки (белый по умолчанию)
        self.pixels = np.full((self.canvas_height, self.canvas_width, 3), 255, dtype=np.uint8)
        # Объект PhotoImage для отображения на холсте
        self.photo_image = ImageTk.PhotoImage(Image.fromarray(self.pixels))
        self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)


        self.create_menu() # Создаем меню
        self.create_toolbar() # Создаем панель инструментов

        # Привязываем события мыши
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.dragging_object = False # Флаг перетаскивания объекта

    def create_menu(self):
        # Создание главного меню
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выход", command=self.master.quit)

        # Меню "Редактировать"
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Редактировать", menu=edit_menu)
        edit_menu.add_command(label="Выбрать объект", command=self.select_object_mode)
        edit_menu.add_command(label="Удалить выбранный", command=self.delete_selected_object)

        # Меню "Примитивы"
        primitives_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Примитивы", menu=primitives_menu)
        primitives_menu.add_command(label="Отрезок", command=lambda: self.start_drawing("line"))
        primitives_menu.add_command(label="Крест (Kr)", command=lambda: self.start_drawing("cross"))
        primitives_menu.add_command(label="Флаг (Flag)", command=lambda: self.start_drawing("flag"))

        # Меню "ТМО" (Теоретико-множественные операции)
        tmo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ТМО", menu=tmo_menu)
        tmo_menu.add_command(label="Пересечение ()", command=self.perform_intersection)
        tmo_menu.add_command(label="Разность ()", command=self.perform_difference)

        # Меню "Преобразования"
        transform_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Преобразования", menu=transform_menu)
        transform_menu.add_command(label="Перемещение", command=self.start_translation)
        transform_menu.add_command(label="Поворот (Rc)", command=self.start_rotation_around_point)
        transform_menu.add_command(label="Зеркальное отражение относительно центра фигуры (Mf)", command=self.mirror_around_figure_center)
        transform_menu.add_command(label="Зеркальное отражение относительно вертикальной прямой (MV)", command=self.start_mirror_vertical_line)

        # Меню "Цвет"
        color_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Цвет", menu=color_menu)
        color_menu.add_command(label="Цвет обводки", command=self.choose_outline_color)
        color_menu.add_command(label="Цвет заливки", command=self.choose_fill_color)

        # Меню "Помощь"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def create_toolbar(self):
        # Создание панели инструментов
        toolbar = tk.Frame(self.master, bd=2, relief=tk.RAISED)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Кнопки на панели инструментов
        tk.Button(toolbar, text="Отрезок", command=lambda: self.start_drawing("line")).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Крест", command=lambda: self.start_drawing("cross")).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Флаг", command=lambda: self.start_drawing("flag")).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Выбрать", command=self.select_object_mode).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Удалить", command=self.delete_selected_object).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Перемещение", command=self.start_translation).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Поворот Rc", command=self.start_rotation_around_point).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Отражение Mf", command=self.mirror_around_figure_center).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Отражение MV", command=self.start_mirror_vertical_line).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Цвет обводки", command=self.choose_outline_color).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Цвет заливки", command=self.choose_fill_color).pack(side=tk.LEFT, padx=2, pady=2)

    def hex_to_rgb(self, hex_color):
        # Преобразование шестнадцатеричного цвета в RGB
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def choose_outline_color(self):
        # Выбор цвета контура
        color_info = colorchooser.askcolor(title="Выбрать цвет обводки")
        if color_info[1]:
            self.current_color = color_info[1]
            if self.selected_object:
                self.selected_object.color = self.current_color
                self.redraw_all_objects()

    def choose_fill_color(self):
        # Выбор цвета заливки
        color_info = colorchooser.askcolor(title="Выбрать цвет заливки")
        if color_info[1]:
            self.current_fill_color = color_info[1]
            if self.selected_object and hasattr(self.selected_object, 'fill_color'):
                self.selected_object.fill_color = self.current_fill_color
                self.redraw_all_objects()

    def show_about(self):
        # Информация о программе
        messagebox.showinfo("О программе", "Графический редактор. Вариант 70.\nРазработано в рамках курсовой работы по дисциплине \"Графические системы компьютеров\".")

    def start_drawing(self, primitive_type):
        # Переключение в режим рисования примитива
        self.drawing_primitive = primitive_type
        self.temp_points = []
        self.selected_object = None
        self.canvas.config(cursor="cross")
        self.clear_transform_marker()
        self.clear_temp_line()
        self.current_transformation_mode = None
        self.redraw_all_objects()

    def select_object_mode(self):
        # Переключение в режим выбора объекта
        self.drawing_primitive = None
        self.canvas.config(cursor="arrow")
        self.clear_transform_marker()
        self.clear_temp_line()
        self.current_transformation_mode = None
        self.redraw_all_objects()

    def delete_selected_object(self):
        # Удаление выбранного объекта
        if self.selected_object:
            self.objects.remove(self.selected_object)
            self.selected_object = None
            self.clear_transform_marker()
            self.redraw_all_objects()

    def on_canvas_click(self, event):
        # Обработка клика по холсту
        if self.drawing_primitive:
            self.temp_points.append(Point(event.x, event.y))
            if self.drawing_primitive == "line":
                if len(self.temp_points) == 2:
                    line = Line(self.temp_points[0], self.temp_points[1], self.current_color)
                    self.objects.append(line)
                    self.drawing_primitive = None
                    self.canvas.config(cursor="arrow")
                    self.selected_object = line
                    self.redraw_all_objects()
            elif self.drawing_primitive == "cross":
                if len(self.temp_points) == 2:
                    center_x, center_y = self.temp_points[0].x, self.temp_points[0].y
                    size = math.sqrt((event.x - center_x)**2 + (event.y - center_y)**2) * 2
                    cross = Cross(center_x, center_y, size, self.current_color, self.current_fill_color)
                    self.objects.append(cross)
                    self.drawing_primitive = None
                    self.canvas.config(cursor="arrow")
                    self.selected_object = cross
                    self.redraw_all_objects()
            elif self.drawing_primitive == "flag":
                if len(self.temp_points) == 2:
                    x1, y1 = self.temp_points[0].x, self.temp_points[0].y
                    x2, y2 = self.temp_points[1].x, self.temp_points[1].y
                    width = abs(x2 - x1)
                    height = abs(y2 - y1)
                    flag = Flag(min(x1, x2), max(y1, y2), width, height, self.current_color, self.current_fill_color)
                    self.objects.append(flag)
                    self.drawing_primitive = None
                    self.canvas.config(cursor="arrow")
                    self.selected_object = flag
                    self.redraw_all_objects()

        elif self.current_transformation_mode == "rotation_around_point":
            # Устанавливаем центр вращения и запрашиваем угол
            self.transform_center = Point(event.x, event.y)
            self.draw_transform_marker(self.transform_center.x, self.transform_center.y, "#FF0000")
            angle = simpledialog.askfloat("Поворот", "Введите угол поворота (градусы):")
            if angle is not None and self.selected_object:
                Transformations.rotate_around_point(self.selected_object, angle, self.transform_center.x, self.transform_center.y)
                self.redraw_all_objects()
            self.current_transformation_mode = None
            self.clear_transform_marker()
            self.canvas.config(cursor="arrow")
        elif self.current_transformation_mode == "mirror_vertical_line":
            # Устанавливаем линию отражения
            self.mirror_line_x = event.x
            self.draw_temp_vertical_line(self.mirror_line_x)
            if self.selected_object:
                Transformations.mirror_vertical_line(self.selected_object, self.mirror_line_x)
                self.redraw_all_objects()
            self.current_transformation_mode = None
            self.clear_temp_line()
            self.canvas.config(cursor="arrow")
        elif self.current_transformation_mode == "translation" and self.selected_object:
            # Начало перетаскивания для перемещения
            self.start_drag_x = event.x
            self.start_drag_y = event.y
            self.dragging_object = True
        else:
            # Режим выбора объекта
            self.select_object_at_click(event.x, event.y)

    def on_canvas_drag(self, event):
        # Обработка перетаскивания мышью (для перемещения)
        if self.dragging_object and self.selected_object and self.current_transformation_mode == "translation":
            dx = event.x - self.start_drag_x
            dy = event.y - self.start_drag_y
            Transformations.translate(self.selected_object, dx, dy)
            self.start_drag_x = event.x
            self.start_drag_y = event.y
            self.redraw_all_objects()

    def on_canvas_release(self, event):
        # Завершение перетаскивания
        self.dragging_object = False
        if self.current_transformation_mode == "translation":
            self.canvas.config(cursor="arrow")
            self.current_transformation_mode = None

    def select_object_at_click(self, x, y):
        # Выбор объекта по клику
        selected_by_area = None
        # Проверяем многоугольники (крест, флаг) по попаданию в область
        for obj in reversed(self.objects): # Сверху вниз
            if isinstance(obj, (Cross, Flag)):
                if self.is_point_in_polygon(Point(x, y), obj.points):
                    selected_by_area = obj
                    break
        
        if selected_by_area:
            self.selected_object = selected_by_area
        else:
            # Для линий ищем ближайшую
            min_dist = float('inf')
            closest_line = None
            for obj in self.objects:
                if isinstance(obj, Line):
                    p1 = obj.points[0]
                    p2 = obj.points[1]
                    dist = self.point_line_distance(Point(x, y), p1, p2)
                    if dist < min_dist and dist < 5: # Если близко к линии
                        min_dist = dist
                        closest_line = obj
            self.selected_object = closest_line

        self.redraw_all_objects()

    def point_line_distance(self, pt, p1, p2):
        # Расстояние от точки до отрезка
        x0, y0 = pt.x, pt.y
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y

        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0: # Если отрезок - это точка
            return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)

        # Проекция точки на прямую
        t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)

        if t < 0: # Вне отрезка, ближе к p1
            closest_x, closest_y = x1, y1
        elif t > 1: # Вне отрезка, ближе к p2
            closest_x, closest_y = x2, y2
        else: # На отрезке
            closest_x = x1 + t * dx
            closest_y = y1 + t * dy

        return math.sqrt((x0 - closest_x)**2 + (y0 - closest_y)**2)

    def is_point_in_polygon(self, pt, poly_points):
        # Проверка, находится ли точка внутри многоугольника (алгоритм "луч")
        x, y = pt.x, pt.y
        n = len(poly_points)
        inside = False

        if n < 3: # Не многоугольник
            return False

        p1x, p1y = poly_points[0].x, poly_points[0].y
        for i in range(n + 1):
            p2x, p2y = poly_points[i % n].x, poly_points[i % n].y
            if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside
            p1x, p1y = p2x, p2y
        return inside


    def highlight_selected_object(self):
        # Маркер центра фигуры (устаревший, теперь рисуется в redraw_all_objects)
        if self.selected_object and self.selected_object.center:
            self.draw_transform_marker(self.selected_object.center.x, self.selected_object.center.y, "#00FF00")

    def redraw_all_objects(self):
        # Перерисовка всего холста
        self.pixels.fill(255) # Очищаем пиксели (белый фон)

        # Отрисовываем все объекты
        for obj in self.objects:
            obj.draw(self)

        # Дополнительная отрисовка выделения для выбранного объекта
        if self.selected_object:
            if isinstance(self.selected_object, Line):
                self.bresenham_line(self.selected_object.points[0], self.selected_object.points[1], "#FF0000", width=3)
            elif isinstance(self.selected_object, (Cross, Flag)):
                points = self.selected_object.points
                n = len(points)
                for i in range(n):
                    p1 = points[i]
                    p2 = points[(i + 1) % n]
                    self.bresenham_line(p1, p2, "#FF0000", width=5)
        
        # Обновляем изображение на Canvas
        self.update_canvas_image()
        
        # Рисуем маркеры поверх (потому что они относятся к интерактиву, а не к содержимому пикселей)
        self.clear_transform_marker()
        if self.current_transformation_mode == "rotation_around_point" and hasattr(self, 'transform_center'):
            self.draw_transform_marker(self.transform_center.x, self.transform_center.y, "#FF0000")
        elif self.current_transformation_mode == "mirror_vertical_line" and hasattr(self, 'mirror_line_x'):
            self.draw_temp_vertical_line(self.mirror_line_x)
        
        # Если объект выбран, рисуем его центр
        if self.selected_object and self.selected_object.center:
            self.draw_transform_marker(self.selected_object.center.x, self.selected_object.center.y, "#FF0000")

    def put_pixel(self, x, y, color_hex, width=1):
        # Установка пикселя (с учетом толщины)
        r, g, b = self.hex_to_rgb(color_hex)
        x = int(round(x))
        y = int(round(y))

        # Рисуем квадрат из пикселей для имитации толщины
        for dy_offset in range(-width // 2, width - width // 2):
            for dx_offset in range(-width // 2, width - width // 2):
                px, py = x + dx_offset, y + dy_offset
                if 0 <= py < self.canvas_height and 0 <= px < self.canvas_width:
                    self.pixels[py, px] = [r, g, b]


    def update_canvas_image(self):
        # Обновление отображения пикселей на холсте
        self.photo_image = ImageTk.PhotoImage(image=Image.fromarray(self.pixels))
        self.canvas.itemconfig(self.image_item, image=self.photo_image)


    # Алгоритм Брезенхэма для отрисовки линии
    def bresenham_line(self, p1, p2, color, width=1):
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.put_pixel(x1, y1, color, width)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    # Алгоритм Scanline для закрашивания полигона
    def scanline_fill(self, points, outline_color, fill_color):
        if not points:
            return

        min_y = min(p.y for p in points)
        max_y = max(p.y for p in points)

        edges = [] # Список активных ребер
        n = len(points)
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]
            
            if p1.y == p2.y: # Горизонтальные ребра пропускаем
                continue

            if p1.y > p2.y: # Ребро должно идти снизу вверх
                p1, p2 = p2, p1

            # Добавляем ребро: [ymin, ymax, x_на_ymin, 1/m (dx/dy)]
            edges.append([p1.y, p2.y, p1.x, (p2.x - p1.x) / (p2.y - p1.y)])

        for y in range(min_y, max_y + 1):
            intersections = [] # Точки пересечения текущей строки развертки
            for edge in edges:
                ymin, ymax, x_curr, inv_slope = edge
                if ymin <= y < ymax:
                    # Вычисляем x на текущей строке развертки
                    current_x = x_curr + inv_slope * (y - ymin)
                    intersections.append(current_x)
            
            intersections.sort() # Сортируем точки пересечения

            for i in range(0, len(intersections), 2): # Заливаем попарно
                if i + 1 < len(intersections):
                    x_start = int(round(intersections[i]))
                    x_end = int(round(intersections[i+1]))
                    for x in range(x_start, x_end + 1):
                        self.put_pixel(x, y, fill_color)

        # Рисуем контур (обводку) поверх заливки
        for i in range(n):
            self.bresenham_line(points[i], points[(i + 1) % n], outline_color)


    def clear_transform_marker(self):
        # Удаление маркера центра трансформации (Canvas-объекта)
        if self.transform_center_marker_id:
            self.canvas.delete(self.transform_center_marker_id)
            self.transform_center_marker_id = None

    def draw_transform_marker(self, x, y, color_hex):
        # Рисование маркера центра трансформации (крестик и круг)
        marker_size = 5

        # Круг (множество пикселей по окружности)
        for angle in np.linspace(0, 2 * np.pi, 30):
            mx = x + marker_size * math.cos(angle)
            my = y + marker_size * math.sin(angle)
            self.put_pixel(mx, my, color_hex)

        # Крест (две линии)
        self.bresenham_line(Point(x - marker_size * 2, y), Point(x + marker_size * 2, y), color_hex)
        self.bresenham_line(Point(x, y - marker_size * 2), Point(x, y + marker_size * 2), color_hex)

    def perform_intersection(self):
        # Сообщение о нереализованной ТМО
        messagebox.showinfo("ТМО: Пересечение", "Пересечение сложных многоугольников не реализовано.")
        return None

    def perform_difference(self):
        # Сообщение о нереализованной ТМО
        messagebox.showinfo("ТМО: Разность", "Разность сложных многоугольников не реализована.")
        return None

    # Геометрические преобразования
    def start_translation(self):
        # Начать перемещение
        if not self.selected_object:
            messagebox.showwarning("Ошибка", "Сначала выберите объект для перемещения.")
            return
        self.current_transformation_mode = "translation"
        messagebox.showinfo("Перемещение", "Переместите объект, перетаскивая его мышью.")
        self.canvas.config(cursor="fleur")

    def start_rotation_around_point(self):
        # Начать поворот вокруг точки
        if not self.selected_object:
            messagebox.showwarning("Ошибка", "Сначала выберите объект для поворота.")
            return
        self.current_transformation_mode = "rotation_around_point"
        messagebox.showinfo("Поворот (Rc)", "Кликните на холсте, чтобы задать центр поворота.")
        self.canvas.config(cursor="dotbox")

    def mirror_around_figure_center(self):
        # Отражение относительно центра фигуры
        if not self.selected_object:
            messagebox.showwarning("Ошибка", "Сначала выберите объект для отражения.")
            return
        Transformations.mirror_around_figure_center(self.selected_object)
        self.redraw_all_objects()

    def start_mirror_vertical_line(self):
        # Начать отражение относительно вертикальной линии
        if not self.selected_object:
            messagebox.showwarning("Ошибка", "Сначала выберите объект для отражения.")
            return
        self.current_transformation_mode = "mirror_vertical_line"
        messagebox.showinfo("Зеркальное отражение (MV)", "Кликните на холсте, чтобы задать вертикальную линию отражения.")
        self.canvas.config(cursor="sb_v_double_arrow")

    def draw_temp_vertical_line(self, x):
        # Рисование временной вертикальной линии (для MV)
        self.clear_temp_line()
        self.temp_line_id = self.canvas.create_line(x, 0, x, self.canvas.winfo_height(), fill="red", dash=(4, 4))

    def clear_temp_line(self):
        # Удаление временной линии
        if self.temp_line_id:
            self.canvas.delete(self.temp_line_id)
            self.temp_line_id = None


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicEditor(root)
    root.mainloop()
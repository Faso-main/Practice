import tkinter as tk
from tkinter import colorchooser, simpledialog, messagebox
import numpy as np
import math

# Класс для представления точки
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_homogeneous(self):
        # Преобразуем точку в numpy-массив для матричных операций (добавляем 1 для однородных координат)
        return np.array([self.x, self.y, 1])

    @staticmethod
    def from_homogeneous(matrix):
        # Обратное преобразование из однородных координат
        # Делим на последний элемент, если он не 1 (для масштабирования в однородных координатах)
        if matrix[0, 2] != 0:
            return Point(matrix[0, 0] / matrix[0, 2], matrix[0, 1] / matrix[0, 2])
        else:
            # Обработка случая, когда z-координата равна 0 (может указывать на бесконечность или ошибку)
            return Point(matrix[0, 0], matrix[0, 1])


# Базовый класс для всех графических объектов
class GraphicObject:
    def __init__(self, color="black", fill_color="blue"):
        self.points = []
        self.color = color
        self.fill_color = fill_color
        self.id = None # ID объекта на холсте tkinter
        self.center = Point(0, 0) # Центр фигуры
        self.calculate_center() # Вызываем для инициализации центра

    def draw(self, canvas):
        raise NotImplementedError

    def apply_transform(self, transform_matrix):
        # Применение преобразования к каждой точке объекта
        new_points_homogeneous = []
        for p in self.points:
            hom_coords = p.to_homogeneous()
            # Умножение матрицы преобразования на вектор-строку точки
            transformed_hom_coords = np.dot(hom_coords, transform_matrix)
            new_points_homogeneous.append(Point.from_homogeneous(transformed_hom_coords.reshape(1, 3)))
        self.points = new_points_homogeneous
        # Пересчет центра фигуры после преобразования
        self.calculate_center()

    def calculate_center(self):
        if not self.points:
            self.center = Point(0, 0)
            return

        sum_x = sum(p.x for p in self.points)
        sum_y = sum(p.y for p in self.points)
        self.center = Point(sum_x / len(self.points), sum_y / len(self.points))


# Примитивы для Варианта 70
class Line(GraphicObject):
    def __init__(self, p1, p2, color="black"):
        super().__init__(color=color)
        self.points = [p1, p2]
        self.calculate_center()

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        self.id = canvas.create_line(self.points[0].x, self.points[0].y,
                                      self.points[1].x, self.points[1].y,
                                      fill=self.color, width=2)

class Cross(GraphicObject): # Kr
    def __init__(self, center_x, center_y, size, color="black", fill_color="blue"):
        super().__init__(color=color, fill_color=fill_color)
        # Примерные координаты креста
        half_size = size / 2
        quarter_size = size / 4
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

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        coords = []
        for p in self.points:
            coords.extend([p.x, p.y])
        self.id = canvas.create_polygon(coords, outline=self.color, fill=self.fill_color, width=2)


class Flag(GraphicObject): # Flag
    def __init__(self, base_x, base_y, width, height, color="black", fill_color="blue"):
        super().__init__(color=color, fill_color=fill_color)
        # Примерные координаты флага
        self.points = [
            Point(base_x, base_y),
            Point(base_x, base_y - height),
            Point(base_x + width, base_y - height),
            Point(base_x + width, base_y - height / 2),
            Point(base_x, base_y - height / 2)
        ]
        self.calculate_center()

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        coords = []
        for p in self.points:
            coords.extend([p.x, p.y])
        self.id = canvas.create_polygon(coords, outline=self.color, fill=self.fill_color, width=2)


# Класс для матричных преобразований
class Transformations:
    @staticmethod
    def translation_matrix(dx, dy):
        return np.array([
            [1, 0, 0],
            [0, 1, 0],
            [dx, dy, 1]
        ])

    @staticmethod
    def rotation_matrix(angle_degrees):
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
        return np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def mirror_x_axis_matrix():
        return np.array([
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def mirror_y_axis_matrix():
        return np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])

    # Rc - Поворот вокруг заданного центра на произвольный угол
    @staticmethod
    def rotate_around_point(obj, angle_degrees, center_x, center_y):
        T1 = Transformations.translation_matrix(-center_x, -center_y)
        R = Transformations.rotation_matrix(angle_degrees)
        T2 = Transformations.translation_matrix(center_x, center_y)
        transform_matrix = np.dot(np.dot(T1, R), T2) # Порядок умножения матриц важен!
        obj.apply_transform(transform_matrix)

    # Mf - Зеркальное отражение относительно центра фигуры
    @staticmethod
    def mirror_around_figure_center(obj):
        if not obj.center:
            obj.calculate_center()
        cx, cy = obj.center.x, obj.center.y

        # Перемещаем центр фигуры в начало координат
        T1 = Transformations.translation_matrix(-cx, -cy)
        # Отражаем относительно начала координат (например, относительно Y-оси, проходящей через центр)
        # Чтобы отразить относительно центра, можно использовать масштаб -1 по обеим осям
        M = Transformations.scale_matrix(-1, -1)
        # Возвращаем на место
        T2 = Transformations.translation_matrix(cx, cy)
        transform_matrix = np.dot(np.dot(T1, M), T2)
        obj.apply_transform(transform_matrix)


    # MV - Зеркальное отражение относительно вертикальной прямой
    @staticmethod
    def mirror_vertical_line(obj, line_x):
        T1 = Transformations.translation_matrix(-line_x, 0)
        M_y = Transformations.mirror_y_axis_matrix() # Отражение относительно Y-оси (которая теперь является линией x=line_x)
        T2 = Transformations.translation_matrix(line_x, 0)
        transform_matrix = np.dot(np.dot(T1, M_y), T2)
        obj.apply_transform(transform_matrix)

    # Плоскопараллельное перемещение (обязательное)
    @staticmethod
    def translate(obj, dx, dy):
        T = Transformations.translation_matrix(dx, dy)
        obj.apply_transform(T)


# Класс для Теоретико-множественных операций (ТМО)
class SetOperations:
    #  - Пересечение
    @staticmethod
    def intersection(obj1, obj2):
        messagebox.showinfo("ТМО: Пересечение", "Реализация пересечения сложных многоугольников требует продвинутых алгоритмов (например, Сазерленнда-Ходжмана). В данной версии не реализовано.")
        return None

    #  - Разность
    @staticmethod
    def difference(obj1, obj2):
        messagebox.showinfo("ТМО: Разность", "Реализация разности сложных многоугольников требует продвинутых алгоритмов. В данной версии не реализовано.")
        return None


class GraphicEditor:
    def __init__(self, master):
        self.master = master
        master.title("Графический редактор (Вариант 70)")

        self.current_color = "black"
        self.current_fill_color = "blue"
        self.objects = []
        self.selected_object = None
        self.drawing_primitive = None # Текущий примитив, который рисуется
        self.temp_points = [] # Временные точки для интерактивного рисования
        self.temp_line_id = None # ID для временной линии (для отражения относительно прямой)
        self.transform_center_marker_id = None # ID для маркера центра преобразования
        self.current_transformation_mode = None # Для отслеживания текущего режима трансформации

        self.canvas = tk.Canvas(master, width=800, height=600, bg="white", borderwidth=2, relief="groove")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.create_menu()
        self.create_toolbar()

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.dragging_object = False # Флаг для отслеживания перетаскивания

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выход", command=self.master.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Редактировать", menu=edit_menu)
        edit_menu.add_command(label="Выбрать объект", command=self.select_object_mode)
        edit_menu.add_command(label="Удалить выбранный", command=self.delete_selected_object)

        primitives_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Примитивы", menu=primitives_menu)
        primitives_menu.add_command(label="Отрезок", command=lambda: self.start_drawing("line"))
        primitives_menu.add_command(label="Крест (Kr)", command=lambda: self.start_drawing("cross"))
        primitives_menu.add_command(label="Флаг (Flag)", command=lambda: self.start_drawing("flag"))

        tmo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ТМО", menu=tmo_menu)
        tmo_menu.add_command(label="Пересечение ()", command=self.perform_intersection)
        tmo_menu.add_command(label="Разность ()", command=self.perform_difference)

        transform_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Преобразования", menu=transform_menu)
        transform_menu.add_command(label="Перемещение", command=self.start_translation)
        transform_menu.add_command(label="Поворот (Rc)", command=self.start_rotation_around_point)
        transform_menu.add_command(label="Зеркальное отражение относительно центра фигуры (Mf)", command=self.mirror_around_figure_center)
        transform_menu.add_command(label="Зеркальное отражение относительно вертикальной прямой (MV)", command=self.start_mirror_vertical_line)


        color_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Цвет", menu=color_menu)
        color_menu.add_command(label="Цвет обводки", command=self.choose_outline_color)
        color_menu.add_command(label="Цвет заливки", command=self.choose_fill_color)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def create_toolbar(self):
        toolbar = tk.Frame(self.master, bd=2, relief=tk.RAISED)
        # Используем pack с side=tk.BOTTOM и fill=tk.X для горизонтального расположения
        # Или place/grid для более точного контроля
        toolbar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Размещаем кнопки в строку, используя side=tk.LEFT
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


    def choose_outline_color(self):
        color_code = colorchooser.askcolor(title="Выбрать цвет обводки")[1]
        if color_code:
            self.current_color = color_code
            if self.selected_object:
                self.selected_object.color = self.current_color
                self.redraw_all_objects() # Перерисовываем для обновления цвета

    def choose_fill_color(self):
        color_code = colorchooser.askcolor(title="Выбрать цвет заливки")[1]
        if color_code:
            self.current_fill_color = color_code
            if self.selected_object and hasattr(self.selected_object, 'fill_color'):
                self.selected_object.fill_color = self.current_fill_color
                self.redraw_all_objects() # Перерисовываем для обновления цвета

    def show_about(self):
        messagebox.showinfo("О программе", "Графический редактор. Вариант 70.\nРазработано в рамках курсовой работы по дисциплине \"Графические системы компьютеров\".")

    def start_drawing(self, primitive_type):
        self.drawing_primitive = primitive_type
        self.temp_points = []
        self.selected_object = None # Снимаем выделение
        self.canvas.config(cursor="cross")
        self.clear_transform_marker()
        self.clear_temp_line()
        self.current_transformation_mode = None # Сброс режима трансформации

    def select_object_mode(self):
        self.drawing_primitive = None
        self.canvas.config(cursor="arrow")
        self.clear_transform_marker()
        self.clear_temp_line()
        self.current_transformation_mode = None # Сброс режима трансформации

    def delete_selected_object(self):
        if self.selected_object:
            self.canvas.delete(self.selected_object.id)
            self.objects.remove(self.selected_object)
            self.selected_object = None
            self.clear_transform_marker()
            self.redraw_all_objects() # Просто перерисовываем, чтобы убедиться в чистоте

    def on_canvas_click(self, event):
        if self.drawing_primitive:
            self.temp_points.append(Point(event.x, event.y))
            if self.drawing_primitive == "line":
                if len(self.temp_points) == 2:
                    line = Line(self.temp_points[0], self.temp_points[1], self.current_color)
                    self.objects.append(line)
                    line.draw(self.canvas)
                    self.drawing_primitive = None
                    self.canvas.config(cursor="arrow")
                    self.selected_object = line # Автоматически выделяем новый объект
                    self.highlight_selected_object()
            elif self.drawing_primitive == "cross":
                if len(self.temp_points) == 2: # Центр и точка для определения размера
                    center_x, center_y = self.temp_points[0].x, self.temp_points[0].y
                    # Размер креста будет определяться расстоянием от центра до второй точки
                    size = math.sqrt((event.x - center_x)**2 + (event.y - center_y)**2) * 2
                    cross = Cross(center_x, center_y, size, self.current_color, self.current_fill_color)
                    self.objects.append(cross)
                    cross.draw(self.canvas)
                    self.drawing_primitive = None
                    self.canvas.config(cursor="arrow")
                    self.selected_object = cross # Автоматически выделяем новый объект
                    self.highlight_selected_object()
            elif self.drawing_primitive == "flag":
                if len(self.temp_points) == 2: # Левая верхняя точка и правая нижняя для определения размеров
                    x1, y1 = self.temp_points[0].x, self.temp_points[0].y
                    x2, y2 = self.temp_points[1].x, self.temp_points[1].y
                    width = abs(x2 - x1)
                    height = abs(y2 - y1)
                    # Базовая точка флага - левая нижняя
                    flag = Flag(min(x1, x2), max(y1, y2), width, height, self.current_color, self.current_fill_color)
                    self.objects.append(flag)
                    flag.draw(self.canvas)
                    self.drawing_primitive = None
                    self.canvas.config(cursor="arrow")
                    self.selected_object = flag # Автоматически выделяем новый объект
                    self.highlight_selected_object()

        elif self.current_transformation_mode == "rotation_around_point":
            self.transform_center = Point(event.x, event.y)
            self.draw_transform_marker(self.transform_center.x, self.transform_center.y)
            angle = simpledialog.askfloat("Поворот", "Введите угол поворота (градусы):")
            if angle is not None and self.selected_object:
                Transformations.rotate_around_point(self.selected_object, angle, self.transform_center.x, self.transform_center.y)
                self.redraw_all_objects()
            self.current_transformation_mode = None
            self.clear_transform_marker()
            self.canvas.config(cursor="arrow") # Возвращаем курсор
        elif self.current_transformation_mode == "mirror_vertical_line":
            self.mirror_line_x = event.x
            self.draw_temp_vertical_line(self.mirror_line_x)
            if self.selected_object:
                Transformations.mirror_vertical_line(self.selected_object, self.mirror_line_x)
                self.redraw_all_objects()
            self.current_transformation_mode = None
            self.clear_temp_line()
            self.canvas.config(cursor="arrow") # Возвращаем курсор
        elif self.selected_object:
            # Если объект уже выбран, инициируем перемещение при клике
            self.start_drag_x = event.x
            self.start_drag_y = event.y
            self.dragging_object = True
        else:
            # Попытка выбрать объект, если не в режиме рисования или трансформации
            self.select_object_at_click(event.x, event.y)

    def on_canvas_drag(self, event):
        if self.dragging_object and self.selected_object and self.current_transformation_mode == "translation":
            dx = event.x - self.start_drag_x
            dy = event.y - self.start_drag_y
            Transformations.translate(self.selected_object, dx, dy)
            self.start_drag_x = event.x
            self.start_drag_y = event.y
            self.redraw_all_objects() # Перерисовываем для плавного перемещения

    def on_canvas_release(self, event):
        self.dragging_object = False
        if self.current_transformation_mode == "translation":
            self.canvas.config(cursor="arrow") # Возвращаем курсор после перетаскивания
            self.current_transformation_mode = None


    def select_object_at_click(self, x, y):
        # Простой выбор: ищем объект, ID которого совпадает с кликнутым
        clicked_item = self.canvas.find_closest(x, y)
        if clicked_item:
            item_id = clicked_item[0]
            for obj in self.objects:
                if obj.id == item_id:
                    self.selected_object = obj
                    self.highlight_selected_object()
                    return
        # Если ни один объект не был выбран, снимаем выделение
        self.selected_object = None
        self.redraw_all_objects() # Перерисовываем, чтобы снять старое выделение

    def highlight_selected_object(self):
        # Сначала сбрасываем выделение со всех объектов, затем выделяем выбранный
        for obj in self.objects:
            if obj.id: # Убедимся, что объект уже отрисован
                self.canvas.itemconfig(obj.id, outline=obj.color, width=2) # Возвращаем исходный цвет и толщину обводки

        if self.selected_object:
            self.canvas.itemconfig(self.selected_object.id, outline="red", width=3)
            # Отображаем центр фигуры
            if self.selected_object.center:
                self.draw_transform_marker(self.selected_object.center.x, self.selected_object.center.y, color="green")

    def redraw_all_objects(self):
        self.canvas.delete("all") # Очищаем холст
        self.clear_transform_marker() # Очищаем маркеры перед перерисовкой
        self.clear_temp_line() # Очищаем временную линию
        for obj in self.objects:
            obj.draw(self.canvas)
        if self.selected_object:
            self.highlight_selected_object() # Выделяем, если есть выбранный объект


    def clear_transform_marker(self):
        if self.transform_center_marker_id:
            self.canvas.delete(self.transform_center_marker_id)
            self.transform_center_marker_id = None

    def draw_transform_marker(self, x, y, color="red"):
        self.clear_transform_marker()
        marker_size = 5
        self.transform_center_marker_id = self.canvas.create_oval(x - marker_size, y - marker_size,
                                                                   x + marker_size, y + marker_size,
                                                                   fill=color, outline=color)
        self.canvas.create_line(x - marker_size * 2, y, x + marker_size * 2, y, fill=color)
        self.canvas.create_line(x, y - marker_size * 2, x, y + marker_size * 2, fill=color)

    def perform_intersection(self):
        messagebox.showinfo("ТМО: Пересечение", "Реализация пересечения сложных многоугольников требует продвинутых алгоритмов (например, Сазерленнда-Ходжмана). В данной версии не реализовано.")
        return None

    def perform_difference(self):
        messagebox.showinfo("ТМО: Разность", "Реализация разности сложных многоугольников требует продвинутых алгоритмов. В данной версии не реализовано.")
        return None


    # Геометрические преобразования
    def start_translation(self):
        if not self.selected_object:
            messagebox.showwarning("Ошибка", "Сначала выберите объект для перемещения.")
            return
        self.current_transformation_mode = "translation"
        messagebox.showinfo("Перемещение", "Переместите объект, перетаскивая его мышью.")
        self.canvas.config(cursor="fleur")

    def start_rotation_around_point(self):
        if not self.selected_object:
            messagebox.showwarning("Ошибка", "Сначала выберите объект для поворота.")
            return
        self.current_transformation_mode = "rotation_around_point"
        messagebox.showinfo("Поворот (Rc)", "Кликните на холсте, чтобы задать центр поворота.")
        self.canvas.config(cursor="dotbox")

    def mirror_around_figure_center(self):
        if not self.selected_object:
            messagebox.showwarning("Ошибка", "Сначала выберите объект для отражения.")
            return
        Transformations.mirror_around_figure_center(self.selected_object)
        self.redraw_all_objects()

    def start_mirror_vertical_line(self):
        if not self.selected_object:
            messagebox.showwarning("Ошибка", "Сначала выберите объект для отражения.")
            return
        self.current_transformation_mode = "mirror_vertical_line"
        messagebox.showinfo("Зеркальное отражение (MV)", "Кликните на холсте, чтобы задать вертикальную линию отражения.")
        self.canvas.config(cursor="sb_v_double_arrow")

    def draw_temp_vertical_line(self, x):
        self.clear_temp_line()
        self.temp_line_id = self.canvas.create_line(x, 0, x, self.canvas.winfo_height(), fill="red", dash=(4, 4))

    def clear_temp_line(self):
        if self.temp_line_id:
            self.canvas.delete(self.temp_line_id)
            self.temp_line_id = None


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicEditor(root)
    root.mainloop()
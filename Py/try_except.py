""" 
try - except - else - finally 
"""

def divide_numbers(a, b):
    try: result = a / b
    except ZeroDivisionError:
        print("Ошибка: деление на ноль!")
        return None
    except TypeError as e:
        print(f"Ошибка типа: {e}. Проверьте, что оба числа - целые или вещественные.")
        return None
    else:
        print("Деление выполнено успешно!")
        return result
    finally: print("Завершение операции деления.\n")


def process_data(data):
    try:
        print("Обработка данных...")
        if not isinstance(data, list):
            raise ValueError("Данные должны быть списком!")
        
        # Вложенный try-except
        try:
            print(f"Сумма элементов списка: {sum(data)}")
        except TypeError:
            print("Ошибка: элементы списка должны быть числами!")
        
    except ValueError as ve: print(f"Ошибка значения: {ve}")
    except Exception as e: print(f"Неожиданная ошибка: {e}")
    else: print("Данные обработаны успешно!")
    finally: print("Завершение обработки данных.\n")


# Пример 1: Обработка деления чисел
print(divide_numbers(10, 2))  # Успешное деление
print(divide_numbers(10, 0))  # Деление на ноль
print(divide_numbers("10", 2))  # Ошибка типа


# Пример 2: Обработка данных
process_data([1, 2, 3])  # Успешная обработка
process_data([1, "2", 3])  # Ошибка в элементах списка
process_data("not a list")  # Ошибка типа данных


# Пример 3: Обработка нескольких исключений в одном блоке
try:
    num = int(input("Введите число: "))
    print(f"Вы ввели: {num}")
except (ValueError, KeyboardInterrupt) as e:
    if isinstance(e, ValueError): print("Ошибка: нужно ввести целое число!")
    else: print("\nОперация прервана пользователем.")
else: print("Ввод корректен!")
finally: print("Конец примера 3.")
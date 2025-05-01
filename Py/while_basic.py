# 1: Базовый цикл while
print("Пример 1: Базовый цикл while")
count = 0
while count < 5:
    print(f"Текущее значение count: {count}")
    count += 1  # Важно не забывать изменять условие, иначе цикл будет бесконечным



# 2: else с while
attempt = 0
max_attempts = 3
while attempt < max_attempts:
    print(f"Попытка {attempt + 1} из {max_attempts}")
    attempt += 1
else:
    print("Все попытки исчерпаны.")  # Выполняется, если цикл завершился без break


# 3:  break
secret_number = 7
while True:  # Бесконечный цикл
    guess = int(input("Угадайте число от 1 до 10: "))
    if guess == secret_number:
        print("Поздравляю! Вы угадали!")
        break  # Выход из цикла
    print("Неверно! Попробуйте еще раз.")
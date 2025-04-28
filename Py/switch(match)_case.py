# Python 3.10+ (works like switch in c++\java)
def number_to_string(argument):
    match argument:
        case 0:
            return "zero"
        case 1:
            return "one"
        case 2:
            return "two"
        case _: # Аналог default в других языках
            return "something"
 

head = number_to_string(4)
print(head)

value = (0, 5)

match value:
    case (0, y):
        print(f"Y = {y}")  # Сработает, если первый элемент 0
    case (x, 0):
        print(f"X = {x}")
    case _:
        print("Не подходит")
"""
Validation in python
"""

class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Имя должно быть строкой")
        if len(value) < 2:
            raise ValueError("Имя слишком короткое")
        self._name = value
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise ValueError("Возраст должен быть целым числом")
        if value < 0 or value > 150:
            raise ValueError("Недопустимый возраст")
        self._age = value
    
    @age.deleter
    def age(self):
        print("Удаление возраста")
        del self._age

# Использование
person = Person("Иван", 25)

# Геттер
print(person.name)  # Иван
print(person.age)   # 25

# Сеттер
person.name = "Петр"
person.age = 30

# Валидация в сеттере
try:
    person.age = -5
except ValueError as e:
    print(f"Ошибка: {e}")  # Ошибка: Недопустимый возраст

# Делитер
del person.age  # Удаление возраста
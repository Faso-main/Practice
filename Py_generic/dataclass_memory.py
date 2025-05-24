"""
Code snippet: dataclasses и __slots__
"""

from dataclasses import dataclass

@dataclass(frozen=True)  # immutable объект
class Point:
    x: float
    y: float

    def distance(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

# __slots__ для оптимизации памяти
class Person:
    __slots__ = ("name", "age")  # Запрещает динамическое добавление атрибутов
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
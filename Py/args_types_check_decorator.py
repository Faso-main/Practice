"""
Code snippet example: decorator, that makes markers in methods into data types
"""

import functools
from typing import get_type_hints

def pointers_to_types(func):
    """Декоратор для проверки типов аргументов функции на основе аннотаций."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        type_hints = get_type_hints(func)
        for i, arg in enumerate(args):
            param_name = list(type_hints.keys())[i] if i < len(type_hints) else f"arg_{i}"
            expected_type = type_hints.get(param_name)
            if expected_type and not isinstance(arg, expected_type):
                raise TypeError(f"Аргумент '{param_name}' должен быть типа {expected_type}, а получен {type(arg)}")
        for key, value in kwargs.items():
            expected_type = type_hints.get(key)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(f"Аргумент '{key}' должен быть типа {expected_type}, а получен {type(value)}")
        return func(*args, **kwargs)
    return wrapper

@pointers_to_types
def process_data(name: str, age: int) -> str:
    return f"{name} : {age} !"

print(process_data("Faso", 30))
try:
    print(process_data("Li", '20'))
except TypeError as e:
    print(e)
"""
Code snippet example: time computing
"""

import time, functools


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Функция '{func.__name__}' выполнилась за {execution_time:.2f} секунд")
        return result
    return wrapper

@timer
def some_operation(n):
    time.sleep(n)

some_operation(1)
some_operation(0.5)

"""
Code snippet example of cash, same task called decorator
"""

import functools

def cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = (args, tuple(sorted(kwargs.items())))
        if cache_key not in wrapper.cache:
            wrapper.cache[cache_key] = func(*args, **kwargs)
        return wrapper.cache[cache_key]
    wrapper.cache = {}
    return wrapper

@cache
def test_function(n):
    print(f"Вычисление для {n}...")
    result = 0
    for i in range(n * 1000000):
        result += i
    return result

print(test_function(5))
print(test_function(5)) # Результат берется из кэша

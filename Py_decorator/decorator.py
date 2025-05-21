"""
Code snippet example of universal, flexible error handling 
"""

import functools

def processing(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try: return func(*args, **kwargs)
        except Exception as e: print(f'Ошибка вида: {e}.....') #общая обработа ошибок
    return wrapper
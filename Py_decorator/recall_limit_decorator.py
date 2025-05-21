"""
Code snippet : limiting the frequent usage
"""

import time
import functools

def limit_recall(interval):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if not hasattr(wrapper, 'last_call') or now - wrapper.last_call >= interval:
                result = func(*args, **kwargs)
                wrapper.last_call = now
                return result
        return wrapper
    return decorator

@limit_recall(1) # Разрешает вызывать функцию не чаще, чем раз в секунду
def api_call():
    print("Вызов API...")

api_call()
time.sleep(0.5)
api_call()
time.sleep(1.2)
api_call()
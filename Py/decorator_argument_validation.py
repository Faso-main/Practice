from functools import wraps

def validate_args(**validators):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Проверяем позиционные аргументы
            for i, (arg_name, validator) in enumerate(validators.items()):
                if i < len(args):
                    if not validator(args[i]):
                        raise ValueError(f"Invalid argument: {arg_name}={args[i]}")
            
            # Проверяем именованные аргументы
            for arg_name, validator in validators.items():
                if arg_name in kwargs and not validator(kwargs[arg_name]):
                    raise ValueError(f"Invalid argument: {arg_name}={kwargs[arg_name]}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Пример использования
@validate_args(x=lambda v: v > 0, y=lambda v: isinstance(v, str))
def process_data(x, y):
    return f"x={x}, y={y}"

print(process_data(10, "test"))  # OK
print(process_data(-5, "abc"))  # ValueError: Invalid argument: x=-5
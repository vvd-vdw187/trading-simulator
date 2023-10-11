from functools import wraps
import inspect

# Decorator that checks if all float or int arguments passed to a function are greater than zero.
def greater_than_zero(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        param_names = list(inspect.signature(func).parameters.keys())
                           
        for i, arg in enumerate(args):
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f"In function '{func.__name__}': Argument '{param_names[i]}' with value {arg} must be greater than zero.")
            
        for key, value in kwargs.items():
            if isinstance(value, (int, float)) and value <= 0:
                raise ValueError(f"In function '{func.__name__}': Argument '{key}' with value {value} must be greater than zero.")
            
        return func(*args, **kwargs)
    return wrapper
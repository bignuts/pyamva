from datetime import datetime
from functools import wraps
from time import perf_counter
from pickle import dump, load
from typing import Any


def timer(func):
    """
    Print the runtime of the decorated function
    """
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


def debug(func):
    """
    Print the function signature and return value
    """
    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")
        return value
    return wrapper_debug


def is_datetime_aware(dt: datetime) -> bool:
    # if dt.tzinfo != None and dt.tzinfo.utcoffset(None) != None:
    if dt.tzinfo is not None:
        return True
    else:
        return False


def pickle_dump(obj: Any, path: str) -> None:
    with open(path, 'wb') as f:
        dump(obj, f)


def pickle_load(path: str) -> Any:
    with open(path, 'rb') as f:
        return load(f)

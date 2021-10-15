from datetime import datetime
from functools import wraps
from time import perf_counter
from pickle import dump, load
from typing import Any, List
from connectors import Rates


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


def rates_to_py_file(rates: List[Rates], file_name: str) -> None:
    with open(file_name, 'w') as file:
        file.write('from typing import List\n')
        file.write('from connectors import Rates\n')
        file.write('from datetime import datetime\n')
        file.writelines('\n')
        file.writelines('\n')
        file.write('rates : List[Rates] = [\n')
        for rate in rates:
            print(rate)
            time = rate['time']
            s = f"\t{{'time': datetime({time.year}, {time.month}, {time.day}, {time.hour}, {time.minute}, {time.second}), 'open': {rate['open']}, 'high': {rate['high']}, 'low': {rate['low']}, 'close': {rate['close']}, 'tick_volume': {rate['tick_volume']}, 'spread': {rate['spread']}, 'real_volume': {rate['real_volume']}}},\n"
            file.write(s)
        file.write(']')

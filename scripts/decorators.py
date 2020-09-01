import time
from functools import update_wrapper, wraps

import pint
from flask import abort, g, redirect, request, url_for


def do_twice(func):
    @wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        return func(*args, **kwargs), func(*args, **kwargs)

    return wrapper_do_twice


def timer(func):
    """
    Print the runtimeof the decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        taken = end_time - start_time
        run_time = f"Finished {func.__name__!r} in {taken: .4f} secs"
        print(run_time)
        return value

    return wrapper


def debug(func):
    """
    Print the function signature and return value
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k} = {v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__}returned {value!r}")
        return value

    return wrapper


def slow_down(func):
    """
    Slows down a function, by 1 second of sleep
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)

    return wrapper


def login_required(func):
    """
    Make sure user is logged in before proceeding
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    return wrapper


def repeat(_func=None, *, num_times=2):
    def decorator_repeat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value

        return wrapper

    if _func is None:
        return decorator_repeat
    else:
        return decorator_repeat(_func)


def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count_calls += 1
        print(f"Call {wrapper.count_calls} of {func.__name__!r}")
        return func(*args, **kwargs)

    wrapper.count_calls = 0
    return wrapper


class Counter:
    def __init__(self, start=0):
        self.count = start

    def __call__(self):
        self.count += 1
        print(f"Current calls count is {self.count}")


class CountCalls:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)


def slowdown(_func=None, *, rate=1):
    """
    Sleep given amount of seconds before calling the function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(rate)
            return func(*args, **kwargs)

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


def set_unit(unit):
    def wrapper(func):
        func.unit = unit
        return func

    return wrapper


def use_unit(unit):
    """
    Have a function return a Quantity with given unit
    """
    use_unit.ureg = pint.UnitRegistry()

    def decorator(func):
        wraps(func)

        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            return value * use_unit.ureg(unit)

        return wrapper

    return decorator


def validate_json(*expected_args):
    def decorator(func):
        wraps(func)

        def wrapper(*args, **kwargs):
            json_object = request.get_json()
            for expected_arg in expected_args:
                if expected_arg not in json_object:
                    abort(400)
                return func(*args, **kwargs)

        return wrapper

    return decorator


a = """
Boiler plate for a decorator that takes args
def name(_func=None, *, kw1=val1, kw2=val2, ...):  # 1
    def decorator_name(func):
        ...  # Create and return a wrapper function.

    if _func is None:
        return decorator_name                      # 2
    else:
        return decorator_name(_func)               # 3
"""

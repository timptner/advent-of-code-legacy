import time

from functools import wraps, partial, update_wrapper

from utilities.storage import BASE_DIR


def measure_time(func):
    """Measure the runtime of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        value = func(*args, **kwargs)
        stop = time.perf_counter_ns()
        delta = stop - start
        return value, delta

    return wrapper


class RateLimit:
    def __init__(self, func, seconds: int = 300):
        update_wrapper(self, func)
        self.func = func
        self.seconds = seconds
        self.time = time.time() - seconds

    def __call__(self, *args, **kwargs):
        now = time.time()
        if now < self.locked_until():
            name = self.func.__name__
            delta = self.locked_until() - now
            raise Exception(f"Canceled execution of '{name}' because rate limit remains for {delta:.1f} s")

        self.time = now
        return self.func(*args, **kwargs)

    def locked_until(self) -> float:
        return self.time + self.seconds


def rate_limit(func=None, *, seconds: int = 300):
    """Rate limit function when called multiple times."""
    if func is None:
        return partial(rate_limit, seconds=seconds)

    return RateLimit(func, seconds=seconds)


def cache(func):
    """Keep a cache of function return value in local file."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        year = kwargs['year']
        day = kwargs['day']
        path = BASE_DIR / 'data' / str(year) / f'{day:02d}.txt'
        if path.exists():
            value = path.read_text()
        else:
            value = func(*args, **kwargs)
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            path.write_text(value)
        return value

    return wrapper

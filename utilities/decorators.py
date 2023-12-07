import time

from functools import wraps, partial, update_wrapper

from utilities.console import console
from utilities.storage import BASE_DIR


def _get_human_delta(delta: int) -> str:
    """Convert time delta (in ns) to human readable unit."""
    digits = len(str(delta))
    if digits < 4:
        msg = f"{delta} ns"
    elif digits < 7:
        msg = f"{delta * 1e-3:.1f} µs"
    elif digits < 10:
        msg = f"{delta * 1e-6:.1f} ms"
    else:
        msg = f"{delta * 1e-9:.1f} s"
    return msg


def measure_time(func):
    """Print the runtime of the decorated function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        value = func(*args, **kwargs)
        stop = time.perf_counter_ns()
        delta = stop - start
        human_delta = _get_human_delta(delta)
        console.print(f"Finished '{func.__name__}' in {human_delta}")
        return value

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

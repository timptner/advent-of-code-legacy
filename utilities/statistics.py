import time


def measure_execution_time(func, *args, **kwargs) -> (int, float):
    start = time.time()
    answer = func(*args, **kwargs)
    stop = time.time()
    delta = stop - start
    return answer, delta


def get_human_delta(delta: float) -> str:
    if delta < 1:
        return f"{delta * 1e3:.1f} ms"
    else:
        return f"{delta:.1f} s"

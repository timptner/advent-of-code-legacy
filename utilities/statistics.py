import time


def measure_execution_time(func, *args, **kwargs) -> (int, float):
    start = time.time()
    answer = func(*args, **kwargs)
    stop = time.time()
    delta = stop - start
    return answer, delta


def get_human_delta(delta: float) -> str:
    if delta < 1e-3:
        msg = f"{delta * 1e6:.1f} µs"
    elif delta < 1:
        msg = f"{delta * 1e3:.1f} ms"
    elif delta < 60:
        msg = f"{delta:.1f} s"
    elif delta < 60**2:
        msg = f"{delta / 60:.1f} min"
    else:
        msg = f"{delta / 60:.1f} h"
    return msg

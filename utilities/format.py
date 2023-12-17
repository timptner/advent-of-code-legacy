def human_delta(delta: int) -> str:
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

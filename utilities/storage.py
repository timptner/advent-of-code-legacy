import os

from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'


def read_data(year: int, day: int, name: str = 'prod') -> str:
    if year not in range(2015, 2024):
        raise ValueError("Invalid year.")

    if day not in range(1, 26):
        raise ValueError("Invalid day.")

    file = DATA_DIR / str(year) / f'{day:02d}' / name

    if not file.exists():
        raise FileNotFoundError(f"Please download {name} data for {year}-{day} first!")

    content = file.read_text()

    return content

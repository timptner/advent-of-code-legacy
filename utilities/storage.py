import os

from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'


def _get_latest_event() -> int:
    today = date.today()
    if today >= date(today.year, 12, 1):
        year = today.year
    else:
        year = today.year - 1
    return year


def read_data(year: int, day: int) -> str:
    latest_event = _get_latest_event()

    if year not in range(2015, latest_event + 1):
        raise ValueError("Invalid year.")
    if day not in range(1, 26):
        raise ValueError("Invalid day.")

    name = os.getenv('AOC_ENV', 'prod')
    choices = ['test', 'prod']
    if name not in choices:
        raise ValueError(f"Unknown value for 'AOC_ENV'. Possible values are: {choices}")

    file = DATA_DIR / str(year) / f'{day:02d}' / f'{name}.txt'

    if not file.exists():
        print(file)
        raise FileNotFoundError(f"Please download {name} data first!")

    content = file.read_text().strip()
    return content

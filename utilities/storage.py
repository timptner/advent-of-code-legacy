import os

from pathlib import Path

from .backend import _get_puzzle_input

BASE_DIR = Path(__file__).parent.parent


def load_dotenv() -> None:
    path = BASE_DIR / '.env'
    content = path.read_text()
    for line in content.splitlines():
        key, value = line.split('=', maxsplit=1)
        if key == 'AOC_SESSION':
            os.environ[key] = value


def read_puzzle_input(year: int, day: int) -> str:
    path = BASE_DIR / 'data' / str(year) / f'{day:02d}.txt'
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    if path.exists():
        content = path.read_text()
    else:
        content = _get_puzzle_input(year, day)
        path.write_text(content)
    return content

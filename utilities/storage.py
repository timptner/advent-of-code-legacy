import os

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


def load_dotenv() -> None:
    path = BASE_DIR / '.env'
    content = path.read_text()
    for line in content.splitlines():
        key, value = line.split('=', maxsplit=1)
        if key == 'AOC_SESSION':
            os.environ[key] = value

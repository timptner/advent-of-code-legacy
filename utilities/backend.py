import os

from pathlib import Path
from urllib.parse import urljoin

import requests

BASE_DIR = Path(__file__).parent.parent

ENDPOINT = 'https://adventofcode.com'


def _get_puzzle_input(year: int, day: int) -> str:
    url = urljoin(ENDPOINT, f'{year}/day/{day}/input')
    session = os.environ['AOC_SESSION']
    headers = {
        'Cookie': f'session={session}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Retrieved puzzle input from backend")
        return response.content.decode('utf-8')
    else:
        raise Exception(f"[{response.status_code}] {response.content}")

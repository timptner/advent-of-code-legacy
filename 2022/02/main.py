#! /usr/bin/env python3

from pathlib import Path

file = Path(__file__).parent / 'data_prod.txt'


def read_data() -> str:
    content = file.read_text().strip()
    return content


PLAYER_A_TRANSLATION = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors',
}

PLAYER_B_TRANSLATION = {
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissors',
}

SHAPE_COUNT = {
    'rock': 1,
    'paper': 2,
    'scissors': 3,
}


def compare(player_a, player_b) -> tuple[int, int]:
    if player_a == player_b:
        return 3, 3
    if player_a == 'rock' and player_b == 'paper':
        return 0, 6
    if player_a == 'rock' and player_b == 'scissors':
        return 6, 0
    if player_a == 'paper' and player_b == 'rock':
        return 6, 0
    if player_a == 'paper' and player_b == 'scissors':
        return 0, 6
    if player_a == 'scissors' and player_b == 'rock':
        return 0, 6
    if player_a == 'scissors' and player_b == 'paper':
        return 6, 0
    raise Exception("Unknown comparison")


def result_converter(player_a, strategy) -> str:
    if player_a == 'rock' and strategy == 'X':
        return 'scissors'
    if player_a == 'rock' and strategy == 'Y':
        return 'rock'
    if player_a == 'rock' and strategy == 'Z':
        return 'paper'

    if player_a == 'paper' and strategy == 'X':
        return 'rock'
    if player_a == 'paper' and strategy == 'Y':
        return 'paper'
    if player_a == 'paper' and strategy == 'Z':
        return 'scissors'

    if player_a == 'scissors' and strategy == 'X':
        return 'paper'
    if player_a == 'scissors' and strategy == 'Y':
        return 'scissors'
    if player_a == 'scissors' and strategy == 'Z':
        return 'rock'

    raise Exception("Unknown combination")


def main() -> None:
    data = read_data()
    player_a_score = 0
    player_b_score = 0
    for game in data.splitlines():
        player_a, player_b = game.split()
        player_a = PLAYER_A_TRANSLATION[player_a]
        player_b = PLAYER_B_TRANSLATION[player_b]
        result = compare(player_a, player_b)
        player_a_score += result[0] + SHAPE_COUNT[player_a]
        player_b_score += result[1] + SHAPE_COUNT[player_b]
    print(f"Scores\n------")
    print(f"Player A: {player_a_score}")
    print(f"Player A: {player_b_score} (me)")

    player_a_score = 0
    player_b_score = 0
    for game in data.splitlines():
        player_a, player_b = game.split()
        player_a = PLAYER_A_TRANSLATION[player_a]
        player_b = result_converter(player_a, player_b)
        result = compare(player_a, player_b)
        player_a_score += result[0] + SHAPE_COUNT[player_a]
        player_b_score += result[1] + SHAPE_COUNT[player_b]
    print(f"Scores V2\n---------")
    print(f"Player A: {player_a_score}")
    print(f"Player A: {player_b_score} (me)")


if __name__ == '__main__':
    main()

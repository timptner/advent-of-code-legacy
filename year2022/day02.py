#! /usr/bin/env python3

from utilities.storage import read_data


def compare(player1: str, player2: str) -> (int, int):
    if player1 == player2:
        return 3, 3
    if player1 == 'rock' and player2 == 'paper':
        return 0, 6
    if player1 == 'rock' and player2 == 'scissors':
        return 6, 0
    if player1 == 'paper' and player2 == 'rock':
        return 6, 0
    if player1 == 'paper' and player2 == 'scissors':
        return 0, 6
    if player1 == 'scissors' and player2 == 'rock':
        return 0, 6
    if player1 == 'scissors' and player2 == 'paper':
        return 6, 0
    raise Exception("Unknown comparison")


def get_move(player1: str, player2: str) -> str:
    if player1 == 'rock' and player2 == 'X':
        return 'scissors'
    if player1 == 'rock' and player2 == 'Y':
        return 'rock'
    if player1 == 'rock' and player2 == 'Z':
        return 'paper'

    if player1 == 'paper' and player2 == 'X':
        return 'rock'
    if player1 == 'paper' and player2 == 'Y':
        return 'paper'
    if player1 == 'paper' and player2 == 'Z':
        return 'scissors'

    if player1 == 'scissors' and player2 == 'X':
        return 'paper'
    if player1 == 'scissors' and player2 == 'Y':
        return 'scissors'
    if player1 == 'scissors' and player2 == 'Z':
        return 'rock'

    raise Exception("Unknown combination")


ENCRYPTION = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors',
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissors',
}


def get_shape(letter: str) -> str:
    try:
        shape = ENCRYPTION[letter]
    except KeyError:
        raise ValueError("Unknown encryption letter.")

    return shape


def get_games(version: int = 1) -> list:
    data = read_data(year=2022, day=2)
    games = []
    for line in data.splitlines():
        player1, player2 = line.split()
        player1 = get_shape(player1)

        if version == 1:
            player2 = get_shape(player2)
        elif version == 2:
            player2 = get_move(player1, player2)
        else:
            raise ValueError("Unknown games version.")

        game = (player1, player2)
        games.append(game)
    return games


def get_score(version: int = 1) -> (int, int):
    shape_points = {
        'rock': 1,
        'paper': 2,
        'scissors': 3,
    }

    player1_score = 0
    player2_score = 0
    for player1, player2 in get_games(version=version):
        result = compare(player1, player2)
        player1_score += shape_points[player1] + result[0]
        player2_score += shape_points[player2] + result[1]
    return player1_score, player2_score


def main() -> None:
    score = get_score()[1]
    print(f"Part 1: {score}")

    score2 = get_score(version=2)[1]
    print(f"Part 2: {score2}")


if __name__ == '__main__':
    main()

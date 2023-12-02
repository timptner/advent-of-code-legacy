#! /usr/bin/env python3

from utilities.storage import read_data


def main() -> None:
    valid = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }
    data = read_data(2023, 2, 'prod')
    invalid_games = set()
    power_list = []
    lines = data.splitlines()
    for line in lines:
        heighest = {
            'red': 0,
            'green': 0,
            'blue': 0,
        }

        game, results = line.split(':')
        index = game.removeprefix('Game ')
        index = int(index)

        items = []
        for result in results.split(';'):
            cubes = []
            for cube in result.split(','):
                amount, color = cube.split()
                amount = int(amount)
                if amount > valid[color]:
                    invalid_games.add(index)
                maximum = heighest[color]
                if amount > maximum:
                    heighest[color] = amount
                cubes.append((amount, color))
            items.append(cubes)
        power = heighest['red'] * heighest['green'] * heighest['blue']
        power_list.append(power)
    games = set(range(1, len(lines) + 1))
    valid_games = games - invalid_games
    print(sum(valid_games))
    print(sum(power_list))


if __name__ == '__main__':
    main()

def main(data: str) -> (int, int):
    valid = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }
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
    return sum(valid_games), sum(power_list)


def first_part(data: str) -> int:
    return main(data)[0]


def second_part(data: str) -> int:
    return main(data)[1]

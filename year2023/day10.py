Coordinates = tuple[int, int]


class Grid:
    data = {}
    size = (0, 0)

    def __init__(self, text: str) -> None:
        lines = text.splitlines()
        rows = len(lines)
        columns = len(list(lines[0]))
        for y, line in enumerate(lines):
            items = list(line)
            if len(items) != columns:
                raise ValueError("Grid has unequal items per line.")
            for x, value in enumerate(items):
                self[x, y] = value
        self.size = (rows, columns)

    def __setitem__(self, key: Coordinates, value) -> None:
        self.data[*key] = str(value)

    def __getitem__(self, item: Coordinates) -> str:
        return self.data[*item]
    
    def print(self) -> None:
        rows, columns = self.size
        for y in range(rows):
            column = ''.join([str(self[x, y]) for x in range(columns)])
            print(column)

    def find(self, value: str) -> list[Coordinates]:
        results = []
        for key, grid_value in self.data.items():
            if value == grid_value:
                results.append(key)
        return results

    def get_above(self, x: int, y: int) -> tuple[Coordinates, str]:
        coordinates = x, y - 1
        return coordinates, self[coordinates]

    def get_below(self, x: int, y: int) -> tuple[Coordinates, str]:
        coordinates = x, y + 1
        return coordinates, self[coordinates]

    def get_left(self, x: int, y: int) -> tuple[Coordinates, str]:
        coordinates = x - 1, y
        return coordinates, self[coordinates]

    def get_right(self, x: int, y: int) -> tuple[Coordinates, str]:
        coordinates = x + 1, y
        return coordinates, self[coordinates]

    def get_neighbors(self, x: int, y: int) -> dict[Coordinates, str]:
        points = [
            self.get_above(x, y),
            self.get_left(x, y),
            self.get_right(x, y),
            self.get_below(x, y),
        ]
        return {key: value for key, value in points}


def first_part(data: str) -> int:
    grid = Grid(data)
    start_point = grid.find('S')[0]

    parameters = {
        'above': ('|', 'F', '7'),
        'below': ('|', 'L', 'J'),
        'left': ('-', 'F', 'L'),
        'right': ('-', 'J', '7'),
    }
    convert = {
        '|': ('above', 'below'),
        'L': ('above', 'right'),
        'F': ('below', 'right'),
        'J': ('above', 'left'),
        '7': ('below', 'left'),
        '-': ('left', 'right'),
    }
    valid_points = [(('above', 'below', 'left', 'right'), start_point)]
    counter = 0
    while True:
        current_points = []
        for names, point in valid_points:
            grid[*point] = counter
            for name in names:
                values = parameters[name]
                func = getattr(grid, f'get_{name}')
                try:
                    next_point, value = func(*point)
                except KeyError:
                    continue
                if value in values:
                    current_points.append((convert[value], next_point))
        if not valid_points:
            break
        else:
            valid_points = current_points
            counter += 1
    return counter - 1


def second_part(data: str) -> int:
    pass

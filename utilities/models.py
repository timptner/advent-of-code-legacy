class Grid:
    Point = tuple[int, int]

    def __init__(self, text: str,) -> None:
        self.data = {}

        lines = text.splitlines()
        for row, line in enumerate(lines):
            for column, character in enumerate(list(line)):
                self[row, column] = character
        self.size = len(lines), len(lines[0])

    def __getitem__(self, point: Point) -> str:
        return self.data[*point]

    def __setitem__(self, point: Point, character: str) -> None:
        self.data[*point] = character

    def __str__(self) -> str:
        rows, columns = self.size
        lines = []
        for row in range(rows):
            line = [self[row, column] for column in range(columns)]
            lines.append(''.join(line))
        return '\n'.join(lines)

    def __repr__(self) -> str:
        return f"Grid {self.size}"

    def transpose(self) -> None:
        rows, columns = self.size
        lines = []
        for row in range(rows):
            line = [self[row, column] for column in range(columns)]
            lines.append(line)
        data = {}
        for row, line in enumerate(zip(*lines)):
            for column, value in enumerate(line):
                data[row, column] = value
        self.data = data

    def flip_horizontal(self) -> None:
        rows, columns = self.size
        lines = []
        for row in range(rows):
            line = [self[row, column] for column in range(columns)]
            lines.append(line)
        data = {}
        for row, line in enumerate(reversed(lines)):
            for column, value in enumerate(line):
                data[row, column] = value
        self.data = data

    def flip_vertical(self) -> None:
        rows, columns = self.size
        lines = []
        for row in range(rows):
            line = [self[row, column] for column in range(columns)]
            lines.append(line)
        data = {}
        for row, line in enumerate(lines):
            for column, value in enumerate(reversed(line)):
                data[row, column] = value
        self.data = data

    def rotate_left(self) -> None:
        self.transpose()
        self.flip_horizontal()

    def rotate_right(self) -> None:
        self.transpose()
        self.flip_vertical()

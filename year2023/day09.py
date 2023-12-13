from utilities.backend import BasePuzzle


def calculate_differences(numbers: list[int]) -> list[int]:
    differences = []
    for index in range(len(numbers) - 1):
        difference = numbers[index + 1] - numbers[index]
        differences.append(difference)
    return differences


def get_prediction(numbers: list[list[int]], is_future: bool = True) -> list[list[int]]:
    numbers = list(reversed(numbers))
    numbers[0].append(0) if is_future else numbers[0].insert(0, 0)
    for index in range(len(numbers) - 1):
        row = numbers[index]
        next_row = numbers[index + 1]
        if is_future:
            new_value = row[-1] + next_row[-1]
            next_row.append(new_value)
        else:
            new_value = next_row[0] - row[0]
            next_row.insert(0, new_value)
    numbers = list(reversed(numbers))
    return numbers


class Puzzle(BasePuzzle):
    year = 2023
    day = 9
    name = "Mirage Maintenance"

    def part1(self, text: str) -> int:
        future_values = []
        for line in text.splitlines():
            numbers = [int(line) for line in line.split()]

            list_of_numbers = [numbers]
            while True:
                numbers = calculate_differences(numbers)
                list_of_numbers.append(numbers)
                if not any(numbers):
                    break

            list_of_numbers = get_prediction(list_of_numbers)
            future_values.append(list_of_numbers[0][-1])
        return sum(future_values)

    def part2(self, text: str) -> int:
        past_values = []
        for line in text.splitlines():
            numbers = [int(line) for line in line.split()]

            list_of_numbers = [numbers]
            while True:
                numbers = calculate_differences(numbers)
                list_of_numbers.append(numbers)
                if not any(numbers):
                    break

            list_of_numbers = get_prediction(list_of_numbers, is_future=False)
            past_values.append(list_of_numbers[0][0])
        return sum(past_values)

    def update_test_data(self) -> None:
        text = """
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
        """
        self.test_data = {
            'part1': (text, 114),
            'part2': (text, 2),
        }

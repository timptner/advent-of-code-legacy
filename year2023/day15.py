from utilities.backend import BasePuzzle


ASCII = {chr(n): n for n in range(32, 127)}


class Puzzle(BasePuzzle):
    year = 2023
    day = 15
    name = "Lens Library"

    def part1(self, text: str) -> int:
        items = text.replace('\n', '').split(',')
        numbers = []
        for item in items:
            chars = list(item)
            number = 0
            for char in chars:
                number = (number + ASCII[char]) * 17 % 256
            numbers.append(number)
        return sum(numbers)

    def part2(self, text: str) -> int:
        items = text.replace('\n', '').split(',')
        boxes = {n: [] for n in range(256)}
        for item in items:
            if '-' in item:
                operation = 'remove'
                label, focal_length = item.split('-')
            elif '=' in item:
                operation = 'replace'
                label, focal_length = item.split('=')
            else:
                raise ValueError(f"Malformed string '{item}'")

            number = 0
            for char in list(label):
                number = (number + ASCII[char]) * 17 % 256

            box: list = boxes[number]
            labels, lengths = list(zip(*box)) if box else [[], []]
            if operation == 'remove':
                if label in labels:
                    index = labels.index(label)
                    box.pop(index)
            elif operation == 'replace':
                focal_length = int(focal_length)
                lens = (label, focal_length)
                if label in labels:
                    index = labels.index(label)
                    box.pop(index)
                    box.insert(index, lens)
                else:
                    box.append(lens)
            else:
                raise ValueError(f"Unknown operation '{operation}'")

            # print(f"\nAfter '{item}':")
            # for n, box in boxes.items():
            #     if not box:
            #         continue
            #     msg = [f'[{lens[0]} {lens[1]}]' for lens in box]
            #     print(f"Box {n}: {' '.join(msg)}")

        lens_power = {}
        for n, box in boxes.items():
            value = n + 1
            for index, lens in enumerate(box, 1):
                label, focal_length = lens
                focusing_power = value * index * focal_length
                if label in lens_power.keys():
                    raise KeyError("Lens already exists")
                lens_power[label] = focusing_power

        return sum(lens_power.values())

    def update_test_data(self) -> None:
        text = """
        rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        """

        self.test_data = {
            'part1': (text, 1320),
            'part2': (text, 145),
        }

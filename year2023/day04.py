def get_matched_numbers(data: str) -> dict:
    cards = {}
    for line in data.splitlines():
        card, numbers = line.split(':')
        card = int(card.removeprefix('Card '))

        game_numbers, winning_numbers = numbers.split('|')
        game_numbers = {int(number) for number in game_numbers.strip().split()}
        winning_numbers = {int(number) for number in winning_numbers.strip().split()}

        matched_numbers = game_numbers & winning_numbers
        cards[card] = matched_numbers
    return cards


def first_part(data: str) -> int:
    cards = get_matched_numbers(data)
    points_per_card = {}
    for card, numbers in cards.items():
        count = len(numbers)
        if count > 0:
            points = 2 ** (count - 1)
        else:
            points = 0
        points_per_card[card] = points
    return sum(points_per_card.values())


def second_part(data: str) -> int:
    cards = get_matched_numbers(data)
    counts = {card: len(numbers) for card, numbers in cards.items()}
    card_counts = {card: 1 for card, count in counts.items()}
    for card, count in counts.items():
        for _ in range(card_counts[card]):
            for index in range(count):
                try:
                    card_counts[card + index + 1] += 1
                except KeyError:
                    continue
    return sum(card_counts.values())

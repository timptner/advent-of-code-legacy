#! /usr/bin/env python3

from utilities.storage import read_data


def main() -> None:
    data = read_data(2023, 4, 'prod')

    cards = {}
    card_wins = {}
    for line in data.splitlines():
        card, numbers = line.split(':')
        card = int(card.removeprefix('Card '))

        numbers = [number.strip() for number in numbers.split('|')]
        numbers1 = {int(number) for number in numbers[0].split()}
        numbers2 = {int(number) for number in numbers[1].split()}
        winning_numbers = numbers1 & numbers2
        wins = len(winning_numbers)
        card_wins[card] = wins
        if wins > 0:
            card_points = 2 ** (wins - 1)
        else:
            card_points = 0
        cards[card] = card_points
    print(f"Part 1: {sum(cards.values())}")

    total_cards = {card: 1 for card, points in card_wins.items()}
    for card, points in card_wins.items():
        amount = total_cards[card]
        for _ in range(amount):
            for index in range(points):
                try:
                    total_cards[card + index + 1] += 1
                except KeyError:
                    continue
        # print(card, total_cards)
    # print(total_cards)
    print(f"Part 2: {sum(total_cards.values())}")


if __name__ == '__main__':
    main()

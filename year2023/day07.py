from enum import Enum


def card_to_hex(letter: str) -> str:
    letters = {
        'T': 'A',
        'J': 'B',
        'Q': 'C',
        'K': 'D',
        'A': 'E',
    }
    try:
        value = letters[letter]
    except KeyError:
        value = letter
    return value


def get_best_hand(hand: str) -> str:
    hand_reduced = hand.replace('J', '')
    card_counts = {card: hand_reduced.count(card) for card in set(hand_reduced)}

    highest_amount = 0
    highest_card_hex = '2'
    highest_card = '2'
    for card, amount in card_counts.items():
        card_hex = card_to_hex(card)
        if amount > highest_amount:
            highest_amount = amount
            highest_card_hex = card_hex
            highest_card = card
            continue
        if amount == highest_amount and card_hex > highest_card_hex:
            highest_amount = amount
            highest_card_hex = card_hex
            highest_card = card
            continue

    best_hand = hand.replace('J', highest_card)
    return best_hand


class HandType(Enum):
    FIVE_OF_A_KIND = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    THREE_OF_A_KIND = 3
    TWO_PAIR = 4
    ONE_PAIR = 5
    HIGH_CARD = 6


def get_hand_type(hand: str) -> HandType:
    card_counts = {card: hand.count(card) for card in set(hand)}
    unique_cards = len(card_counts)
    count_set = set(card_counts.values())
    if count_set == {5}:
        hand_type = HandType.FIVE_OF_A_KIND
    elif count_set == {1, 4}:
        hand_type = HandType.FOUR_OF_A_KIND
    elif count_set == {2, 3}:
        hand_type = HandType.FULL_HOUSE
    elif count_set == {1, 3}:
        hand_type = HandType.THREE_OF_A_KIND
    elif count_set == {1, 2}:
        if unique_cards == 3:
            hand_type = HandType.TWO_PAIR
        elif unique_cards == 4:
            hand_type = HandType.ONE_PAIR
        else:
            raise ValueError(f"Unknown hand type: {hand}")
    elif count_set == {1}:
        hand_type = HandType.HIGH_CARD
    else:
        raise ValueError(f"Unknown hand type: {hand}")
    return hand_type


def sort_by_hand_type(item) -> int:
    hand_type, _ = item
    return hand_type.value


def sort_by_hand(item: tuple[str, int]) -> int:
    hand = item[0]
    cards_hex = [card_to_hex(card) for card in hand]
    value = int(''.join(cards_hex), 16)
    return value


def sort_data(data: str, use_jokers: bool = False) -> int:
    rounds = []
    for line in data.splitlines():
        hand, bid = line.split()
        item = (hand, int(bid))
        rounds.append(item)

    groups = {}
    for hand, bid in rounds:
        if use_jokers:
            hand = get_best_hand(hand)

        hand_type = get_hand_type(hand)
        if hand_type not in groups.keys():
            groups[hand_type] = []

        item = (hand, bid)
        groups[hand_type].append(item)

    rounds_grouped = list(groups.items())
    rounds_grouped.sort(key=sort_by_hand_type, reverse=True)
    _, rounds_sorted = zip(*rounds_grouped)

    bids_sorted = []
    for group in rounds_sorted:
        if use_jokers:
            group = [(hand.replace('J', '1'), bid) for hand, bid in group]
        group.sort(key=sort_by_hand)
        hands, bids = zip(*group)
        bids_sorted += bids

    total = 0
    for rank, bid in enumerate(bids_sorted, 1):
        total += bid * rank
    return total


def first_part(data: str) -> int:
    value = sort_data(data)
    return value


def second_part(data: str) -> int:
    value = sort_data(data, use_jokers=True)
    return value

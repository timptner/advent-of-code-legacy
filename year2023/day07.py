from enum import Enum


def get_best_hand(hand: str) -> str:
    cards = [card for card in list(hand) if card != 'J']
    card_counts = {card: cards.count(card) for card in set(cards)}
    highest_amount = 0
    highest_hex_card = '2'
    highest_card = '2'
    for card, amount in card_counts.items():
        hex_card = card_to_hex(card)
        if amount > highest_amount:
            highest_amount = amount
            highest_hex_card = hex_card
            highest_card = card
            continue
        if amount == highest_amount and hex_card > highest_hex_card:
            highest_amount = amount
            highest_hex_card = hex_card
            highest_card = card
            continue

    best_hand = hand.replace('J', highest_card)
    return best_hand


Hand = tuple[str, int]


def parse_data(data: str) -> list[Hand]:
    lines = []
    for line in data.splitlines():
        hand, bid = line.split()
        bid = int(bid)
        lines.append((hand, bid))
    return lines


class HandType(Enum):
    FIVE_OF_A_KIND = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    THREE_OF_A_KIND = 3
    TWO_PAIR = 4
    ONE_PAIR = 5
    HIGH_CARD = 6


def filter_type(cards: str) -> HandType:
    card_counts = {card: cards.count(card) for card in set(cards)}
    count_set = set(card_counts.values())
    if count_set == {5}:
        hand_type = HandType.FIVE_OF_A_KIND
    elif count_set == {1, 4}:
        hand_type = HandType.FOUR_OF_A_KIND
    elif count_set == {2, 3}:
        hand_type = HandType.FULL_HOUSE
    elif count_set == {1, 3}:
        hand_type = HandType.THREE_OF_A_KIND
    elif count_set == {1, 2} and len(card_counts) == 3:
        hand_type = HandType.TWO_PAIR
    elif count_set == {1, 2} and len(card_counts) == 4:
        hand_type = HandType.ONE_PAIR
    elif count_set == {1}:
        hand_type = HandType.HIGH_CARD
    else:
        raise ValueError(f"Unknown hand type: {cards}")
    return hand_type


def card_to_hex(char: str) -> str:
    letters = {
        'T': 'A',
        'J': 'B',
        'Q': 'C',
        'K': 'D',
        'A': 'E',
    }
    try:
        number = letters[char]
    except KeyError:
        number = char
    return number


def card_to_hex_with_joker(card: str) -> str:
    letters = {
        'T': 'A',
        'J': '1',
        'Q': 'C',
        'K': 'D',
        'A': 'E',
    }
    try:
        value = letters[card]
    except KeyError:
        value = card
    return value


def get_hex_from_hand(hand: Hand) -> int:
    cards, bid = hand
    hex_cards = [card_to_hex(card) for card in list(cards)]
    value = int(''.join(hex_cards), 16)
    return value


def get_hex_from_hand_with_joker(hand: Hand) -> int:
    cards, bid = hand
    hex_cards = [card_to_hex_with_joker(card) for card in list(cards)]
    value = int(''.join(hex_cards), 16)
    return value


def group_hands_by_type(list_of_hands: list[Hand]) -> dict[HandType, list[Hand]]:
    grouped_list_of_hands = {}
    for hand in list_of_hands:
        cards, bid = hand
        hand_type = filter_type(cards)
        if hand_type not in grouped_list_of_hands.keys():
            grouped_list_of_hands[hand_type] = []
        grouped_list_of_hands[hand_type].append(hand)
    return grouped_list_of_hands


def get_sorted_list_of_hands(grouped_list_of_hands: dict[HandType, list[Hand]], sorting_func) -> list[Hand]:
    list_of_hands = []
    for hand_type in reversed(HandType):
        if hand_type not in grouped_list_of_hands.keys():
            continue
        grouped_list_of_hands[hand_type].sort(key=sorting_func)
        for hand in grouped_list_of_hands[hand_type]:
            list_of_hands.append(hand)
    return list_of_hands


def calculate_total_winnings(list_of_hands: list[Hand]) -> int:
    total_winnings = 0
    for rank, hand in enumerate(list_of_hands, 1):
        cards, bid = hand
        winnings = rank * bid
        total_winnings += winnings
    return total_winnings


def first_part(data: str) -> int:
    list_of_hands = parse_data(data)
    grouped_list_of_hands = group_hands_by_type(list_of_hands)
    sorted_list_of_hands = get_sorted_list_of_hands(grouped_list_of_hands, sorting_func=get_hex_from_hand)
    total_winnings = calculate_total_winnings(sorted_list_of_hands)
    return total_winnings


def second_part(data: str) -> int:
    list_of_hands = parse_data(data)
    grouped_list_of_hands = group_hands_by_type(list_of_hands)
    sorted_list_of_hands = get_sorted_list_of_hands(grouped_list_of_hands, sorting_func=get_hex_from_hand_with_joker)
    total_winnings = calculate_total_winnings(sorted_list_of_hands)

    # for hand, bid in list_of_hands:
    #     hand_type = filter_type(get_best_hand(hand))
    #     _cards = [card_to_hex_with_joker(card) for card in list(hand)]
    #     value = int(''.join(_cards), 16)
    #     game = (hand, bid, value)
    #     if hand_type not in grouped_list_of_hands.keys():
    #         grouped_list_of_hands[hand_type] = []
    #     grouped_list_of_hands[hand_type].append(game)
    # list_of_hands = []
    # for hand_type in reversed(HandType):
    #     if hand_type not in grouped_list_of_hands.keys():
    #         continue
    #     ordered_hands = sorted(grouped_list_of_hands[hand_type], key=lambda items: items[2])
    #     for hand in ordered_hands:
    #         list_of_hands.append(hand)
    # total_winnings = 0
    # for index, hand in enumerate(list_of_hands):
    #     rank = index + 1
    #     bid = hand[1]
    #     winnings = rank * bid
    #     total_winnings += winnings
    return total_winnings

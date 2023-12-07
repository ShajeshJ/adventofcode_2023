from dataclasses import dataclass
from enum import Enum, auto
from utils import read_problem_input


CARD_LOOKUP = {
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class HandType(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIRS = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


@dataclass(frozen=True)
class HandAndBid:
    cards: list[int, int, int, int, int]
    bid: int
    hand_type: HandType

    def sort_key(self) -> tuple[int, int, int, int, int, int]:
        return (self.hand_type.value, *self.cards)


def get_hand_type(hand: list[int]) -> HandType:
    card_count: dict[int, int] = {}

    # get # of jokers and count of each card
    jokers = 0
    for card in hand:
        if card == 1:
            jokers += 1
        else:
            card_count[card] = card_count.get(card, 0) + 1
    count_of_each = list(card_count.values())

    # factor in jokers
    if jokers == 5:
        return HandType.FIVE_OF_A_KIND
    elif jokers > 0:
        idx = count_of_each.index(max(count_of_each))
        count_of_each[idx] += jokers

    # determine hand type
    if 5 in count_of_each:
        hand_type = HandType.FIVE_OF_A_KIND
    elif 4 in count_of_each:
        hand_type = HandType.FOUR_OF_A_KIND
    elif 3 in count_of_each:
        if 2 in count_of_each:
            hand_type = HandType.FULL_HOUSE
        else:
            hand_type = HandType.THREE_OF_A_KIND
    elif 2 in count_of_each:
        if count_of_each.count(2) == 2:
            hand_type = HandType.TWO_PAIRS
        else:
            hand_type = HandType.ONE_PAIR
    else:
        hand_type = HandType.HIGH_CARD

    return hand_type


def parse_hand_and_bid(s: str, joker_rules: bool = False) -> HandAndBid:
    hand_str, bid_str = s.split(" ")

    hand: list[int] = []
    for c in hand_str:
        if joker_rules and c == "J":
            hand.append(1)
        else:
            hand.append(CARD_LOOKUP.get(c) or int(c))

    return HandAndBid(hand, int(bid_str), get_hand_type(hand))


def part_1() -> str:
    hand_and_bids = (parse_hand_and_bid(line) for line in read_problem_input())
    ordered_hands = sorted(hand_and_bids, key=HandAndBid.sort_key)
    winnings = sum(hand.bid * i for i, hand in enumerate(ordered_hands, start=1))
    return str(winnings)


def part_2() -> str:
    hand_and_bids = (parse_hand_and_bid(line, joker_rules=True) for line in read_problem_input())
    ordered_hands = sorted(hand_and_bids, key=HandAndBid.sort_key)
    winnings = sum(hand.bid * i for i, hand in enumerate(ordered_hands, start=1))
    return str(winnings)

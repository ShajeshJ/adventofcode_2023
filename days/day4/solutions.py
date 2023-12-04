from dataclasses import dataclass
from typing import Callable, Self

from utils import read_problem_input


@dataclass
class Card:
    _id: int
    winners: set[int]
    owned: list[int]

    @classmethod
    def from_str(cls, s: str) -> Self:
        id_str, s = s.replace("Card ", "").split(":")
        _id = int(id_str)
        s = s.strip()
        winners_str, owned_str = s.split(" | ")
        winners = {int(num) for num in winners_str.split(" ") if num}
        owned = [int(num) for num in owned_str.split(" ") if num]
        return cls(_id, winners, owned)

    def get_num_winners(self) -> int:
        return sum(1 for num in self.owned if num in self.winners)

def part_1() -> str:
    cards = (Card.from_str(s) for s in read_problem_input())
    win_counts = (card.get_num_winners() for card in cards)
    total = sum(2**(num_wins - 1) if num_wins > 0 else 0 for num_wins in win_counts)
    return str(total)

def part_2() -> str:
    cards = (Card.from_str(s) for s in read_problem_input())
    all_cards = {card._id: (card, 1) for card in cards}

    for id in all_cards:
        card, num_instances = all_cards[id]
        num_wins = card.get_num_winners()

        for i in range(id+1, id+num_wins+1):
            card_i, num_instances_i = all_cards[i]
            all_cards[i] = (card_i, num_instances_i + num_instances)

    return str(sum(c[1] for c in all_cards.values()))

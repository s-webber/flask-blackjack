import random
from collections import namedtuple

Rank = namedtuple('Rank', 'name value')
Card = namedtuple('Card', 'rank suit')


class Deck:
    """
    Represents a deck of cards.
    """

    def __init__(self, cards):
        self.cards = cards

    def deal(self):
        """
        Removes and returns the next card from the deck.
        """
        return self.cards.pop()


ranks = [
    Rank("2", 2),
    Rank("3", 3),
    Rank("4", 4),
    Rank("5", 5),
    Rank("6", 6),
    Rank("7", 7),
    Rank("8", 8),
    Rank("9", 9),
    Rank("T", 10),
    Rank("J", 10),
    Rank("Q", 10),
    Rank("K", 10),
    Rank("A", 11)
]

suits = ["S", "H", "D", "C"]

all_cards = [Card(rank, suit) for rank in ranks for suit in suits]


def new_deck():
    """
    Returns a new Deck instance.
    """
    deck = all_cards.copy()
    random.shuffle(deck)
    return Deck(deck)

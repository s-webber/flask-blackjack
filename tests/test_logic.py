from blackjack.logic import Game
from blackjack.deck import all_cards, Card, Deck
from blackjack.exceptions import GameNotOpenException
import pytest


dummy_game_id = 'dummy-game-id'


def test_initial_state():
    game_id = 'test-initial-state-game-id'
    deck = parse_deck("JS 7C 9D")
    g = Game(game_id, deck)
    assert g.get_state() == {
        'game_id': game_id,
        'status': 'OPEN',
        'dealer': {'hand': ['JS'], 'score': 10},
        'player': {'hand': ['7C', '9D'], 'score': 16}
    }


def test_both_have_21_not_blackjack():
    g = Game(dummy_game_id, parse_deck("7S TH 3S 4S 4C 7H 7D"))
    g.hit()
    g.hit()
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'DRAW',
        'dealer': {'hand': ['7S', '7H', '7D'], 'score': 21},
        'player': {'hand': ['TH', '3S', '4S', '4C'], 'score': 21}
    }


def test_both_have_17():
    g = Game(dummy_game_id, parse_deck("7D TH 7H TD"))
    g.stand()
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'DRAW',
        'dealer': {'hand': ['7D', 'TD'], 'score': 17},
        'player': {'hand': ['TH', '7H'], 'score': 17}
    }


def test_player_has_18_dealer_has_17():
    g = Game(dummy_game_id, parse_deck("7D TH 8H TD"))
    g.stand()
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'WIN',
        'dealer': {'hand': ['7D', 'TD'], 'score': 17},
        'player': {'hand': ['TH', '8H'], 'score': 18}
    }


def test_player_has_18_dealer_has_19():
    g = Game(dummy_game_id, parse_deck("9D TH 8H TD"))
    g.stand()
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'LOSE',
        'dealer': {'hand': ['9D', 'TD'], 'score': 19},
        'player': {'hand': ['TH', '8H'], 'score': 18}
    }


def test_player_has_15_dealer_bust():
    g = Game(dummy_game_id, parse_deck("7D TH 5H 9D 6D"))
    g.stand()
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'WIN',
        'dealer': {'hand': ['7D', '9D', '6D'], 'score': 22},
        'player': {'hand': ['TH', '5H'], 'score': 15}
    }


def test_player_has_16_dealer_bust():
    g = Game(dummy_game_id, parse_deck("7D TH 6H 9D 6D"))
    g.stand()
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'WIN',
        'dealer': {'hand': ['7D', '9D', '6D'], 'score': 22},
        'player': {'hand': ['TH', '6H'], 'score': 16}
    }


def test_player_bust():
    g = Game(dummy_game_id, parse_deck("2C TH TD 2S"))
    g.hit()
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'LOSE',
        'dealer': {'hand': ['2C'], 'score': 2},
        'player': {'hand': ['TH', 'TD', '2S'], 'score': 22}
    }


def test_dealer_continues_until_17():
    g = Game(dummy_game_id, parse_deck("2S TD 4D 2H 2D 2C 3S 3H 3D"))
    g.stand()
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'LOSE',
        'dealer': {'hand': ['2S', '2H', '2D', '2C', '3S', '3H', '3D'], 'score': 17},
        'player': {'hand': ['TD', '4D'], 'score': 14}
    }


def test_dealer_bust():
    g = Game(dummy_game_id, parse_deck("TH TD 4D 5H 7H"))
    g.stand()
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'WIN',
        'dealer': {'hand': ['TH', '5H', '7H'], 'score': 22},
        'player': {'hand': ['TD', '4D'], 'score': 14}
    }


def test_player_has_blackjack_dealer_has_2():
    g = Game(dummy_game_id, parse_deck("2C AS KH"))
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'WIN',
        'dealer': {'hand': ['2C'], 'score': 2},
        'player': {'hand': ['AS', 'KH'], 'score': 21}
    }


def test_player_has_blackjack_dealer_has_9():
    g = Game(dummy_game_id, parse_deck("9C AS KH"))
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'WIN',
        'dealer': {'hand': ['9C'], 'score': 9},
        'player': {'hand': ['AS', 'KH'], 'score': 21}
    }


def test_dealer_has_blackjack():
    g = Game(dummy_game_id, parse_deck("KH 7D 3H 8C AS"))
    g.hit()
    g.stand()
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'LOSE',
        'dealer': {'hand': ['KH', 'AS'], 'score': 21},
        'player': {'hand': ['7D', '3H', '8C'], 'score': 18}
    }


def test_player_has_blackjack_dealer_has_ace():
    g = Game(dummy_game_id, parse_deck("AS AC TC 4C"))
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'WIN',
        'dealer': {'hand': ['AS', '4C'], 'score': 15},
        'player': {'hand': ['AC', 'TC'], 'score': 21}
    }


def test_player_has_blackjack_dealer_has_ten():
    g = Game(dummy_game_id, parse_deck("TS AC TC 4C"))
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'WIN',
        'dealer': {'hand': ['TS', '4C'], 'score': 14},
        'player': {'hand': ['AC', 'TC'], 'score': 21}
    }


def test_player_has_21_dealer_has_blackjack():
    g = Game(dummy_game_id, parse_deck("AS 9S 4S 8S TS"))
    g.hit()
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'LOSE',
        'dealer': {'hand': ['AS', 'TS'], 'score': 21},
        'player': {'hand': ['9S', '4S', '8S'], 'score': 21}
    }


def test_both_have_blackjack():
    g = Game(dummy_game_id, parse_deck("KH AS TD AC"))
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'DRAW',
        'dealer': {'hand': ['KH', 'AC'], 'score': 21},
        'player': {'hand': ['AS', 'TD'], 'score': 21}
    }


def test_cannot_update_after_stand():
    g = Game(dummy_game_id, parse_deck("9D TH 7H TD"))
    g.stand()
    assert_cannot_update(g)
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'LOSE',
        'dealer': {'hand': ['9D', 'TD'], 'score': 19},
        'player': {'hand': ['TH', '7H'], 'score': 17}
    }


def test_cannot_update_after_bust():
    g = Game(dummy_game_id, parse_deck("9D TH 5H 7H"))
    g.hit()
    assert_cannot_update(g)
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'LOSE',
        'dealer': {'hand': ['9D'], 'score': 9},
        'player': {'hand': ['TH', '5H', '7H'], 'score': 22}
    }


def test_cannot_update_after_reached_target():
    g = Game(dummy_game_id, parse_deck("9D TH 5H 6H 8D"))
    g.hit()
    assert_cannot_update(g)
    assert g.get_state() == {
        'game_id': dummy_game_id,
        'status': 'WIN',
        'dealer': {'hand': ['9D', '8D'], 'score': 17},
        'player': {'hand': ['TH', '5H', '6H'], 'score': 21}
    }


def assert_cannot_update(g):
    with pytest.raises(GameNotOpenException):
        g.hit()
    with pytest.raises(GameNotOpenException):
        g.stand()


def test_parse_deck():
    deck = parse_deck("AS JC 9D")

    card = deck.deal()
    assert type(card) == Card
    assert card.rank.name == 'A'
    assert card.suit == 'S'

    card = deck.deal()
    assert card.rank.name == 'J'
    assert card.suit == 'C'

    card = deck.deal()
    assert card.rank.name == '9'
    assert card.suit == 'D'

    with pytest.raises(IndexError):
        deck.deal()


def parse_deck(card_ids):
    """
    Creates and returns a Deck consisting of the cards represented by the given string.
    """
    cards = []

    while card_ids:
        rank = card_ids[0]
        suit = card_ids[1]
        assert not card_ids[2:3].strip()
        card = next(c for c in all_cards if c.rank.name == rank and c.suit == suit)
        cards.append(card)
        card_ids = card_ids[3:]

    cards.reverse()
    return Deck(cards)

import blackjack.deck
import pytest


def test_new_deck_has_52_cards():
    deck = blackjack.deck.new_deck()
    for i in range(52):
        deck.deal()
    with pytest.raises(IndexError):
        deck.deal()


def test_new_deck_has_all_cards():
    deck = blackjack.deck.new_deck()
    cards = [deck.deal() for i in range(52)]
    card_ids = [card.rank.name + card.suit for card in cards]
    card_ids.sort()
    assert card_ids == [
        '2C', '2D', '2H', '2S',
        '3C', '3D', '3H', '3S',
        '4C', '4D', '4H', '4S',
        '5C', '5D', '5H', '5S',
        '6C', '6D', '6H', '6S',
        '7C', '7D', '7H', '7S',
        '8C', '8D', '8H', '8S',
        '9C', '9D', '9H', '9S',
        'AC', 'AD', 'AH', 'AS',
        'JC', 'JD', 'JH', 'JS',
        'KC', 'KD', 'KH', 'KS',
        'QC', 'QD', 'QH', 'QS',
        'TC', 'TD', 'TH', 'TS'
    ]


def test_not_pure():
    """
    Confirm that different decks return the same cards but in a different order.
    """
    first_deck = blackjack.deck.new_deck()
    first_cards = [first_deck.deal() for _ in range(52)]
    second_deck = blackjack.deck.new_deck()
    second_cards = [second_deck.deal() for _ in range(52)]
    assert first_cards != second_cards

    first_cards.sort()
    second_cards.sort()
    assert first_cards == second_cards


def test_new_deck_shuffle(mocker):
    shuffle_invocation_ctr = 0

    def shuffle_side_effect(unshuffled_cards):
        nonlocal shuffle_invocation_ctr
        shuffle_invocation_ctr += 1
        unshuffled_card_ids = [card.rank.name + card.suit for card in unshuffled_cards]
        assert unshuffled_card_ids == [
            '2S', '2H', '2D', '2C',
            '3S', '3H', '3D', '3C',
            '4S', '4H', '4D', '4C',
            '5S', '5H', '5D', '5C',
            '6S', '6H', '6D', '6C',
            '7S', '7H', '7D', '7C',
            '8S', '8H', '8D', '8C',
            '9S', '9H', '9D', '9C',
            'TS', 'TH', 'TD', 'TC',
            'JS', 'JH', 'JD', 'JC',
            'QS', 'QH', 'QD', 'QC',
            'KS', 'KH', 'KD', 'KC',
            'AS', 'AH', 'AD', 'AC'
        ]
        unshuffled_cards.reverse()

    mocker.patch('random.shuffle', side_effect=shuffle_side_effect)
    deck = blackjack.deck.new_deck()
    cards = [deck.deal() for _ in range(52)]
    card_ids = [card.rank.name + card.suit for card in cards]
    assert shuffle_invocation_ctr == 1
    assert card_ids == [
        '2S', '2H', '2D', '2C',
        '3S', '3H', '3D', '3C',
        '4S', '4H', '4D', '4C',
        '5S', '5H', '5D', '5C',
        '6S', '6H', '6D', '6C',
        '7S', '7H', '7D', '7C',
        '8S', '8H', '8D', '8C',
        '9S', '9H', '9D', '9C',
        'TS', 'TH', 'TD', 'TC',
        'JS', 'JH', 'JD', 'JC',
        'QS', 'QH', 'QD', 'QC',
        'KS', 'KH', 'KD', 'KC',
        'AS', 'AH', 'AD', 'AC'
    ]

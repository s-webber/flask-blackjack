import blackjack.cache
import pytest


@pytest.fixture
def game_store():
    return blackjack.cache.GameStore()


def test_get_ids_empty(game_store):
    assert [] == game_store.get_ids()


def test_get_ids_populated(game_store):
    game1 = game_store.create_game()
    game2 = game_store.create_game()
    game3 = game_store.create_game()
    assert [game1.game_id, game2.game_id, game3.game_id] == game_store.get_ids()


def test_retrieve_game_unknown_id(game_store):
    with pytest.raises(blackjack.cache.GameNotFoundException):
        game_store.retrieve_game("unknown id")


def test_retrieve_game_known_id(game_store):
    game = game_store.create_game()
    assert game is game_store.retrieve_game(game.game_id)


def test_create_game_unique_ids(game_store):
    game1 = game_store.create_game()
    game2 = game_store.create_game()
    assert game1.game_id != game2.game_id


def test_create_game_uses_uuid(mocker, game_store):
    mocker.patch('uuid.uuid1', return_value='dummy uuid')
    game = game_store.create_game()
    assert game.game_id == 'dummy uuid'

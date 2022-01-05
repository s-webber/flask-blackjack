from blackjack.logic import Game
from blackjack.deck import new_deck
from blackjack.exceptions import GameNotFoundException
import uuid


class GameStore:
	"""
	A repository of blackjack games.
	"""

	def __init__(self):
		self.game_cache = {}

	def get_ids(self):
		"""
		Returns all game IDs in the store.
		"""
		return list(self.game_cache)

	def create_game(self):
		"""
		Creates a new game, adds it to the store and returns it.
		"""
		game_id = str(uuid.uuid1())
		deck = new_deck()
		new_game = Game(game_id, deck)
		self.game_cache[game_id] = new_game
		return new_game

	def retrieve_game(self, game_id):
		"""
		Returns the game from the store with given game ID.
		"""
		try:
			return self.game_cache[game_id]
		except KeyError:
			raise GameNotFoundException(game_id)

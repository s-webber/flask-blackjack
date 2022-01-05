import threading

from blackjack.exceptions import GameNotOpenException

ace_high_value = 14
ace_low_value = 1
target_value = 21
dealer_target_value = 17


def calculate_hand_value(hand):
	hand_value = 0
	aces = 0
	for card in hand:
		rank = card.rank.value
		if __is_ace(rank):
			aces += 1
		hand_value += rank
	return __treat_ace_as_low_if_necessary(hand_value, aces)


def __is_ace(rank):
	return rank == 14


def __treat_ace_as_low_if_necessary(hand_value, aces):
	while aces > 0 and is_bust(hand_value):
		hand_value -= ace_high_value - ace_low_value
		aces -= 1
	return hand_value


def is_bust(hand_value):
	return hand_value > target_value


def is_blackjack(hand):
	return len(hand) == 2 and calculate_hand_value(hand) == target_value


def is_target(hand):
	return calculate_hand_value(hand) == target_value


class Game:
	"""
	Represents a blackjack game.
	"""

	def __init__(self, game_id, deck):
		self.game_id = game_id
		self.deck = deck
		self.dealer = []
		self.player = []
		self.status = 'OPEN'
		self.lock = threading.Lock()

		self.__deal(self.dealer)
		self.__deal(self.player)
		self.__deal(self.player)

		self._post_update()

	def hit(self):
		with self.lock:
			self.__assert_is_open()
			self.__deal(self.player)
			self._post_update()

	def stand(self):
		with self.lock:
			self.__assert_is_open()
			self.status = 'DEALERS_TURN'
			self._post_update()

	def _post_update(self):
		if is_blackjack(self.player):
			self.__handle_player_blackjack()
		elif is_bust(calculate_hand_value(self.player)):
			self.status = 'LOSE'
		elif self.__is_dealers_turn():
			self.__play_dealer()
			self.__set_game_outcome()

	def __handle_player_blackjack(self):
		dealers_card = self.dealer[0]
		if dealers_card.rank.value > 9:
			self.__deal(self.dealer)
			self.__set_game_outcome()
		else:
			self.status = 'WIN'

	def __is_dealers_turn(self):
		return self.status == 'DEALERS_TURN' or is_target(self.player)

	def __assert_is_open(self):
		if self.status != 'OPEN':
			raise GameNotOpenException(str(self.game_id) + ' ' + self.status)

	def __deal(self, hand):
		hand.append(self.deck.deal())

	def __play_dealer(self):
		while calculate_hand_value(self.dealer) < dealer_target_value:
			self.__deal(self.dealer)

	def __set_game_outcome(self):
		dealer_value = calculate_hand_value(self.dealer)
		player_value = calculate_hand_value(self.player)
		if dealer_value > target_value or player_value > dealer_value:
			self.status = 'WIN'
		elif player_value < dealer_value:
			self.status = 'LOSE'
		else:
			player_has_blackjack = is_blackjack(self.player)
			dealer_has_blackjack = is_blackjack(self.dealer)
			if player_has_blackjack == dealer_has_blackjack:
				self.status = 'DRAW'
			elif dealer_has_blackjack:
				self.status = 'LOSE'
			else:
				# sanity check - if player has blackjack then it should not be possible for the dealer to reach 21 with
				# more than 2 cards, as dealer will stop dealing themselves card once they know they cannot win, so the
				# branch of the code should never be executed
				raise Exception()

	def get_state(self):
		return {
			"game_id": self.game_id,
			"status": self.status,
			"dealer": {
				"hand": [card.rank.name + card.suit for card in self.dealer],
				"score": calculate_hand_value(self.dealer)
			},
			"player": {
				"hand": [card.rank.name + card.suit for card in self.player],
				"score": calculate_hand_value(self.player)
			}
		}

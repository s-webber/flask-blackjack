"""
This module implements an API for playing the blackjack card game.
"""
from flask import Flask, abort, jsonify, request, Response
import blackjack.cache as cache
from blackjack.exceptions import BlackjackException

urlPrefix = "/blackjack"
game_store = cache.GameStore()

app = Flask(__name__)


@app.route(urlPrefix, methods=['GET'])
def list():
	"""Returns IDs of games belonging to the given user.
	
	All games for the given user, regardless of if they have already been completed, will be returned.
	"""
	return jsonify(game_store.get_ids())


@app.route(urlPrefix, methods=['POST'])
def create():
	"""Creates a new game.
	
	Two cards will automatically be dealt to the player and one to the dealer. If the player has blackjack then the game will immediately move to a completed state.
	"""
	game = game_store.create_game()
	return jsonify(game.get_state()), 201


@app.route(urlPrefix + "/<game_id>", methods=['GET'])
def retrieve(game_id):
	"""Retrieves the state of an existing game.
	
	Returns a snapshot of the current stage of a game.
	"""
	game = game_store.retrieve_game(game_id)
	return game.get_state()


@app.route(urlPrefix + "/<game_id>", methods=['POST'])
def update(game_id):
	"""Updates an existing game.
	
	A game will only be updatable if its current status is PLAYERS_TURN.
	"""
	action = request.form.get('action')
	game = game_store.retrieve_game(game_id)

	if action == 'HIT':
		game.hit()
	elif action == 'STAND':
		game.stand()
	else:
		abort(Response('invalid action', 422))

	return game.get_state()


@app.errorhandler(BlackjackException)
def handle_bad_request(e):
	return type(e).__name__ + ' ' + str(e), 422

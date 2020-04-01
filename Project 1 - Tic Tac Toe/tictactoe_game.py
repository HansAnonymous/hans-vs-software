# Adapated from https://github.com/Cledersonbc/tic-tac-toe-minimax
# Minimax algorithm: https://en.wikipedia.org/wiki/Minimax
from math import inf
from random import choice
from copy import deepcopy

class TicTacToe():
	def __init__(self):
		self.HUMAN = -1
		self.COMP = +1
		self.PLAYERONE = 1
		self.PLAYERTWO = 2
		self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

	def get_board(self):
		return self.board

	def print_board(self):
		print("---------------")
		for row in self.board:
			print(row)

	def restart_game(self):
		self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

	def check_win(self, state, player):
		# Can win by row (3), col (3) or diag (2)
		# param player: Which player is to be checked
		# return True if that player won
		b = state # board b
		win_state = [
			[b[0][0], b[0][1], b[0][2]], # row 1
			[b[1][0], b[1][1], b[1][2]], # row 2
			[b[2][0], b[2][1], b[2][2]], # row 3
			[b[0][0], b[1][0], b[2][0]], # col 1
			[b[0][1], b[1][1], b[2][1]], # col 2
			[b[0][2], b[1][2], b[2][2]], # col 3
			[b[0][0], b[1][1], b[2][2]], # diag 1
			[b[2][0], b[1][1], b[0][2]], # diag 2
		]

		return True if [player, player, player] in win_state else False

	def game_over(self, state):
		# return True if one player won
		return self.check_win(state, self.PLAYERONE) or self.check_win(state, self.PLAYERTWO)


	def get_empty_cells(self, state):
		cells = []

		for x, row in enumerate(state):
			for y, cell in enumerate(row):
				if cell == 0:
					cells.append([x, y])
		return cells

	def check_valid_move(self, x, y):
		# params x: X coord; y: Y coord
		# return True if the coordinate in board is empty
		return True if [x, y] in self.get_empty_cells(self.board) else False

	def minimaximize(self, state, player):
		# params state: state of the board
		# 		 player: player to be converted (PLAYERONE || PLAYERTWO)
		# return a board in minimax format
		for x, row in enumerate(state):
			for y, cell in enumerate(row):
				if cell == player:
					state[x][y] = self.COMP
				elif cell == 0:
					state[x][y] = 0
				else:
					state[x][y] = self.HUMAN
		return state

	def evaluate(self, state):
		# get heuristic evaluation of the board
		# param state, state of the board to be evaluated
		# return +1 if computer won; -1 if human won; 0 if draw
		if self.check_win(state, self.COMP):
			score = +1
		elif self.check_win(state, self.HUMAN):
			score = -1
		else:
			score = 0
		return score

	def minimax(self, state, depth, player):
		# AI algorithm
		# params state: current state of board;
		#		 depth: node index in tree
		#		 player: human or computer
		# return list: [ideal row, ideal col, ideal score]
		# set "scores"
		if player == self.COMP:
			best = [-1, -1, -inf]
		else:
			best = [-1, -1, +inf]
		
		# Base case
		if depth == 0 or self.game_over(state):
			score = self.evaluate(state)
			return [-1, -1, score]

		for cell in self.get_empty_cells(state):
			x, y = cell[0], cell[1]
			state[x][y] = player
			score = self.minimax(state, depth - 1, -player)
			state[x][y] = 0
			score[0], score[1] = x, y

			if player == self.COMP:
				if score[2] > best[2]:
					best = score # max
			else:
				if score[2] < best[2]:
					best = score # min
		return best

	def play_move(self, x, y, player):
		# params x: X coord; y: Y coord; player: player to move
		# return True if successfully played
		if self.check_valid_move(x, y):
			self.board[x][y] = player
			return True
		else:
			return False

	def ai_move(self, player):
		# minimax function is used where depth < 9
		# else choose random coordinate
		# params player: PLAYERONE || PLAYERTWO
		depth = len(self.get_empty_cells(self.board))
		if depth == 0 or self.game_over(self.board):
			return

		if depth == 9:
			x = choice([0, 1, 2])
			y = choice([0, 1, 2])
		else:
			state = self.minimaximize(deepcopy(self.board), player)
			move = self.minimax(state, depth, self.COMP)
			x, y = move[0], move[1]

		self.play_move(x, y, player)

	def player_move(self, player, x, y):
		# Play with valid move
		# params c_choice: PLAYERONE || PLAYERTWO
		depth = len(self.get_empty_cells(self.board))
		if depth == 0 or self.game_over(self.board):
			return

		self.play_move(x, y, player)

from Heuristic import heuristic

player = 0
AI = 1
AI_PIECE = 2
PLAYER_PIECE = 1
empty=0

class GameState:
	""""Class that represents a state of the game
	
	Responsible for storing the state of the game, finding all possible moves,
	
	and predicting the score of this state.
	"""
	state: int = 0 #How should we represent the state of the board

	def __init__(self, state: int) -> None:
		self.state = state

	#Public methods

	#Uses the heuristic function to predict the score of this state.
	def predict_score(self) -> int:
		"""Uses a heuristic function to predict the score of this state"""
		return heuristic(self)
	
	
	def get_next_states(self, turn) -> list:
		"""Gets all possible next states of the game in a dictionary.

		Keys correspond to a move, and values correspond to the state reached by applying the move"""
		child_states = []
		for i in range(7):
			child_state = self.get_child_state(i, turn)
			if child_state is not None:
				child = GameState(child_state)
				child_states.append(child)
		return child_states

	def convert_to_matrix(self):
		matrix = [[0 for i in range(7)] for j in range(6)]
		print(matrix)
		mask = 0b111111111
		for i in range(7):
			col = (self.state >> 9 * i) & mask
			pieces_num = 3 & col
			col = col >> 3
			print(pieces_num)
			for j in range(pieces_num):
				if col & 1 == 1:
					matrix[5 - j][i] = 2
				else:
					matrix[5 - j][i] = 1
				col = col >> 1
		return matrix

	def __set_bit(self, bit):
		return self.state | (1 << bit)

	def __clear_bit(self, bit):
		return self.state & ~(1 << bit)

	def __get_pieces_num(self, col):
		return (self.state & (3 << col * 9)) >> col * 9

	def __increase_pieces_num(self, col):
		return self.state + (1 << col * 9)

	def get_child_state(self, col, turn):
		pieces_num = self.__get_pieces_num(col)
		if pieces_num == 7:
			return None
		bit_num = (pieces_num + 3) + 9 * col
		child_state = GameState(self.__increase_pieces_num(col))
		if turn:
			return child_state.__set_bit(bit_num)
		else:
			return child_state.__clear_bit(bit_num)








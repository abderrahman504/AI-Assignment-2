from typing import Self

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
		pass
	
	
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
		matrix = [[None for i in range(7)] for j in range(6)]
		print(matrix)
		mask = 0b111111111
		for i in range(7):
			col = (self.state >> 9 * i) & mask
			pieces_num = 3 & col
			col = col >> 3
			print(pieces_num)
			for j in range(pieces_num):
				if col & 1 == 1:
					matrix[5 - j][i] = True
				else:
					matrix[5 - j][i] = False
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



class Node:
	"""Class used to form the tree structure.

	Responsible for navigating the tree and evaluating a state's score.
	"""
	parent: Self = None
	value: GameState
	score: int
	children: dict = None

	def __init__(self, value: GameState) -> None:
		self.value = value

	#Public methods

	def get_child(self, move: int) -> Self:
		"""Returns this node's child"""
		return self.children[move]
	

	def expand_to_depth(self, depth: int, a_b_pruning: bool) -> None:
		"""Expands this node and its children until a certain depth is reached"""
		"""if self.children is None: self._build_children()
		if k == 1: 
			for k,v in self.children: v._build_score()
		else:
			for k,v in self.children:
				v.expand_to_depth(depth-1)
		self._build_score()"""

	#Private methods

	def _build_children(self) -> None:
		"""Expands this node by creating its child nodes"""
		states: dict = self.value.get_next_states()
		for k, v in states:
			self.children[k] = Node(v)
	

	def _build_score(self) -> None:
		"""Evaluates this node's score using minmax function with pruning"""
		if self.children is None:
			score = self.value.predict_score()
		else: #This isn't a leaf node so use minmax to set score.
			pass



class GameTree:
	root: Node
	selected: Node
	k: int
	a_b_pruning: bool

	def __init__(self,aiFirst: bool, k: int, pruning: bool) -> None:
		emptyBoard: GameState = GameState(0)
		self.root = Node(emptyBoard)
		self.selected = self.root
		self.a_b_pruning = pruning
	
	#Public Methods

	#Apply
	def apply_move(self, move:int) -> None:
		"""Applies a move to the game tree and progresses the selected node"""
		self.selected = self.selector.get_child(move)
		self.selected.expand_to_depth(self.k, self.a_b_pruning)
		self._update_scores()

	#Private Methods
	
	def _update_scores(self) -> None:
		"""Re-evaluates the scores of all parent nodes of the selected node.
		
		Should be used whenever the tree is expanded """	
		current: Node = self.selector.parent
		while current != self.root:
			current.set_score()
			current = current.parent
	

	
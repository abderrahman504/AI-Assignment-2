from typing import Self


emptyBoardMatrix = []
for i in range(6):
	row = []
	for j in range(7):
		row.append(None)
	emptyBoardMatrix.append(row)


class GameState:
	""""Class that represents a state of the game
	
	Responsible for storing the state of the game, finding all possible moves,
	
	and predicting the score of this state.
	"""
	state = 0 #How should we represent the state of the board
	aiPlaying: bool

	def __init__(self, aiPlaying: bool, state: list = emptyBoardMatrix) -> None:
		self.state = state
		self.aiPlaying = aiPlaying

	#Public methods

	#Uses the heuristic function to predict the score of this state.
	def predict_score(self) -> int:
		"""Uses a heuristic function to predict the score of this state"""
		pass
	
	def get_next_states(self) -> dict:
		"""Gets all possible next states of the game in a dictionary.
		
		Keys correspond to a move, and values correspond to the state reached by applying the move"""
		pass



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
	

	def expand_to_depth(self, depth: int, a_b_pruning: bool):
		"""Expands this node and its children until a certain depth is reached"""
		if self.children is None: self._build_children()
		if k == 1: 
			for k,v in self.children: v._build_score()
		else:
			for k,v in self.children:
				v.expand_to_depth(depth-1)
		self._build_score()

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
		emptyBoard: GameState = GameState(aiFirst)
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
	

	
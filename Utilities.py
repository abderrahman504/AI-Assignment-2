
emptyBoardMatrix = []
for i in range(6):
	row = []
	for j in range(7):
		row.append(None)
	emptyBoardMatrix.append(row)


class GameState:
	state = 0 #How should we represent the state of the board
	aiPlaying: bool

	def __init__(self, aiPlaying: bool, state: list = emptyBoardMatrix) -> None:
		self.state = state
		self.aiPlaying = aiPlaying

	#Public methods

	#Uses the heuristic function to predict the score of this state.
	def predict_score(self) -> int:
		pass
	
	def get_next_states(self) -> dict:
		pass



class Node:
	parent = None
	value: GameState
	score: int
	children: dict = None

	def __init__(self, value: GameState) -> None:
		self.value = value

	#Public methods

	def get_child(self, move: int):
		return self.children[move]
	
	def expand_to_depth(self, depth: int):
		if self.children is None: self.build_children()
		if k == 1: 
			for k,v in self.children: v.set_score()
		else:
			for k,v in self.children:
				v.expand_to_depth(depth-1)
		self.set_score()

	#Private methods

	def build_children(self) -> None:
		states: dict = self.value.get_next_states()
		for k, v in states:
			self.children[k] = Node(v)
	

	def set_score(self) -> None:
		if self.children is None:
			score = self.value.predict_score()
		else: #This isn't a leaf node so use minmax to set score.
			pass



class Tree:
	root: Node
	selected: Node
	k: int

	def __init__(self,aiFirst: bool, k: int) -> None:
		#Create initial board state and store it in root
		emptyBoard: GameState = GameState(aiFirst)
		self.root = Node(emptyBoard)
		self.selected = self.root
	
	#Public Methods

	def apply_move(self, move:int) -> None:
		self.selected = self.selector.get_child(move)
		self.selected.expand_to_depth(self.k)
		self.update_scores()

	#Private Methods
	
	def update_scores(self) -> None:
		current: Node = self.selector.parent
		while current != self.root:
			current.set_score()
			current = current.parent
	

	
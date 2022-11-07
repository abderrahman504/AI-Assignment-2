


class GameState:
	state = 0 #How should we represent the state of the board
	aiPlaying: bool
	score: int


	def predict_score(self) -> int:
		pass
	

	def get_next_states(self) -> list:
		pass



class Node:
	value: GameState
	children: list



class Tree:
	root: Node
	selected: Node

	def __init__(self,aiFirst: bool) -> None:
		self.root = Node()
		self.selected = self.root


	
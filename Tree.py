from __future__ import annotations
from Utilities import GameState


class TreeNode:
	"""
	Class used to form the tree structure.
	"""
	__value: GameState
	__score: int
	__children: list


	def __init__(self, value: GameState) -> None:
		self.__value = value
		self.__children=[]

	def get_value(self):
		return self.__value

	def add_child(self, child: TreeNode):
		"""Expands this node by creating its child nodes"""
		self.__children.append(child)

	def get_children(self):
		"""Returns this node's child"""
		return self.__children

	def set_score(self, score):
		self.__score = score

	def get_score(self):
		return self.__children



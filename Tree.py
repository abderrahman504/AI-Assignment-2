from __future__ import annotations


class TreeNode:
	"""
	Class used to form the tree structure.
	"""
	__score: int
	__children:[]
	__indx = 0


	def __init__(self, ) -> None:
		self.__children=[ None for i in range(7)]

	def get_value(self):
		#return self.__value
		return str(self.__score)

	def add_child(self, child: TreeNode):
		"""Expands this node by creating its child nodes"""
		print(self.__indx)
		self.__children[self.__indx] = child
		self.__indx += 1

	def get_children(self):
		"""Returns this node's child"""
		return self.__children

	def set_score(self, score):
		self.__score = score

	def get_score(self):
		return self.__children



from __future__ import annotations
from Utilities import GameState

import pydot

from IPython.display import Image, display

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

	def display(self,root: TreeNode, indent=0):
		#level = indent
		print((' ' * indent) + str(root.get_value()))
		for c in root.get_children():
			drawnode()
			c.display(c,indent + 1)
	def displaygui(self,G,root: TreeNode, indent=0):

		#level = indent
		print((' ' * indent) + str(root.get_value()))
		rootNode = pydot.Node(root.get_value(), style="filled", fillcolor="green")
		G.add_node(rootNode)
		for c in root.get_children():
			drawnode(G,root,c)
			c.displaygui(G,c,indent+1) 
        
        
        
        
        

	def printtree(self,root:TreeNode): 
        
		G = pydot.Dot(graph_type="digraph")
		self.displaygui(G,root)
		im = Image(G.create_png())
		display(im)



def drawnode(G,parentnode:TreeNode,childnode:TreeNode):
		node = pydot.Node(childnode.get_value(), style="filled", fillcolor="green")
		G.add_node(node)
		edge = pydot.Edge(parentnode.get_value(), childnode.get_value())
		G.add_edge(edge)
from Tree import TreeNode
import pydot

from IPython.display import Image, display



root = TreeNode(45)        #45
                #55      #42     #33
            #15   #20  #22

child_node55 = TreeNode(55)
child_node42 = TreeNode(42)
child_node33 = TreeNode(33)
child_node15 = TreeNode(15)
child_node20 = TreeNode(20)
child_node22 = TreeNode(22)
root.add_child(child_node55)
root.add_child(child_node42)
root.add_child(child_node33)
child_node55.add_child(child_node15)
child_node55.add_child(child_node20)
child_node42.add_child(child_node22)
def displaygui(G,root: TreeNode, indent=0):
		print((' ' * indent) + str(root.get_value()))
		rootNode = pydot.Node(root.get_value(), style="filled", fillcolor="cyan")
		G.add_node(rootNode)
		for c in root.get_children():
			drawnode(G,root,c)
			displaygui(G,c,indent+1) 

		#level = indent

        
        
        
        
        

def printtree(root:TreeNode):
		G = pydot.Dot(graph_type="digraph")
		displaygui(G,root)
		im = Image(G.create_png())
		display(im)

def drawnode(G,parentnode:TreeNode,childnode:TreeNode):
		node = pydot.Node(childnode.get_value(), style="filled", fillcolor="cyan")
		G.add_node(node)
		edge = pydot.Edge(parentnode.get_value(), childnode.get_value())
		G.add_edge(edge)
    


printtree(root)




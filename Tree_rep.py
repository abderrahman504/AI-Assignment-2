from Tree import TreeNode
import pydot
from IPython.display import Image, display
from tkinter import *
from Utilities import GameState
from Minimax import minimax
import pygame
nodeid=0

from PIL import Image, ImageTk

x = GameState(0)
t = TreeNode(x)
y, z = minimax(x, 0, True, 4,  t)
mat = z.convert_to_matrix()
for i in mat:
    print(i)
print(y)

"""""""""""
root = TreeNode(45)  # 45
# 55      #42     #33
# 15   #20  #22

child_node55 = TreeNode(55)
child_node42 = TreeNode(42)
child_node33 = TreeNode(33)
child_node15 = TreeNode(15)
child_node20 = TreeNode(20)
child_node22 = TreeNode(22)
child_node552 = TreeNode(55)
child_node553 = TreeNode(55)

root.add_child(child_node55)
root.add_child(child_node552)
root.add_child(child_node42)
root.add_child(child_node33)
child_node55.add_child(child_node15)
child_node55.add_child(child_node20)
child_node42.add_child(child_node22)
child_node22.add_child(child_node553)
"""""
def displaygui(G, root: TreeNode, indent=0):
    global nodeid

    print((' ' * indent) + str(root.get_value()))
    rootnodeid=nodeid
    rootNode = pydot.Node(rootnodeid,label=root.get_value(), style="filled", fillcolor="cyan")
    G.add_node(rootNode)
    for c in root.get_children():
        nodeid=nodeid+1
        childnodeid=nodeid
        childnode=pydot.Node(childnodeid,label=c.get_value(), style="filled", fillcolor="cyan")
        G.add_node(childnode)
        drawnode(G,rootnodeid, childnodeid)
        displaygui(G, c, indent + 1)

    # level = indent


def displayphotograph(photo):
    window = Tk()
    window.geometry("600x700")

    frame = Frame(window)
    frame.pack(expand=1, fill=BOTH)

   # frame.grid_rowconfigure(0, weight=1)
    #frame.grid_columnconfigure(0, weight=1)
    yscrollbar = Scrollbar(frame)
    yscrollbar.pack(side=RIGHT ,fill='y')

    xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
    xscrollbar.pack(side=BOTTOM, fill='x')



    canvas = Canvas(frame, bd=0, xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)
    canvas.pack(expand=1, fill=BOTH)
    image = Image.open(photo)
    display = ImageTk.PhotoImage(image)




    canvas.create_image(0,0, image=display, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    xscrollbar.config(command=canvas.xview)
    yscrollbar.config(command=canvas.yview)


    frame.pack()
    window.mainloop()

def printtree(root: TreeNode):
    G = pydot.Dot(graph_type="graph")
    displaygui(G, root)
    G.write_png('G.png')
    displayphotograph('G.png')



def drawnode(G, parentnode, childnode):
   # node = pydot.Node(childnode.get_value(), style="filled", fillcolor="cyan")
    #G.add_node(node)
    edge = pydot.Edge(parentnode, childnode)
    G.add_edge(edge)

printtree(t)

#printtree(root)




from Tree import TreeNode



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

printtree(root)




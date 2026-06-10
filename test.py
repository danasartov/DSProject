from AVLTree import AVLTree

def print_tree():
    print("           " + str(t.root.key))
    print("        " + str(t.root.left.key) + "        " + str(t.root.right.key))
    #print(str(t.root.left.left.key) + "   " + str(t.root.left.right.key) + "   " + str(t.root.right.left.key) + "   " + str(t.root.right.right.key))
    print(" ")

t = AVLTree(True)
t.insert(1,"1")
t.insert(0,"0")
t.insert(3,"3")
t.insert(2,"2")
t.insert(4,"4")

print_tree()
print(t.avl_to_list())

print("delete " + str(t.root.left.key))
t.delete(t.root.left)
print_tree()

print("delete " + str(t.root.key))
t.delete(t.root)
print_tree()

print("delete " + str(t.root.left.key))
t.delete(t.root.left)
print_tree()
print(t.root.height)
print(t.root.right.height)











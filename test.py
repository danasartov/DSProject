from AVLTree import AVLTree

t = AVLTree(True)
keys = [50, 30, 70, 20, 40, 60, 80, 35, 45, 65]
expected = {}
nodes = {}
for k in keys:
    node, *_ = t.insert(k, str(k))
    expected[k] = str(k)
    nodes[k] = node

#assert_bst_structure(self, t, expected, check_avl=True, check_heights=True)

node_30 = t.root.left
node_20 = t.root.left.left
node_60 = t.root.right.left
node_50 = t.root
t.delete(node_20)
t.delete(node_60)
t.delete(node_30)

#t.delete(node_50)

print(t.root.key)
print(t.root.left.height)

print(" ")
print(t.get_height())


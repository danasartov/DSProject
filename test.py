from AVLTree import AVLTree

n = 100

###### experiment 1 ######
t1 = AVLTree(False)

for i in range(n):
    t1.insert(i,str(i))

print("For test 1 with n = " + str(n) + " the size is: " + str(t1.size()) )







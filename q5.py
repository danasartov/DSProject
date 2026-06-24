from AVLTree import AVLTree

def median_order(arr):
    """Returns insertion order that creates a balanced tree."""
    if not arr:
        return []
    mid = len(arr) // 2
    return [arr[mid]] + median_order(arr[:mid]) + median_order(arr[mid + 1:])

def create_tree(n):
    # Create perfect AVL tree:
    #           3
    #       /       \
    #      1         5
    #    /   \     /   \
    #   0     2   4     6
    
    tree = AVLTree(True)

    keys = list(range(1, n + 1))
    for key in median_order(keys):
        tree.insert(key, str(key))

    return tree

def insert_delete(n, node_num):
    tree = create_tree(node_num)

    total_search_time = 0
    total_rotations = 0
    total_height_changes = 0

    for _ in range(1,n):
        node, search_time, rotations, height_changes = tree.insert(node_num, str(node_num))
        tree.delete(node)

        total_search_time += search_time
        total_rotations += rotations
        total_height_changes += height_changes
    
    return total_search_time, total_rotations, total_height_changes


def main():
    
    for i in range(1, 6):
        n = 300 * (2 ** i)
        print(f"Running experiment for n = {n}, nodes number 7...")
        search_time, rotations, height_changes = insert_delete(n, 7)

        print("For n = " + str(n) + " we get: ")
        print("search time: " + str(search_time) + " rotations: " + str(rotations) + " height changes: " + str(height_changes) )
        print("where height_changes/n is: " + str(height_changes/n))
        print(" ")

    for i in range(1, 5):
        n = 300 * (2 ** i)
        print(f"Running experiment for n = {n}...")
        search_time, rotations, height_changes = insert_delete(n, 63)

        print("For n = " + str(n) + " we get: ")
        print("search time: " + str(search_time) + " rotations: " + str(rotations) + " height changes: " + str(height_changes) )
        print("where height_changes/n is: " + str(height_changes/n))
        print(" ")

if __name__ == "__main__":
    main()
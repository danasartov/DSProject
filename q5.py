from FinalSubmission.AVLTree import AVLTree

def perfect_tree_order(start, end):
    """
    Returns insertion order by levels for a perfect BST
    with keys start,...,end.
    Assumes number of keys is 2^(h+1)-1.
    """
    order = []
    queue = [(start, end)]

    while queue:
        left, right = queue.pop(0)

        if left > right:
            continue

        mid = (left + right) // 2
        order.append(mid)

        queue.append((left, mid - 1))
        queue.append((mid + 1, right))

    return order

def create_perfect_avl(height):
    """
    Creates a perfect AVL tree of height `height`.
    If height of leaf is 0, then number of nodes is 2^(height+1)-1.
    """
    n = 2 ** (height + 1) - 1
    tree = AVLTree(True)

    for key in perfect_tree_order(1, n):
        tree.insert(key, str(key))

    return tree

def insert_delete(repetitions, h):
    tree = create_perfect_avl(h)

    total_search_time = 0
    total_rotations = 0
    total_height_changes = 0

    for _ in range(repetitions):
        node, search_time, rotations, height_changes = tree.insert(2 ** h, str(2 ** h))
        tree.delete(node)

        total_search_time += search_time
        total_rotations += rotations
        total_height_changes += height_changes
    
    return total_search_time, total_rotations, total_height_changes

def run_insert_delete(height):
    for i in range(1, 6):
        repetitions = 300 * (2 ** i)
        print(f"Running experiment for n = {repetitions}, height {height}..")
        search_time, rotations, height_changes = insert_delete(repetitions, height)

        print("For n = " + str(repetitions) + " we get: ")
        print("search time: " + str(search_time) + " rotations: " + str(rotations) + " height changes: " + str(height_changes) )
        print("where height_changes/repetitions is: " + str(height_changes/repetitions))
        print(" ")

def main():
    # For height 5, we need 2^0 + 2^1 + .. + 2^5 = 63 nodes
    run_insert_delete(5)

    # For height 10, we need 2^0 + 2^1 + .. + 2^10 = 2047 nodes
    run_insert_delete(10)

if __name__ == "__main__":
    main()
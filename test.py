import time
import matplotlib.pyplot as plt
from AVLTree import AVLTree


def run_experiment_1(n):
    """
    Experiment 1:
    Insert keys 1,2,...,n in sorted order into a binary tree.
    """

    tree = AVLTree(False)  

    total_search_time = 0
    total_rotations = 0
    total_height_changes = 0

    start_time = time.perf_counter()

    for key in range(1, n + 1):
        node, search_time, rotations, height_changes = tree.insert(key, str(key))

        total_search_time += search_time
        total_rotations += rotations
        total_height_changes += height_changes

    end_time = time.perf_counter()

    runtime_ms = (end_time - start_time) * 1000

    runtime_operations = (
        total_search_time
        + total_rotations
        + total_height_changes
    )

    return {
        "n": n,
        "height": tree.get_height(),
        "rotations": total_rotations,
        "height_changes": total_height_changes,
        "runtime_operations": runtime_operations,
        "runtime_ms": runtime_ms
    }

def run_experiment_2(n):
    """
    Experiment 2:
    Insert keys 1,2,...,n in sorted order into an AVL tree.
    """

    tree = AVLTree(True)  # True => AVL tree

    total_search_time = 0
    total_rotations = 0
    total_height_changes = 0

    start_time = time.perf_counter()

    for key in range(1, n + 1):
        node, search_time, rotations, height_changes = tree.insert(key, str(key))

        total_search_time += search_time
        total_rotations += rotations
        total_height_changes += height_changes

    end_time = time.perf_counter()

    runtime_ms = (end_time - start_time) * 1000

    runtime_operations = (
        total_search_time
        + total_rotations
        + total_height_changes
    )

    return {
        "n": n,
        "height": tree.get_height(),
        "rotations": total_rotations,
        "height_changes": total_height_changes,
        "runtime_operations": runtime_operations,
        "runtime_ms": runtime_ms
    }

def plot_graph(x_values, y_values, title, xlabel, ylabel):
    plt.figure()
    plt.plot(x_values, y_values, marker="o")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def run_test1():
    results = []

    for i in range(1, 11):
        n = 300 * (2 ** i)
        print(f"Running experiment 1 for n = {n}...")
        result = run_experiment_1(n)
        results.append(result)

    print("\nResults:")
    print("n,height,rotations,height_changes,runtime_operations,runtime_ms")
    for row in results:
        print(
            row["n"],
            row["height"],
            row["rotations"],
            row["height_changes"],
            row["runtime_operations"],
            row["runtime_ms"],
            sep=","
        )

    n_values = [row["n"] for row in results]
    runtime_ms = [row["runtime_ms"] for row in results]

    plot_graph(
        n_values,
        runtime_ms,
        "Experiment 1: Runtime in Milliseconds as Function of n",
        "n",
        "Runtime in ms"
    )

def run_test2():
    results = []

    for i in range(1, 11):
        n = 300 * (2 ** i)
        print(f"Running experiment 2 for n = {n}...")
        result = run_experiment_2(n)
        results.append(result)

    print("\nResults:")
    print("n,height,rotations,height_changes,runtime_operations,runtime_ms")
    for row in results:
        print(
            row["n"],
            row["height"],
            row["rotations"],
            row["height_changes"],
            row["runtime_operations"],
            row["runtime_ms"],
            sep=","
        )

    n_values = [row["n"] for row in results]
    runtime_ms = [row["runtime_ms"] for row in results]

    plot_graph(
        n_values,
        runtime_ms,
        "Experiment 2: Runtime in Milliseconds as Function of n",
        "n",
        "Runtime in ms"
    )

def main():
    run_test2()

    


if __name__ == "__main__":
    main()
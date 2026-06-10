"""
Standalone tests for the Data Structures AVLTree.py project.

How to run:
    python test_avl_tree_project.py
or:
    python test_avl_tree_project.py /path/to/AVLTree.py

Assumptions from the project skeleton:
    - file exposes classes AVLTree and AVLNode
    - AVLTree(is_avl=True) behaves as an AVL tree
    - AVLTree(is_avl=False) behaves as a regular BST without rotations
    - public methods: search, insert, delete, avl_to_list, size, get_root, get_height
"""

import importlib.util
import math
import os
import random
import sys
import unittest


DEFAULT_MODULE_PATH = os.path.join(os.path.dirname(__file__), "AVLTree.py")
MODULE_PATH = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODULE_PATH
# Prevent unittest from treating the module path as a test name.
sys.argv = [sys.argv[0]]


def load_avl_module(path):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Cannot find AVLTree.py at {path!r}. Put this test file next to AVLTree.py "
            f"or run: python test_avl_tree_project.py /full/path/to/AVLTree.py"
        )
    spec = importlib.util.spec_from_file_location("student_avl_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AVL_MODULE = load_avl_module(MODULE_PATH)
AVLTree = AVL_MODULE.AVLTree
AVLNode = AVL_MODULE.AVLNode


def is_real(node):
    return node is not None and hasattr(node, "is_real_node") and node.is_real_node()


def node_height(node):
    return node.height if is_real(node) else -1


def inorder_nodes(root):
    out = []

    def visit(x):
        if not is_real(x):
            return
        visit(x.left)
        out.append(x)
        visit(x.right)

    visit(root)
    return out


def actual_height(root):
    if not is_real(root):
        return -1
    return 1 + max(actual_height(root.left), actual_height(root.right))


def assert_bst_structure(testcase, tree, expected_items, *, check_avl=False, check_heights=False):
    """Checks order, size, root parent, parent pointers, heights, and optionally AVL balance."""
    root = tree.get_root()
    expected_list = sorted(expected_items.items())

    testcase.assertEqual(tree.avl_to_list(), expected_list, "avl_to_list must return sorted (key, value) pairs")
    testcase.assertEqual(tree.size(), len(expected_items), "size() is inconsistent with inserted/deleted keys")
    testcase.assertEqual(tree.get_height(), actual_height(root), "get_height() is inconsistent with the actual tree shape")

    if not expected_items:
        testcase.assertIsNone(root, "Empty tree must have root None")
        testcase.assertEqual(tree.get_height(), -1, "Empty tree height must be -1")
        return

    testcase.assertTrue(is_real(root), "Non-empty tree root must be a real node")
    testcase.assertIsNone(root.parent, "Root parent must be None")

    seen_keys = []

    def walk(x, lo, hi, parent):
        if not is_real(x):
            return -1

        testcase.assertIs(x.parent, parent, f"Wrong parent pointer at key {x.key}")
        testcase.assertIsInstance(x.key, int, "Project requires integer keys")
        testcase.assertGreater(x.key, lo, f"BST invariant violated: key {x.key} <= lower bound {lo}")
        testcase.assertLess(x.key, hi, f"BST invariant violated: key {x.key} >= upper bound {hi}")
        testcase.assertEqual(x.value, expected_items[x.key], f"Wrong value stored at key {x.key}")

        lh = walk(x.left, lo, x.key, x)
        seen_keys.append(x.key)
        rh = walk(x.right, x.key, hi, x)
        h = 1 + max(lh, rh)

        if check_heights:
            testcase.assertEqual(x.height, h, f"Wrong stored height at key {x.key}")
        if check_avl:
            testcase.assertLessEqual(abs(lh - rh), 1, f"AVL balance violated at key {x.key}: left={lh}, right={rh}")
        return h

    walk(root, -math.inf, math.inf, None)
    testcase.assertEqual(seen_keys, [k for k, _ in expected_list], "In-order traversal is not sorted as expected")


class TestAVLProjectAPI(unittest.TestCase):
    def test_empty_tree_contract(self):
        for is_avl in (True, False):
            with self.subTest(is_avl=is_avl):
                t = AVLTree(is_avl)
                self.assertIsNone(t.get_root())
                self.assertEqual(t.size(), 0)
                self.assertEqual(t.get_height(), -1)
                self.assertEqual(t.avl_to_list(), [])
                self.assertEqual(t.search(12345), (None, 1), "Search in an empty tree must return search_time=1")

    def test_node_realness_for_real_node(self):
        node = AVLNode(10, "x")
        self.assertTrue(node.is_real_node(), "A node created with a key/value should be real")

    def test_search_time_on_bst_chain(self):
        t = AVLTree(False)
        expected = {}
        for k in range(1, 6):
            node, search_time, rotations, height_changes = t.insert(k, str(k))
            expected[k] = str(k)
            self.assertTrue(is_real(node))
            self.assertEqual(search_time, k, f"BST sorted insertion of key {k} should have search_time={k}")
            self.assertEqual(rotations, 0, "BST mode must not perform rotations")
            self.assertEqual(height_changes, 0, "BST mode must not count AVL height changes")
            assert_bst_structure(self, t, expected, check_avl=False, check_heights=False)

        for k in range(1, 6):
            node, search_time = t.search(k)
            self.assertTrue(is_real(node))
            self.assertEqual(node.key, k)
            self.assertEqual(search_time, k, f"Searching key {k} in a right chain should visit {k} real nodes")

        node, search_time = t.search(999)
        self.assertIsNone(node)
        self.assertEqual(search_time, 6, "Failed search after a 5-node right chain should return 6")
        self.assertEqual(t.get_height(), 4, "Unbalanced BST right chain with 5 nodes should have height 4")

    def test_avl_rotation_examples_from_assignment(self):
        # Example in the instructions: insert 3, then 1, then 2.
        t = AVLTree(True)
        n3, st, rot, hc = t.insert(3, "3")
        self.assertEqual((st, rot, hc), (1, 0, 0))
        n1, st, rot, hc = t.insert(1, "1")
        self.assertEqual((st, rot, hc), (2, 0, 1))
        n2, st, rot, hc = t.insert(2, "2")
        self.assertEqual(st, 3)
        self.assertEqual(rot, 2, "LR case should be counted as 2 rotations")
        self.assertEqual(hc, 1, "Only the height change before the double rotation should be counted")
        assert_bst_structure(self, t, {1: "1", 2: "2", 3: "3"}, check_avl=True, check_heights=True)
        self.assertEqual(t.get_root().key, 2)

        # Symmetric RL case: insert 1, then 3, then 2.
        t = AVLTree(True)
        self.assertEqual(t.insert(1, "1")[1:], (1, 0, 0))
        self.assertEqual(t.insert(3, "3")[1:], (2, 0, 1))
        node, st, rot, hc = t.insert(2, "2")
        self.assertEqual(st, 3)
        self.assertEqual(rot, 2, "RL case should be counted as 2 rotations")
        self.assertEqual(hc, 1)
        assert_bst_structure(self, t, {1: "1", 2: "2", 3: "3"}, check_avl=True, check_heights=True)
        self.assertEqual(t.get_root().key, 2)

    def test_single_rotation_cases(self):
        cases = [
            ([3, 2, 1], 1, 2, "LL case should be one right rotation"),
            ([1, 2, 3], 1, 2, "RR case should be one left rotation"),
        ]
        for keys, expected_rotations, expected_root, message in cases:
            with self.subTest(keys=keys):
                t = AVLTree(True)
                observed = []
                expected = {}
                for k in keys:
                    node, st, rot, hc = t.insert(k, str(k))
                    observed.append((st, rot, hc))
                    expected[k] = str(k)
                    self.assertLessEqual(rot, 2, "AVL insertion should use at most one regular/double rotation")
                    assert_bst_structure(self, t, expected, check_avl=True, check_heights=True)
                self.assertEqual(observed[-1][1], expected_rotations, message)
                self.assertEqual(t.get_root().key, expected_root)

    def test_avl_sorted_insertions_stay_logarithmic_and_bst_does_not(self):
        n = 100

        avl = AVLTree(True)
        avl_items = {}
        total_rotations = 0
        for k in range(1, n + 1):
            node, st, rot, hc = avl.insert(k, str(k))
            avl_items[k] = str(k)
            total_rotations += rot
            self.assertTrue(is_real(node))
            self.assertLessEqual(rot, 2, "Each AVL insert may do at most 2 counted rotations")
            self.assertGreaterEqual(hc, 0)
        assert_bst_structure(self, avl, avl_items, check_avl=True, check_heights=True)
        # A valid AVL tree with 100 nodes has height far below 99. This bound is intentionally loose.
        self.assertLessEqual(avl.get_height(), 12, "AVL height after 100 sorted inserts is too large")
        self.assertGreater(total_rotations, 0, "Sorted AVL insertion should require rotations")

        bst = AVLTree(False)
        bst_items = {}
        for k in range(1, n + 1):
            node, st, rot, hc = bst.insert(k, str(k))
            bst_items[k] = str(k)
            self.assertEqual(rot, 0)
            self.assertEqual(hc, 0)
        assert_bst_structure(self, bst, bst_items, check_avl=False, check_heights=False)
        self.assertEqual(bst.get_height(), n - 1, "Regular BST sorted inserts should create a chain")

    def test_delete_leaf_one_child_two_children_root_until_empty(self):
        t = AVLTree(True)
        keys = [50, 30, 70, 20, 40, 60, 80, 35, 45, 65]
        expected = {}
        nodes = {}
        for k in keys:
            node, *_ = t.insert(k, str(k))
            expected[k] = str(k)
            nodes[k] = node
        assert_bst_structure(self, t, expected, check_avl=True, check_heights=True)

        # Delete a leaf, then a node with one child, then a node with two children, then the root.
        for k in [20, 60, 30, 50]:
            with self.subTest(delete=k):
                node, _ = t.search(k)
                self.assertTrue(is_real(node), f"Key {k} should exist before deletion")
                t.delete(node)
                print(k)
                expected.pop(k)
                self.assertIsNone(t.search(k)[0], f"Key {k} should not exist after deletion")
                assert_bst_structure(self, t, expected, check_avl=True, check_heights=True)

        # Delete all remaining nodes, using fresh pointers from search.
        for k in list(expected.keys()):
            node, _ = t.search(k)
            t.delete(node)
            expected.pop(k)
            assert_bst_structure(self, t, expected, check_avl=True, check_heights=True)

    def test_randomized_avl_insert_delete_against_python_dict(self):
        rng = random.Random(2026)
        keys = list(range(1, 151))
        rng.shuffle(keys)

        t = AVLTree(True)
        expected = {}
        for i, k in enumerate(keys):
            node, st, rot, hc = t.insert(k, f"v{k}")
            expected[k] = f"v{k}"
            self.assertTrue(is_real(node))
            self.assertLessEqual(rot, 2)
            if i % 10 == 0:
                assert_bst_structure(self, t, expected, check_avl=True, check_heights=True)
        assert_bst_structure(self, t, expected, check_avl=True, check_heights=True)

        rng.shuffle(keys)
        for i, k in enumerate(keys):
            node, st = t.search(k)
            self.assertTrue(is_real(node), f"Key {k} should be found before deletion")
            self.assertEqual(node.key, k)
            t.delete(node)
            expected.pop(k)
            if i % 10 == 0:
                assert_bst_structure(self, t, expected, check_avl=True, check_heights=True)
        assert_bst_structure(self, t, expected, check_avl=True, check_heights=True)

    def test_randomized_bst_against_python_dict(self):
        rng = random.Random(2158)
        keys = list(range(-50, 51))
        rng.shuffle(keys)
        t = AVLTree(False)
        expected = {}

        for k in keys:
            node, st, rot, hc = t.insert(k, f"v{k}")
            expected[k] = f"v{k}"
            self.assertEqual(rot, 0)
            self.assertEqual(hc, 0)
            self.assertTrue(is_real(node))
        assert_bst_structure(self, t, expected, check_avl=False, check_heights=False)

        # Search existing and missing keys.
        for k in [-50, -1, 0, 1, 50]:
            node, st = t.search(k)
            self.assertTrue(is_real(node))
            self.assertEqual((node.key, node.value), (k, f"v{k}"))
            self.assertGreaterEqual(st, 1)
        for k in [-999, 999, 52]:
            node, st = t.search(k)
            self.assertIsNone(node)
            self.assertGreaterEqual(st, 1)

        # Delete half of the keys.
        for k in keys[:50]:
            node, _ = t.search(k)
            t.delete(node)
            expected.pop(k)
        assert_bst_structure(self, t, expected, check_avl=False, check_heights=False)


if __name__ == "__main__":
    unittest.main(verbosity=2)

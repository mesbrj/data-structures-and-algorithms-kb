from collections import deque
from dataclasses import dataclass
from typing import List
from pytest import fixture

@dataclass
class TreeNode():
    value: int
    left: 'TreeNode' = None
    right: 'TreeNode' = None

class BinarySearchTree():
    def __init__(self, root: TreeNode = None):
        self.root = root

    def add_node(self, value: int) -> bool:
        def _add_single_node(node: TreeNode, value: int):
            if node is None:
                node = TreeNode(value)
                return True
            elif value < node.value:
                return _add_single_node(node.left, value)
            elif value > node.value:
                return _add_single_node(node.right, value)
            else:
                return False
        return _add_single_node(self.root, value)

    def serch_node(self, value: int) -> bool:
        def _search_single_node(node: TreeNode, value: int) -> bool:
            if node is None:
                return False
            elif value == node.value:
                return True
            elif value < node.value:
                return _search_single_node(node.left, value)
            else:
                return _search_single_node(node.right, value)
        return _search_single_node(self.root, value)

    def bf_level_order(self) -> List[List[int]]:
        list_levels = []
        if not self.root:
            return list_levels

        queue = deque([self.root])
        while queue:
            level_size = len(queue)
            current_level = []
            for _ in range(level_size):
                current = queue.popleft()
                current_level.append(current.value)
                if current.left:
                    queue.append(current.left)
                if current.right:
                    queue.append(current.right)
            list_levels.append(current_level)
        return list_levels

    def df_pre_order(self) -> List[int]:
        pre_order = []
        def _df_pre_order(root: TreeNode):
            if root:
                pre_order.append(root.value)
                _df_pre_order(root.left)
                _df_pre_order(root.right)
        _df_pre_order(self.root)
        return pre_order

    def df_in_order(self) -> List[int]:
        in_order = []
        def _df_in_order(root: TreeNode):
            if root:
                _df_in_order(root.left)
                in_order.append(root.value)
                _df_in_order(root.right)
        _df_in_order(self.root)
        return in_order

    def df_post_order(self) -> List[int]:
        post_order = []
        def _df_post_order(root: TreeNode):
            if root:
                _df_post_order(root.left)
                _df_post_order(root.right)
                post_order.append(root.value)
        _df_post_order(self.root)
        return post_order


@fixture
def sample_bst() -> BinarySearchTree:
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(15)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(7)
    root.right.right = TreeNode(18)
    return BinarySearchTree(root)

@fixture
def bst_from_list() -> BinarySearchTree:
    sorted_values = sorted([8, 3, 10, 1, 6, 14, 4, 7, 13])

    def insert(value: int, left: List[int], right: List[int]) -> TreeNode:
        node = TreeNode(value)
        if left:
            mid = len(left) // 2
            node.left = insert(left[mid], left[:mid], left[mid+1:])
        if right:
            mid = len(right) // 2
            node.right = insert(right[mid], right[:mid], right[mid+1:])
        return node

    mid = len(sorted_values) // 2
    root = insert(sorted_values[mid], sorted_values[:mid], sorted_values[mid+1:])
    return BinarySearchTree(root)


def test_add_node(sample_bst: BinarySearchTree, bst_from_list: BinarySearchTree):

    assert BinarySearchTree().add_node(150) == True
    assert sample_bst.add_node(6) == True
    assert sample_bst.add_node(15) == False
    assert bst_from_list.add_node(9) == True
    assert bst_from_list.add_node(4) == False


def test_serch_node(sample_bst: BinarySearchTree, bst_from_list: BinarySearchTree):

    assert sample_bst.serch_node(7) == True
    assert sample_bst.serch_node(20) == False
    assert bst_from_list.serch_node(10) == True
    assert bst_from_list.serch_node(2) == False

def test_df_in_order(sample_bst: BinarySearchTree, bst_from_list: BinarySearchTree):

    assert sample_bst.df_in_order() == [3, 5, 7, 10, 15, 18]
    assert bst_from_list.df_in_order() == [1, 3, 4, 6, 7, 8, 10, 13, 14]

def test_df_pre_order(sample_bst: BinarySearchTree, bst_from_list: BinarySearchTree):

    assert sample_bst.df_pre_order() == [10, 5, 3, 7, 15, 18]
    assert bst_from_list.df_pre_order() == [7, 4, 3, 1, 6, 13, 10, 8, 14]

def test_df_post_order(sample_bst: BinarySearchTree, bst_from_list: BinarySearchTree):

    assert sample_bst.df_post_order() == [3, 7, 5, 18, 15, 10]
    assert bst_from_list.df_post_order() == [1, 3, 6, 4, 8, 10, 14, 13, 7]

def test_bf_level_order(sample_bst: BinarySearchTree, bst_from_list: BinarySearchTree):

    assert sample_bst.bf_level_order() == [[10], [5, 15], [3, 7, 18]]
    assert bst_from_list.bf_level_order() == [[7], [4, 13], [3, 6, 10, 14], [1, 8]]

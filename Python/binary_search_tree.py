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

    def df_pre_order(self, node: TreeNode) -> None:
        if node:
            print(node.value)
            self.df_pre_order(node.left)
            self.df_pre_order(node.right)

    def df_in_order(self, node: TreeNode) -> None:
        if node:
            self.df_in_order(node.left)
            print(node.value)
            self.df_in_order(node.right)

    def df_post_order(self, node: TreeNode) -> None:
        if node:
            self.df_post_order(node.left)
            self.df_post_order(node.right)
            print(node.value)

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
    root = None

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

def test_bf_level_order(bst_from_list: BinarySearchTree):
    assert bst_from_list.bf_level_order() == [[7], [4, 13], [3, 6, 10, 14], [1, 8]]

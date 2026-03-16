# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file.

from typing import TypeVar
import random

KeyType = TypeVar("KeyType")
ValType = TypeVar("ValType")


class Node:
    def __init__(self, key, val, rank):
        self.key = key
        self.val = val
        self.rank = rank
        self.left = None
        self.right = None


class ZipTree:
    def __init__(self):
        self.root = None
        self.size = 0

    @staticmethod
    def get_random_rank() -> int:
        rank = 0
        while random.random() < 0.5:  # "tails"
            rank += 1
        return rank

    def insert(self, key: KeyType, val: ValType, rank: int = -1):
        if rank == -1:
            rank = ZipTree.get_random_rank()

        self.root = self.unzip_and_link(self.root, key, val, rank)
        self.size += 1

    def unzip_and_link(self, node: Node, key: KeyType, val: ValType, rank: int) -> Node:
        if node is None:
            return Node(key, val, rank)

        if rank > node.rank or (rank == node.rank and key < node.key):
            # new node x outranks current node, x takes this spot
            # unzip the subtree rooted at node into P and Q
            x = Node(key, val, rank)
            x.left, x.right = self.unzip(node, key)
            return x

        if key < node.key:
            node.left = self.unzip_and_link(node.left, key, val, rank)
        else:
            node.right = self.unzip_and_link(node.right, key, val, rank)

        return node

    def unzip(self, node: Node, key: KeyType) -> tuple[Node, Node]:
        if node is None:
            return None, None

        if key < node.key:
            # node goes into Q (right output), recurse left to keep splitting
            left, node.left = self.unzip(node.left, key)
            return left, node
        else:
            # node goes into P (left output), recurse right to keep splitting
            node.right, right = self.unzip(node.right, key)
            return node, right

    def zip(self, left: Node, right: Node):
        if left is None:
            return right
        if right is None:
            return left

        if left.rank >= right.rank:
            # left wins, it stays on top
            # zip its right spine with the right subtree
            left.right = self.zip(left.right, right)
            return left
        else:
            # right wins, it stays on top
            # zip its left spine with the left subtree
            right.left = self.zip(left, right.left)
            return right

    def find_node_to_remove(self, node: Node, key: KeyType):
        if node is None:
            return None

        if key == node.key:
            # found it, zip children together to fill the gap
            return self.zip(node.left, node.right)
        elif key < node.key:
            node.left = self.find_node_to_remove(node.left, key)
        else:
            node.right = self.find_node_to_remove(node.right, key)

        return node

    def remove(self, key: KeyType):
        self.root = self.find_node_to_remove(self.root, key)
        self.size -= 1

    def find(self, key: KeyType) -> ValType:
        cur = self.root
        while cur is not None:
            if key == cur.key:
                return cur.val
            elif key < cur.key:
                cur = cur.left
            else:
                cur = cur.right

    def get_size(self) -> int:
        return self.size

    def get_height(self) -> int:
        def height(node: Node):
            if node is None:
                return -1
            return 1 + max(height(node.left), height(node.right))

        return height(self.root)

    def get_depth(self, key: KeyType):
        depth = 0
        cur = self.root
        while cur is not None:
            if key == cur.key:
                return depth
            elif key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
            depth += 1


# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define

# explanations for member functions are provided in requirements.py
# each file that uses a skip list should import it from this file.

from typing import TypeVar
import random
from zip_tree import ZipTree


KeyType = TypeVar("KeyType")
ValType = TypeVar("ValType")


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None


class SkipList:
    def __init__(self):
        self.heads = []
        self.max_lvl = -1

    def get_random_level(self, key: KeyType) -> int:
        # Do not change this function. Use this function to determine what level each key should be at. Assume levels start at 0 (i.e. the bottom-most list is at level 0)
        # e.g. for some key x, if get_random_level(x) = 5, then x should be in the lists on levels 0, 1, 2, 3, 4 and 5 in the skip list.
        random.seed(str(key))
        level = 0
        while random.random() < 0.5 and level < 20:
            level += 1
        return level

    def insert(self, key: KeyType, val: ValType):
        lvl = self.get_random_level(key)

        # make new heads list if new level exceeds current max
        while lvl > self.max_lvl:
            self.heads.append(Node(None, None))
            self.max_lvl += 1
        # insert at every level depending on lvl
        for l in range(lvl + 1):
            newnode = Node(key, val)
            cur = self.heads[l]
            # insert newnode where it should be in this list
            while cur.next is not None and cur.next.key < key:
                cur = cur.next
            newnode.next = cur.next
            cur.next = newnode

    def remove(self, key: KeyType):
        # for every possible level
        for l in range(self.max_lvl + 1):
            cur = self.heads[l]
            while cur.next is not None and cur.next.key < key:
                cur = cur.next
            if cur.next is not None and cur.next.key == key:
                cur.next = cur.next.next

    def find(self, key: KeyType) -> ValType:
        # searching top down
        for l in range(self.max_lvl, -1, -1):
            cur = self.heads[l]
            while cur.next is not None and cur.next.key <= key:
                cur = cur.next
                if cur.key == key:
                    return cur.val
        return None

    def get_list_size_at_level(self, level: int):
        if level > self.max_lvl:
            return 0
        count = 0
        cur = self.heads[level].next
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def from_zip_tree(self, zip_tree: ZipTree) -> None:
        # traverse zip tree and insert nodes from level to rank
        def traverse(node):
            if node is None:
                return
            # set level as the rank
            level = node.rank
            while level > self.max_lvl:
                self.heads.append(Node(None, None))
                self.max_lvl += 1

            for lvl in range(level + 1):
                newnode = Node(node.key, node.val)
                cur = self.heads[lvl]
                while cur.next is not None and cur.next.key < node.key:
                    cur = cur.next
                newnode.next = cur.next
                cur.next = newnode

            traverse(node.left)
            traverse(node.right)

        traverse(zip_tree.root)


# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define

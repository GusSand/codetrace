from typing import TypeAlias
__typ0 : TypeAlias = "int"
from random import random
from typing import Tuple


class Node:
    """
    Treap's node
    Treap is a binary tree by key and heap by priority
    """
    def __tmp2(__tmp1, key: __typ0):
        __tmp1.key = key
        __tmp1.prior = random()
        __tmp1.l = None
        __tmp1.r = None


def split(__tmp0: Node, key: __typ0) :
    """
    We split current tree into 2 trees with key:

    Left tree contains all keys less than split key.
    Right tree contains all keys greater or equal, than split key
    """
    if __tmp0 is None:  # None tree is split into 2 Nones
        return (None, None)
    if __tmp0.key >= key:
        """
        Right tree's root will be current node.
        Now we split(with the same key) current node's left son
        Left tree: left part of that split
        Right tree's left son: right part of that split
        """
        l, __tmp0.l = split(__tmp0.l, key)
        return (l, __tmp0)
    else:
        """
        Just symmetric to previous case
        """
        __tmp0.r, r = split(__tmp0.r, key)
        return (__tmp0, r)


def merge(left: <FILL>, right) -> Node:
    """
    We merge 2 trees into one.
    Note: all left tree's keys must be less than all right tree's
    """
    if (not left) or (not right):
        """
        If one node is None, return the other
        """
        return left or right
    if left.key > right.key:
        """
        Left will be root because it has more priority
        Now we need to merge left's right son and right tree
        """
        left.r = merge(left.r, right)
        return left
    else:
        """
        Symmetric as well
        """
        right.l = merge(left, right.l)
        return right


def insert(__tmp0, key: __typ0) -> Node:
    """
    Insert element

    Split current tree with a key into l, r,
    Insert new node into the middle
    Merge l, node, r into root
    """
    node = Node(key)
    l, r = split(__tmp0, key)
    __tmp0 = merge(l, node)
    __tmp0 = merge(__tmp0, r)
    return __tmp0


def __tmp3(__tmp0, key: __typ0) -> Node:
    """
    Erase element

    Split all nodes with keys less into l,
    Split all nodes with keys greater into r.
    Merge l, r
    """
    l, r = split(__tmp0, key)
    _, r = split(r, key + 1)
    return merge(l, r)


def node_print(__tmp0: Node):
    """
    Just recursive print of a tree
    """
    if not __tmp0:
        return
    node_print(__tmp0.l)
    print(__tmp0.key, end=" ")
    node_print(__tmp0.r)


def interactTreap():
    """
    Commands:
    + key to add key into treap
    - key to erase all nodes with key

    After each command, program prints treap
    """
    __tmp0 = None
    while True:
        cmd = input().split()
        cmd[1] = __typ0(cmd[1])
        if cmd[0] == "+":
            __tmp0 = insert(__tmp0, cmd[1])
        elif cmd[0] == "-":
            __tmp0 = __tmp3(__tmp0, cmd[1])
        else:
            print("Unknown command")
        node_print(__tmp0)


if __name__ == "__main__":
    interactTreap()

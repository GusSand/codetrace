from random import random
from typing import Tuple


class __typ0:
    """
    Treap's node
    Treap is a binary tree by key and heap by priority
    """
    def __tmp3(self, key: int):
        self.key = key
        self.prior = random()
        self.l = None
        self.r = None


def split(__tmp0: __typ0, key: <FILL>) -> Tuple[__typ0, __typ0]:
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


def __tmp4(__tmp1: __typ0, right: __typ0) -> __typ0:
    """
    We merge 2 trees into one.
    Note: all left tree's keys must be less than all right tree's
    """
    if (not __tmp1) or (not right):
        """
        If one node is None, return the other
        """
        return __tmp1 or right
    if __tmp1.key > right.key:
        """
        Left will be root because it has more priority
        Now we need to merge left's right son and right tree
        """
        __tmp1.r = __tmp4(__tmp1.r, right)
        return __tmp1
    else:
        """
        Symmetric as well
        """
        right.l = __tmp4(__tmp1, right.l)
        return right


def insert(__tmp0, key: int) -> __typ0:
    """
    Insert element

    Split current tree with a key into l, r,
    Insert new node into the middle
    Merge l, node, r into root
    """
    node = __typ0(key)
    l, r = split(__tmp0, key)
    __tmp0 = __tmp4(l, node)
    __tmp0 = __tmp4(__tmp0, r)
    return __tmp0


def __tmp5(__tmp0: __typ0, key: int) :
    """
    Erase element

    Split all nodes with keys less into l,
    Split all nodes with keys greater into r.
    Merge l, r
    """
    l, r = split(__tmp0, key)
    _, r = split(r, key + 1)
    return __tmp4(l, r)


def node_print(__tmp0: __typ0):
    """
    Just recursive print of a tree
    """
    if not __tmp0:
        return
    node_print(__tmp0.l)
    print(__tmp0.key, end=" ")
    node_print(__tmp0.r)


def __tmp2():
    """
    Commands:
    + key to add key into treap
    - key to erase all nodes with key

    After each command, program prints treap
    """
    __tmp0 = None
    while True:
        cmd = input().split()
        cmd[1] = int(cmd[1])
        if cmd[0] == "+":
            __tmp0 = insert(__tmp0, cmd[1])
        elif cmd[0] == "-":
            __tmp0 = __tmp5(__tmp0, cmd[1])
        else:
            print("Unknown command")
        node_print(__tmp0)


if __name__ == "__main__":
    __tmp2()

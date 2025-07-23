from random import random
from typing import Tuple


class __typ0:
    """
    Treap's node
    Treap is a binary tree by key and heap by priority
    """
    def __tmp6(__tmp0, key: int):
        __tmp0.key = key
        __tmp0.prior = random()
        __tmp0.l = None
        __tmp0.r = None


def split(__tmp1: __typ0, key: int) -> Tuple[__typ0, __typ0]:
    """
    We split current tree into 2 trees with key:

    Left tree contains all keys less than split key.
    Right tree contains all keys greater or equal, than split key
    """
    if __tmp1 is None:  # None tree is split into 2 Nones
        return (None, None)
    if __tmp1.key >= key:
        """
        Right tree's root will be current node.
        Now we split(with the same key) current node's left son
        Left tree: left part of that split
        Right tree's left son: right part of that split
        """
        l, __tmp1.l = split(__tmp1.l, key)
        return (l, __tmp1)
    else:
        """
        Just symmetric to previous case
        """
        __tmp1.r, r = split(__tmp1.r, key)
        return (__tmp1, r)


def __tmp8(__tmp5: __typ0, __tmp3) -> __typ0:
    """
    We merge 2 trees into one.
    Note: all left tree's keys must be less than all right tree's
    """
    if (not __tmp5) or (not __tmp3):
        """
        If one node is None, return the other
        """
        return __tmp5 or __tmp3
    if __tmp5.key > __tmp3.key:
        """
        Left will be root because it has more priority
        Now we need to merge left's right son and right tree
        """
        __tmp5.r = __tmp8(__tmp5.r, __tmp3)
        return __tmp5
    else:
        """
        Symmetric as well
        """
        __tmp3.l = __tmp8(__tmp5, __tmp3.l)
        return __tmp3


def __tmp7(__tmp1: __typ0, key: int) -> __typ0:
    """
    Insert element

    Split current tree with a key into l, r,
    Insert new node into the middle
    Merge l, node, r into root
    """
    node = __typ0(key)
    l, r = split(__tmp1, key)
    __tmp1 = __tmp8(l, node)
    __tmp1 = __tmp8(__tmp1, r)
    return __tmp1


def erase(__tmp1: __typ0, key: <FILL>) -> __typ0:
    """
    Erase element

    Split all nodes with keys less into l,
    Split all nodes with keys greater into r.
    Merge l, r
    """
    l, r = split(__tmp1, key)
    _, r = split(r, key + 1)
    return __tmp8(l, r)


def __tmp2(__tmp1: __typ0):
    """
    Just recursive print of a tree
    """
    if not __tmp1:
        return
    __tmp2(__tmp1.l)
    print(__tmp1.key, end=" ")
    __tmp2(__tmp1.r)


def __tmp4():
    """
    Commands:
    + key to add key into treap
    - key to erase all nodes with key

    After each command, program prints treap
    """
    __tmp1 = None
    while True:
        cmd = input().split()
        cmd[1] = int(cmd[1])
        if cmd[0] == "+":
            __tmp1 = __tmp7(__tmp1, cmd[1])
        elif cmd[0] == "-":
            __tmp1 = erase(__tmp1, cmd[1])
        else:
            print("Unknown command")
        __tmp2(__tmp1)


if __name__ == "__main__":
    __tmp4()

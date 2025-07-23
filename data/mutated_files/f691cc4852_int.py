from typing import TypeAlias
__typ1 : TypeAlias = "str"
from datetime import timedelta
from typing import Union, List


class __typ0:
    """
    Used to represent a tree with a value (usually time)

    Useful to visualize time spent in each category.
    """
    def __init__(__tmp0, label, value: <FILL>):
        __tmp0.label = label
        __tmp0.value = value
        __tmp0.children = []

    def __tmp3(__tmp0) :
        return f"<Node '{__tmp0.label}' with '{__tmp0.value}' and {len(__tmp0.children)} children>"

    def __tmp1(__tmp0, label) :
        if isinstance(label, list):
            node = __tmp0
            for sublabel in label:
                node = node[sublabel]
            return node
        else:
            return any(label == child.label for child in __tmp0.children)

    def __getitem__(__tmp0, label) :
        return next(child for child in __tmp0.children if child.label == label)

    def __tmp4(__tmp0, __tmp2) :
        assert isinstance(__tmp2, __typ0)
        __tmp0.children.append(__tmp2)
        return __tmp0

    def total(__tmp0) :
        acc = __tmp0.value
        if isinstance(__tmp0.value, timedelta):
            zero = timedelta()
        else:
            zero = 0
        acc += sum([c.total() for c in __tmp0.children], zero)
        return acc

    def print(__tmp0, depth=1, width=24, indent=4, sort=True) :
        total = __tmp0.total()
        children = __tmp0.children
        if sort:
            children = sorted(children, key=lambda c: c.total(), reverse=True)
        label = f"{__tmp0.label}:".ljust(width - indent * depth)
        parent = f"  {total}  {'(' + __typ1(__tmp0.value) + ')' if __tmp0.value != total else ''}\n"
        children = "".join([(" " * indent * depth) + node.print(depth=depth + 1) for node in children])
        return label + parent + children


def test_node():
    root = __typ0('root', 1)

    work = __typ0('Work', 2)
    root += work
    assert 'Work' in root

    prog = __typ0('Programming', 2)
    work += prog
    assert 'Programming' in work
    assert work['Programming']

    media = __typ0('Media', 3)
    root += media
    media += __typ0('YouTube', 5)

    print(work.print())
    print(root.print())
    assert root.total() == 13


def test_node_timedelta():
    root = __typ0('root', timedelta(seconds=5))
    root += __typ0('work', timedelta(seconds=30))
    print(root.total())
    print(root.print(sort=False))


if __name__ == "__main__":
    test_node()
    test_node_timedelta()

from datetime import timedelta
from typing import Union, List


class Node:
    """
    Used to represent a tree with a value (usually time)

    Useful to visualize time spent in each category.
    """
    def __init__(__tmp1, label: <FILL>, value: int):
        __tmp1.label = label
        __tmp1.value = value
        __tmp1.children = []

    def __repr__(__tmp1) -> str:
        return f"<Node '{__tmp1.label}' with '{__tmp1.value}' and {len(__tmp1.children)} children>"

    def __tmp0(__tmp1, label: Union[str, List[str]]) -> bool:
        if isinstance(label, list):
            node = __tmp1
            for sublabel in label:
                node = node[sublabel]
            return node
        else:
            return any(label == child.label for child in __tmp1.children)

    def __getitem__(__tmp1, label: str) -> 'Node':
        return next(child for child in __tmp1.children if child.label == label)

    def __iadd__(__tmp1, other: 'Node') -> 'Node':
        assert isinstance(other, Node)
        __tmp1.children.append(other)
        return __tmp1

    def total(__tmp1) :
        acc = __tmp1.value
        if isinstance(__tmp1.value, timedelta):
            zero = timedelta()
        else:
            zero = 0
        acc += sum([c.total() for c in __tmp1.children], zero)
        return acc

    def print(__tmp1, depth=1, width=24, indent=4, sort=True) -> str:
        total = __tmp1.total()
        children = __tmp1.children
        if sort:
            children = sorted(children, key=lambda c: c.total(), reverse=True)
        label = f"{__tmp1.label}:".ljust(width - indent * depth)
        parent = f"  {total}  {'(' + str(__tmp1.value) + ')' if __tmp1.value != total else ''}\n"
        children = "".join([(" " * indent * depth) + node.print(depth=depth + 1) for node in children])
        return label + parent + children


def test_node():
    root = Node('root', 1)

    work = Node('Work', 2)
    root += work
    assert 'Work' in root

    prog = Node('Programming', 2)
    work += prog
    assert 'Programming' in work
    assert work['Programming']

    media = Node('Media', 3)
    root += media
    media += Node('YouTube', 5)

    print(work.print())
    print(root.print())
    assert root.total() == 13


def test_node_timedelta():
    root = Node('root', timedelta(seconds=5))
    root += Node('work', timedelta(seconds=30))
    print(root.total())
    print(root.print(sort=False))


if __name__ == "__main__":
    test_node()
    test_node_timedelta()

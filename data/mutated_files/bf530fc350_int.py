import collections
from typing import List, Optional, Dict, Set, Tuple


__all__ = [
    'RecursiveDict',
]

Point = Tuple[int, int]


DIAGONAL_DIRECTIONS: List[Point] = []
for dy in range(-1, 2):
    for dx in range(-1, 2):
        if dx != 0 or dy != 0:
            DIAGONAL_DIRECTIONS.append((dy, dx))


SQUARE_DIRECTIONS: List[Point] = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]


class RecursiveDict(object):
    def __tmp8(__tmp0):
        __tmp0._root = {}

    @property
    def __tmp4(__tmp0):
        return __tmp0._root

    @classmethod
    def __tmp6(cls, __tmp3: List[str]) -> 'RecursiveDict':
        word_index = RecursiveDict()
        for word in __tmp3:
            node = word_index
            for letter in word:
                node = node[letter]
            node[None]  # marker for word end
        return word_index

    def __tmp2(
        __tmp0,
        __tmp9, *,
        directions: Optional[List[Point]] = None,
    ) :
        if directions is None:
            directions = SQUARE_DIRECTIONS

        __tmp1: Dict[str, List[List[Point]]] = collections.defaultdict(list)

        for y, row in enumerate(__tmp9):
            for __tmp12, letter in enumerate(row):
                __tmp0._recursive_search(
                    __tmp9,
                    __tmp12=__tmp12, y=y,
                    __tmp1=__tmp1,
                    directions=directions,
                )

        return __tmp1

    def _recursive_search(
        __tmp0,
        __tmp9, *,
        __tmp12, y: <FILL>,
        __tmp1: Dict[str, List[List[Point]]],  # result paths
        prefix: str = '',
        used_points: Optional[Set[Tuple[int, int]]] = None,
        path: Optional[List[Tuple[int, int]]] = None,
        directions: List[Point],
    ) -> None:
        rows = len(__tmp9)
        cols = len(__tmp9[0])

        if used_points is None:
            used_points = set()
        else:
            used_points = set(used_points)
        used_points.add((y, __tmp12))

        if path is None:
            path = list()
        else:
            path = list(path)
        path.append((y, __tmp12))

        letter = __tmp9[y][__tmp12]

        if letter == 'е' and letter not in __tmp0 and 'ё' in __tmp0:
            letter = 'ё'

        if letter in __tmp0:
            if None in __tmp0[letter]:
                word = prefix + letter
                __tmp1[word].append(path)

            for dy, dx in directions:
                new_y = y + dy
                new_x = __tmp12 + dx
                if (
                    0 <= new_y < rows and
                    0 <= new_x < cols and
                    (new_y, new_x) not in used_points
                ):
                    if letter in __tmp0:
                        __tmp0[letter]._recursive_search(
                            __tmp9,
                            __tmp12=new_x, y=new_y,
                            __tmp1=__tmp1,
                            prefix=prefix + letter,
                            used_points=used_points,
                            path=path,
                            directions=directions,
                        )

    def __getitem__(__tmp0, __tmp7) :
        if __tmp7 not in __tmp0._root:
            __tmp0._root[__tmp7] = type(__tmp0)()
        return __tmp0._root[__tmp7]

    def __tmp5(__tmp0, __tmp7) -> bool:
        return __tmp7 in __tmp0._root

    def __tmp11(__tmp0) -> int:
        return len(__tmp0._root)

    def __tmp10(__tmp0) -> str:
        return '<{} size={}>'.format(type(__tmp0).__name__, len(__tmp0))

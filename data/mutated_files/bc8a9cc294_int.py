from typing import TypeAlias
__typ1 : TypeAlias = "T"
from typing import TypeVar, Generic, List
__typ1 = TypeVar("T")


class __typ0(Generic[__typ1]):
    def __tmp1(__tmp0) :
        __tmp0._container: List[__typ1] = []

    def push(__tmp0, item) :
        __tmp0._container.append(item)

    def pop(__tmp0) :
        return __tmp0._container.pop()

    def __tmp3(__tmp0) :
        return repr(__tmp0._container)

num_discs: int = 4
tower_a: __typ0[int] = __typ0()
tower_b: __typ0[int] = __typ0()
tower_c: __typ0[int] = __typ0()
for i in range(1, num_discs + 1):
    tower_a.push(i)

def __tmp2(begin, end, temp, n:<FILL>) :
    if n == 1:
        end.push(begin.pop())
    else:
        __tmp2(begin, temp, end, n - 1)
        __tmp2(begin, end, temp, 1)
        __tmp2(temp, end, begin, n - 1)

if __name__ == "__main__":
    __tmp2(tower_a, tower_c, tower_b, num_discs)
    print(tower_a)
    print(tower_b)
    print(tower_c)

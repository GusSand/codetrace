from typing import TypeVar, Generic, List
T = TypeVar("T")


class __typ0(Generic[T]):
    def __tmp5(__tmp0) :
        __tmp0._container: List[T] = []

    def push(__tmp0, __tmp3: <FILL>) :
        __tmp0._container.append(__tmp3)

    def pop(__tmp0) -> T:
        return __tmp0._container.pop()

    def __tmp7(__tmp0) :
        return repr(__tmp0._container)

num_discs: int = 4
tower_a: __typ0[int] = __typ0()
tower_b: __typ0[int] = __typ0()
tower_c: __typ0[int] = __typ0()
for i in range(1, num_discs + 1):
    tower_a.push(i)

def __tmp6(__tmp2: __typ0[int], __tmp1: __typ0[int], __tmp4, n) -> None:
    if n == 1:
        __tmp1.push(__tmp2.pop())
    else:
        __tmp6(__tmp2, __tmp4, __tmp1, n - 1)
        __tmp6(__tmp2, __tmp1, __tmp4, 1)
        __tmp6(__tmp4, __tmp1, __tmp2, n - 1)

if __name__ == "__main__":
    __tmp6(tower_a, tower_c, tower_b, num_discs)
    print(tower_a)
    print(tower_b)
    print(tower_c)

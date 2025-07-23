from functools import lru_cache

@lru_cache(maxsize=None)
def __tmp0(n: <FILL>) -> int:
    if n < 2:
        return n
    return __tmp0(n - 1) + __tmp0(n - 2)

if __name__ == "__main__":
    print(__tmp0(1))
    print(__tmp0(10))
    print(__tmp0(20))
    print(__tmp0(30))
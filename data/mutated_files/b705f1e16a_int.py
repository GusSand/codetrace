from typing import Dict
memo: Dict[int, int] = {0: 0, 1: 1}

def __tmp0(n: <FILL>) :
    if n not in memo:
        memo[n] = __tmp0(n - 1) + __tmp0(n - 2)
    return memo[n]

if __name__ == "__main__":
    print(__tmp0(1))
    print(__tmp0(10))
    print(__tmp0(20))
    print(__tmp0(30))
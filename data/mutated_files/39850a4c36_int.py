def __tmp1(__tmp0: <FILL>) :
    if __tmp0 == 0: return __tmp0
    lst: int = 0
    nxt: int = 1
    for _ in range(1,__tmp0):
        lst, nxt = nxt, lst + nxt
    return nxt

if __name__ == "__main__":
    print(__tmp1(1))
    print(__tmp1(10))
    print(__tmp1(20))
    print(__tmp1(30))
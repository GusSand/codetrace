def __tmp0(n: <FILL>) :
    return __tmp0(n - 1) + __tmp0(n - 2)

if __name__ == "__main__":
    print(
        __tmp0(5)
    )

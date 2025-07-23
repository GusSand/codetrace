

def __tmp2(__tmp0, __tmp1: <FILL>) -> int:
    """
        Considering natural numbers of the form, a**b, where a, b < 100,
        what is the maximum digital sum?
        :param a:
        :param b:
        :return:
        >>> maximum_digital_sum(10,10)
        45

        >>> maximum_digital_sum(100,100)
        972

        >>> maximum_digital_sum(100,200)
        1872
    """

    # RETURN the MAXIMUM from the list of SUMs of the list of INT converted from STR of BASE raised to the POWER
    return max([sum([int(x) for x in str(base**power)]) for base in range(__tmp0) for power in range(__tmp1)])

#Tests
if __name__ == "__main__":
    import doctest
    doctest.testmod()

from typing import TypeAlias
__typ1 : TypeAlias = "set"
__typ0 : TypeAlias = "int"
"""
Given weights and values of n items, put these items in a knapsack of
 capacity W to get the maximum total value in the knapsack.

Note that only the integer weights 0-1 knapsack problem is solvable
 using dynamic programming.
"""


def __tmp2(__tmp1, __tmp5, __tmp0, __tmp7):
    '''
    This code involves the concept of memory functions. Here we solve the subproblems which are needed
    unlike the below example
    F is a 2D array with -1s filled up
    '''
    global F  # a global dp table for knapsack
    if F[__tmp1][__tmp7] < 0:
        if __tmp7 < __tmp5[__tmp1-1]:
            __tmp0 = __tmp2(__tmp1-1, __tmp5, __tmp0, __tmp7)
        else:
            __tmp0 = max(__tmp2(__tmp1-1, __tmp5, __tmp0, __tmp7),
                      __tmp2(__tmp1-1, __tmp5, __tmp0, __tmp7 - __tmp5[__tmp1-1]) + __tmp0[__tmp1-1])
        F[__tmp1][__tmp7] = __tmp0
    return F[__tmp1][__tmp7]


def __tmp3(__tmp8, __tmp5, __tmp0, __tmp4):
    __tmp11 = [[0 for __tmp1 in range(__tmp8+1)]for __tmp7 in range(__tmp4+1)]

    for __tmp1 in range(1,__tmp4+1):
        for w in range(1, __tmp8+1):
            if __tmp5[__tmp1-1] <= w:
                __tmp11[__tmp1][w] = max(__tmp0[__tmp1-1] + __tmp11[__tmp1-1][w-__tmp5[__tmp1-1]], __tmp11[__tmp1-1][w])
            else:
                __tmp11[__tmp1][w] = __tmp11[__tmp1-1][w]

    return __tmp11[__tmp4][__tmp8], __tmp11


def __tmp9(__tmp8, __tmp5: list, __tmp0:<FILL>):
    """
    Solves the integer weights knapsack problem returns one of
    the several possible optimal subsets.

    Parameters
    ---------

    W: int, the total maximum weight for the given knapsack problem.
    wt: list, the vector of weights for all items where wt[i] is the weight
    of the ith item.
    val: list, the vector of values for all items where val[i] is the value
    of te ith item

    Returns
    -------
    optimal_val: float, the optimal value for the given knapsack problem
    example_optional_set: set, the indices of one of the optimal subsets
    which gave rise to the optimal value.

    Examples
    -------
    >>> knapsack_with_example_solution(10, [1, 3, 5, 2], [10, 20, 100, 22])
    (142, {2, 3, 4})
    >>> knapsack_with_example_solution(6, [4, 3, 2, 3], [3, 2, 4, 4])
    (8, {3, 4})
    >>> knapsack_with_example_solution(6, [4, 3, 2, 3], [3, 2, 4])
    Traceback (most recent call last):
        ...
    ValueError: The number of weights must be the same as the number of values.
    But got 4 weights and 3 values
    """
    if not (isinstance(__tmp5, (list, tuple)) and isinstance(__tmp0, (list, tuple))):
        raise ValueError("Both the weights and values vectors must be either lists or tuples")

    num_items = len(__tmp5)
    if num_items != len(__tmp0):
        raise ValueError("The number of weights must be the "
                         "same as the number of values.\nBut "
                         "got {} weights and {} values".format(num_items, len(__tmp0)))
    for __tmp1 in range(num_items):
        if not isinstance(__tmp5[__tmp1], __typ0):
            raise TypeError("All weights must be integers but "
                            "got weight of type {} at index {}".format(type(__tmp5[__tmp1]), __tmp1))

    optimal_val, dp_table = __tmp3(__tmp8, __tmp5, __tmp0, num_items)
    example_optional_set = __typ1()
    __tmp10(dp_table, __tmp5, num_items, __tmp8, example_optional_set)

    return optimal_val, example_optional_set


def __tmp10(__tmp11, __tmp5:list, __tmp1:__typ0, __tmp7:__typ0, __tmp6:__typ1):
    """
    Recursively reconstructs one of the optimal subsets given
    a filled DP table and the vector of weights

    Parameters
    ---------

    dp: list of list, the table of a solved integer weight dynamic programming problem

    wt: list or tuple, the vector of weights of the items
    i: int, the index of the  item under consideration
    j: int, the current possible maximum weight
    optimal_set: set, the optimal subset so far. This gets modified by the function.

    Returns
    -------
    None

    """
    # for the current item i at a maximum weight j to be part of an optimal subset,
    # the optimal value at (i, j) must be greater than the optimal value at (i-1, j).
    # where i - 1 means considering only the previous items at the given maximum weight
    if __tmp1 > 0 and __tmp7 > 0:
        if __tmp11[__tmp1 - 1][__tmp7] == __tmp11[__tmp1][__tmp7]:
            __tmp10(__tmp11, __tmp5, __tmp1 - 1, __tmp7, __tmp6)
        else:
            __tmp6.add(__tmp1)
            __tmp10(__tmp11, __tmp5, __tmp1 - 1, __tmp7 - __tmp5[__tmp1-1], __tmp6)


if __name__ == '__main__':
    '''
    Adding test case for knapsack
    '''
    __tmp0 = [3, 2, 4, 4]
    __tmp5 = [4, 3, 2, 3]
    __tmp4 = 4
    w = 6
    F = [[0] * (w + 1)] + [[0] + [-1 for __tmp1 in range(w + 1)] for __tmp7 in range(__tmp4 + 1)]
    optimal_solution, _ = __tmp3(w,__tmp5,__tmp0, __tmp4)
    print(optimal_solution)
    print(__tmp2(__tmp4,__tmp5,__tmp0,w))  # switched the n and w

    # testing the dynamic programming problem with example
    # the optimal subset for the above example are items 3 and 4
    optimal_solution, optimal_subset = __tmp9(w, __tmp5, __tmp0)
    assert optimal_solution == 8
    assert optimal_subset == {3, 4}
    print("optimal_value = ", optimal_solution)
    print("An optimal subset corresponding to the optimal value", optimal_subset)


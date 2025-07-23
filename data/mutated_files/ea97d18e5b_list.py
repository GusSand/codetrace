from typing import TypeAlias
__typ0 : TypeAlias = "int"
"""
Given weights and values of n items, put these items in a knapsack of
 capacity W to get the maximum total value in the knapsack.

Note that only the integer weights 0-1 knapsack problem is solvable
 using dynamic programming.
"""


def MF_knapsack(__tmp0, __tmp2, val, __tmp4):
    '''
    This code involves the concept of memory functions. Here we solve the subproblems which are needed
    unlike the below example
    F is a 2D array with -1s filled up
    '''
    global F  # a global dp table for knapsack
    if F[__tmp0][__tmp4] < 0:
        if __tmp4 < __tmp2[__tmp0-1]:
            val = MF_knapsack(__tmp0-1, __tmp2, val, __tmp4)
        else:
            val = max(MF_knapsack(__tmp0-1, __tmp2, val, __tmp4),
                      MF_knapsack(__tmp0-1, __tmp2, val, __tmp4 - __tmp2[__tmp0-1]) + val[__tmp0-1])
        F[__tmp0][__tmp4] = val
    return F[__tmp0][__tmp4]


def __tmp1(__tmp5, __tmp2, val, n):
    dp = [[0 for __tmp0 in range(__tmp5+1)]for __tmp4 in range(n+1)]

    for __tmp0 in range(1,n+1):
        for w in range(1, __tmp5+1):
            if __tmp2[__tmp0-1] <= w:
                dp[__tmp0][w] = max(val[__tmp0-1] + dp[__tmp0-1][w-__tmp2[__tmp0-1]], dp[__tmp0-1][w])
            else:
                dp[__tmp0][w] = dp[__tmp0-1][w]

    return dp[n][__tmp5], dp


def knapsack_with_example_solution(__tmp5: __typ0, __tmp2: <FILL>, val:list):
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
    if not (isinstance(__tmp2, (list, tuple)) and isinstance(val, (list, tuple))):
        raise ValueError("Both the weights and values vectors must be either lists or tuples")

    num_items = len(__tmp2)
    if num_items != len(val):
        raise ValueError("The number of weights must be the "
                         "same as the number of values.\nBut "
                         "got {} weights and {} values".format(num_items, len(val)))
    for __tmp0 in range(num_items):
        if not isinstance(__tmp2[__tmp0], __typ0):
            raise TypeError("All weights must be integers but "
                            "got weight of type {} at index {}".format(type(__tmp2[__tmp0]), __tmp0))

    optimal_val, dp_table = __tmp1(__tmp5, __tmp2, val, num_items)
    example_optional_set = set()
    __tmp6(dp_table, __tmp2, num_items, __tmp5, example_optional_set)

    return optimal_val, example_optional_set


def __tmp6(dp:list, __tmp2:list, __tmp0:__typ0, __tmp4, __tmp3:set):
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
    if __tmp0 > 0 and __tmp4 > 0:
        if dp[__tmp0 - 1][__tmp4] == dp[__tmp0][__tmp4]:
            __tmp6(dp, __tmp2, __tmp0 - 1, __tmp4, __tmp3)
        else:
            __tmp3.add(__tmp0)
            __tmp6(dp, __tmp2, __tmp0 - 1, __tmp4 - __tmp2[__tmp0-1], __tmp3)


if __name__ == '__main__':
    '''
    Adding test case for knapsack
    '''
    val = [3, 2, 4, 4]
    __tmp2 = [4, 3, 2, 3]
    n = 4
    w = 6
    F = [[0] * (w + 1)] + [[0] + [-1 for __tmp0 in range(w + 1)] for __tmp4 in range(n + 1)]
    optimal_solution, _ = __tmp1(w,__tmp2,val, n)
    print(optimal_solution)
    print(MF_knapsack(n,__tmp2,val,w))  # switched the n and w

    # testing the dynamic programming problem with example
    # the optimal subset for the above example are items 3 and 4
    optimal_solution, optimal_subset = knapsack_with_example_solution(w, __tmp2, val)
    assert optimal_solution == 8
    assert optimal_subset == {3, 4}
    print("optimal_value = ", optimal_solution)
    print("An optimal subset corresponding to the optimal value", optimal_subset)


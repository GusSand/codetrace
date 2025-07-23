from typing import TypeAlias
__typ0 : TypeAlias = "int"
"""
Author  : Turfa Auliarachman
Date    : October 12, 2016

This is a pure Python implementation of Dynamic Programming solution to the edit distance problem.

The problem is :
Given two strings A and B. Find the minimum number of operations to string B such that A = B. The permitted operations are removal,  insertion, and substitution.
"""


class EditDistance:
    """
    Use :
    solver              = EditDistance()
    editDistanceResult  = solver.solve(firstString, secondString)
    """

    def __tmp4(__tmp0):
        __tmp0.__prepare__()

    def __prepare__(__tmp0, N = 0, M = 0):
        __tmp0.dp = [[-1 for __tmp3 in range(0,M)] for __tmp6 in range(0,N)]

    def __solveDP(__tmp0, __tmp6, __tmp3):
        if (__tmp6==-1):
            return __tmp3+1
        elif (__tmp3==-1):
            return __tmp6+1
        elif (__tmp0.dp[__tmp6][__tmp3]>-1):
            return __tmp0.dp[__tmp6][__tmp3]
        else:
            if (__tmp0.A[__tmp6]==__tmp0.B[__tmp3]):
                __tmp0.dp[__tmp6][__tmp3] = __tmp0.__solveDP(__tmp6-1,__tmp3-1)
            else:
                __tmp0.dp[__tmp6][__tmp3] = 1+min(__tmp0.__solveDP(__tmp6,__tmp3-1), __tmp0.__solveDP(__tmp6-1,__tmp3), __tmp0.__solveDP(__tmp6-1,__tmp3-1))

            return __tmp0.dp[__tmp6][__tmp3]

    def solve(__tmp0, A, B):
        if isinstance(A,bytes):
            A = A.decode('ascii')

        if isinstance(B,bytes):
            B = B.decode('ascii')

        __tmp0.A = str(A)
        __tmp0.B = str(B)

        __tmp0.__prepare__(len(A), len(B))

        return __tmp0.__solveDP(len(A)-1, len(B)-1)


def __tmp2(__tmp5: <FILL>, __tmp1: str) :
    """
    >>> min_distance_bottom_up("intention", "execution")
    5
    >>> min_distance_bottom_up("intention", "")
    9
    >>> min_distance_bottom_up("", "")
    0
    """
    m = len(__tmp5)
    n = len(__tmp1)
    dp = [[0 for _ in range(n+1) ] for _ in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):

            if i == 0:  #first string is empty
                dp[i][j] = j
            elif j == 0: #second string is empty
                dp[i][j] = i
            elif __tmp5[i-1] == __tmp1[j-1]: #last character of both substing is equal
                dp[i][j] = dp[i-1][j-1]
            else:
                insert = dp[i][j-1]
                delete = dp[i-1][j]
                replace = dp[i-1][j-1]
                dp[i][j] = 1 + min(insert, delete, replace)
    return dp[m][n]

if __name__ == '__main__':
        solver = EditDistance()

        print("****************** Testing Edit Distance DP Algorithm ******************")
        print()

        S1 = input("Enter the first string: ").strip()
        S2 = input("Enter the second string: ").strip()

        print()
        print("The minimum Edit Distance is: %d" % (solver.solve(S1, S2)))
        print("The minimum Edit Distance is: %d" % (__tmp2(S1, S2)))
        print()
        print("*************** End of Testing Edit Distance DP Algorithm ***************")





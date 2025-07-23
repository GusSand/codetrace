from typing import TypeAlias
__typ0 : TypeAlias = "int"
"""
This module provides two implementations for the rod-cutting problem:
1. A naive recursive implementation which has an exponential runtime
2. Two dynamic programming implementations which have quadratic runtime

The rod-cutting problem is the problem of finding the maximum possible revenue
obtainable from a rod of length ``n`` given a list of prices for each integral piece
of the rod. The maximum revenue can thus be obtained by cutting the rod and selling the
pieces separately or not cutting it at all if the price of it is the maximum obtainable.

"""


def naive_cut_rod_recursive(__tmp1, __tmp3: <FILL>):
	"""
	Solves the rod-cutting problem via naively without using the benefit of dynamic programming.
	The results is the same sub-problems are solved several times leading to an exponential runtime

	Runtime: O(2^n)

	Arguments
	-------
	n: int, the length of the rod
	prices: list, the prices for each piece of rod. ``p[i-i]`` is the
	price for a rod of length ``i``

	Returns
	-------
	The maximum revenue obtainable for a rod of length n given the list of prices for each piece.

	Examples
	--------
	>>> naive_cut_rod_recursive(4, [1, 5, 8, 9])
	10
	>>> naive_cut_rod_recursive(10, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30])
	30
	"""

	_enforce_args(__tmp1, __tmp3)
	if __tmp1 == 0:
		return 0
	max_revue = float("-inf")
	for i in range(1, __tmp1 + 1):
		max_revue = max(max_revue, __tmp3[i - 1] + naive_cut_rod_recursive(__tmp1 - i, __tmp3))

	return max_revue


def __tmp5(__tmp1, __tmp3):
	"""
	Constructs a top-down dynamic programming solution for the rod-cutting problem
	via memoization. This function serves as a wrapper for _top_down_cut_rod_recursive

	Runtime: O(n^2)

	Arguments
	--------
	n: int, the length of the rod
	prices: list, the prices for each piece of rod. ``p[i-i]`` is the
	price for a rod of length ``i``

	Note
	----
	For convenience and because Python's lists using 0-indexing, length(max_rev) = n + 1,
	to accommodate for the revenue obtainable from a rod of length 0.

	Returns
	-------
	The maximum revenue obtainable for a rod of length n given the list of prices for each piece.

	Examples
	-------
	>>> top_down_cut_rod(4, [1, 5, 8, 9])
	10
	>>> top_down_cut_rod(10, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30])
	30
	"""
	_enforce_args(__tmp1, __tmp3)
	__tmp0 = [float("-inf") for _ in range(__tmp1 + 1)]
	return __tmp4(__tmp1, __tmp3, __tmp0)


def __tmp4(__tmp1, __tmp3, __tmp0):
	"""
	Constructs a top-down dynamic programming solution for the rod-cutting problem
	via memoization.

	Runtime: O(n^2)

	Arguments
	--------
	n: int, the length of the rod
	prices: list, the prices for each piece of rod. ``p[i-i]`` is the
	price for a rod of length ``i``
	max_rev: list, the computed maximum revenue for a piece of rod.
	``max_rev[i]`` is the maximum revenue obtainable for a rod of length ``i``

	Returns
	-------
	The maximum revenue obtainable for a rod of length n given the list of prices for each piece.
	"""
	if __tmp0[__tmp1] >= 0:
		return __tmp0[__tmp1]
	elif __tmp1 == 0:
		return 0
	else:
		max_revenue = float("-inf")
		for i in range(1, __tmp1 + 1):
			max_revenue = max(max_revenue, __tmp3[i - 1] + __tmp4(__tmp1 - i, __tmp3, __tmp0))

		__tmp0[__tmp1] = max_revenue

	return __tmp0[__tmp1]


def __tmp2(__tmp1: __typ0, __tmp3):
	"""
	Constructs a bottom-up dynamic programming solution for the rod-cutting problem

	Runtime: O(n^2)

	Arguments
	----------
	n: int, the maximum length of the rod.
	prices: list, the prices for each piece of rod. ``p[i-i]`` is the
	price for a rod of length ``i``

	Returns
	-------
	The maximum revenue obtainable from cutting a rod of length n given
	the prices for each piece of rod p.

	Examples
	-------
	>>> bottom_up_cut_rod(4, [1, 5, 8, 9])
	10
	>>> bottom_up_cut_rod(10, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30])
	30
	"""
	_enforce_args(__tmp1, __tmp3)

	# length(max_rev) = n + 1, to accommodate for the revenue obtainable from a rod of length 0.
	__tmp0 = [float("-inf") for _ in range(__tmp1 + 1)]
	__tmp0[0] = 0

	for i in range(1, __tmp1 + 1):
		max_revenue_i = __tmp0[i]
		for j in range(1, i + 1):
			max_revenue_i = max(max_revenue_i, __tmp3[j - 1] + __tmp0[i - j])

		__tmp0[i] = max_revenue_i

	return __tmp0[__tmp1]


def _enforce_args(__tmp1: __typ0, __tmp3: list):
	"""
	Basic checks on the arguments to the rod-cutting algorithms

	n: int, the length of the rod
	prices: list, the price list for each piece of rod.

	Throws ValueError:

	if n is negative or there are fewer items in the price list than the length of the rod
	"""
	if __tmp1 < 0:
		raise ValueError(f"n must be greater than or equal to 0. Got n = {__tmp1}")

	if __tmp1 > len(__tmp3):
		raise ValueError(f"Each integral piece of rod must have a corresponding "
						 f"price. Got n = {__tmp1} but length of prices = {len(__tmp3)}")


def main():
	__tmp3 = [6, 10, 12, 15, 20, 23]
	__tmp1 = len(__tmp3)

	# the best revenue comes from cutting the rod into 6 pieces, each
	# of length 1 resulting in a revenue of 6 * 6 = 36.
	expected_max_revenue = 36

	max_rev_top_down = __tmp5(__tmp1, __tmp3)
	max_rev_bottom_up = __tmp2(__tmp1, __tmp3)
	max_rev_naive = naive_cut_rod_recursive(__tmp1, __tmp3)

	assert expected_max_revenue == max_rev_top_down
	assert max_rev_top_down == max_rev_bottom_up
	assert max_rev_bottom_up == max_rev_naive


if __name__ == '__main__':
	main()

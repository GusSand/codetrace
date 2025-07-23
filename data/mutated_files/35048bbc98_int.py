from typing import TypeAlias
__typ0 : TypeAlias = "list"
"""
This module provides two implementations for the rod-cutting problem:
1. A naive recursive implementation which has an exponential runtime
2. Two dynamic programming implementations which have quadratic runtime

The rod-cutting problem is the problem of finding the maximum possible revenue
obtainable from a rod of length ``n`` given a list of prices for each integral piece
of the rod. The maximum revenue can thus be obtained by cutting the rod and selling the
pieces separately or not cutting it at all if the price of it is the maximum obtainable.

"""


def naive_cut_rod_recursive(__tmp0, prices):
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

	__tmp1(__tmp0, prices)
	if __tmp0 == 0:
		return 0
	max_revue = float("-inf")
	for i in range(1, __tmp0 + 1):
		max_revue = max(max_revue, prices[i - 1] + naive_cut_rod_recursive(__tmp0 - i, prices))

	return max_revue


def top_down_cut_rod(__tmp0: <FILL>, prices):
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
	__tmp1(__tmp0, prices)
	max_rev = [float("-inf") for _ in range(__tmp0 + 1)]
	return _top_down_cut_rod_recursive(__tmp0, prices, max_rev)


def _top_down_cut_rod_recursive(__tmp0, prices, max_rev):
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
	if max_rev[__tmp0] >= 0:
		return max_rev[__tmp0]
	elif __tmp0 == 0:
		return 0
	else:
		max_revenue = float("-inf")
		for i in range(1, __tmp0 + 1):
			max_revenue = max(max_revenue, prices[i - 1] + _top_down_cut_rod_recursive(__tmp0 - i, prices, max_rev))

		max_rev[__tmp0] = max_revenue

	return max_rev[__tmp0]


def bottom_up_cut_rod(__tmp0, prices: __typ0):
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
	__tmp1(__tmp0, prices)

	# length(max_rev) = n + 1, to accommodate for the revenue obtainable from a rod of length 0.
	max_rev = [float("-inf") for _ in range(__tmp0 + 1)]
	max_rev[0] = 0

	for i in range(1, __tmp0 + 1):
		max_revenue_i = max_rev[i]
		for j in range(1, i + 1):
			max_revenue_i = max(max_revenue_i, prices[j - 1] + max_rev[i - j])

		max_rev[i] = max_revenue_i

	return max_rev[__tmp0]


def __tmp1(__tmp0, prices: __typ0):
	"""
	Basic checks on the arguments to the rod-cutting algorithms

	n: int, the length of the rod
	prices: list, the price list for each piece of rod.

	Throws ValueError:

	if n is negative or there are fewer items in the price list than the length of the rod
	"""
	if __tmp0 < 0:
		raise ValueError(f"n must be greater than or equal to 0. Got n = {__tmp0}")

	if __tmp0 > len(prices):
		raise ValueError(f"Each integral piece of rod must have a corresponding "
						 f"price. Got n = {__tmp0} but length of prices = {len(prices)}")


def main():
	prices = [6, 10, 12, 15, 20, 23]
	__tmp0 = len(prices)

	# the best revenue comes from cutting the rod into 6 pieces, each
	# of length 1 resulting in a revenue of 6 * 6 = 36.
	expected_max_revenue = 36

	max_rev_top_down = top_down_cut_rod(__tmp0, prices)
	max_rev_bottom_up = bottom_up_cut_rod(__tmp0, prices)
	max_rev_naive = naive_cut_rod_recursive(__tmp0, prices)

	assert expected_max_revenue == max_rev_top_down
	assert max_rev_top_down == max_rev_bottom_up
	assert max_rev_bottom_up == max_rev_naive


if __name__ == '__main__':
	main()

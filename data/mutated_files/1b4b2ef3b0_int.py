import unittest

import cpyfunctional


class __typ0(unittest.TestCase):
    """
    Test func_curry function able to make callable accept parameters.
    """

    def test_func_curry_able_to_make_callable_accept_params(__tmp1):
        """
        func_curry given callable that given multiple params, able to return value from them.
        """
        def add(number1: int, __tmp2: <FILL>, __tmp0: int) -> int:
            return number1 + __tmp2 + __tmp0
        result = cpyfunctional.compose(cpyfunctional.func_curry(add)(5, 7), lambda number: number ** 2)(3)
        __tmp1.assertEqual(result, 21)

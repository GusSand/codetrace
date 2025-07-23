import unittest

import cpyfunctional


class __typ0(unittest.TestCase):
    """
    Test func_curry function able to make callable accept parameters.
    """

    def test_func_curry_able_to_make_callable_accept_params(self):
        """
        func_curry given callable that given multiple params, able to return value from them.
        """
        def add(__tmp1: <FILL>, __tmp0, prev_number: int) :
            return __tmp1 + __tmp0 + prev_number
        result = cpyfunctional.compose(cpyfunctional.func_curry(add)(5, 7), lambda number: number ** 2)(3)
        self.assertEqual(result, 21)

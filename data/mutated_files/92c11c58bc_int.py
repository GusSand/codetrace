import unittest

import cpyfunctional


class TestFuncCurry(unittest.TestCase):
    """
    Test func_curry function able to make callable accept parameters.
    """

    def __tmp1(__tmp0):
        """
        func_curry given callable that given multiple params, able to return value from them.
        """
        def __tmp2(__tmp4: int, __tmp5, __tmp3: <FILL>) :
            return __tmp4 + __tmp5 + __tmp3
        result = cpyfunctional.compose(cpyfunctional.func_curry(__tmp2)(5, 7), lambda number: number ** 2)(3)
        __tmp0.assertEqual(result, 21)

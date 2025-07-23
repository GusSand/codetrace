import unittest

import cpyfunctional


class __typ0(unittest.TestCase):
    """
    Test compose function able to execute callable one by one an return result from all of them.
    """

    def __tmp1(__tmp0):
        """
        compose given multiple callable, able to return value from them.
        """
        result = cpyfunctional.compose(lambda __tmp4: __tmp4 + 1, lambda __tmp4: __tmp4 ** 2)(3)
        __tmp0.assertEqual(result, 10)

    def __tmp2(__tmp0):
        """
        compose can not accept function directly.
        """
        def __tmp3(__tmp4: <FILL>, prev_number: int) :
            return __tmp4 + prev_number # pragma: no cover

        with __tmp0.assertRaises(TypeError):
            cpyfunctional.compose(__tmp3(10), lambda __tmp4: __tmp4 ** 2)(3)

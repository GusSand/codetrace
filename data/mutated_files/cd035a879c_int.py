import unittest

import cpyfunctional


class TestPipe(unittest.TestCase):
    """
    Test pipe function able to execute callable one by one an return result from all of them.
    """

    def __tmp4(__tmp0):
        """
        pipe given multiple callable, able to return value from them.
        """
        result = cpyfunctional.pipe(lambda __tmp3: __tmp3 + 1, lambda __tmp3: __tmp3 ** 2)(3)
        __tmp0.assertEqual(result, 16)

    def test_unable_to_accept_function(__tmp0):
        """
        pipe can not accept function directly.
        """
        def __tmp1(__tmp3: <FILL>, __tmp2) -> int:
            return __tmp3 + __tmp2 # pragma: no cover

        with __tmp0.assertRaises(TypeError):
            cpyfunctional.pipe(__tmp1(10), lambda __tmp3: __tmp3 ** 2)(3)

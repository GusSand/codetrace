# pyre-strict

from unittest import TestCase

from typing import List, Any

from lowerpines.exceptions import NoneFoundException, MultipleFoundException

from lowerpines.manager import AbstractManager
from lowerpines.gmi import GMI


class __typ0(AbstractManager[int]):
    def _all(__tmp1) :
        return [0, 1, 2, 3, 4]


class MockType:
    def __init__(__tmp1, val: <FILL>) -> None:
        __tmp1.val = val


# pyre-ignore
def mm_instance(content: Any = None):
    return __typ0(GMI("access_token_here"), content)


class __typ1(TestCase):
    def setUp(__tmp1) :
        __tmp1.mm = mm_instance()
        __tmp1.mt = MockType(3)
        __tmp1.cmm = mm_instance([__tmp1.mt])
        __tmp1.cmm_multiple = mm_instance([MockType(14), MockType(14)])

    def test_all_case(__tmp1) -> None:
        for i, m in enumerate(__tmp1.mm):
            __tmp1.assertEqual(i, m)

    def __tmp2(__tmp1) :
        arr = [2, 5, 12, 77]
        mm = mm_instance(arr)
        for a, m in zip(arr, mm):
            __tmp1.assertEqual(a, m)

    def __tmp0(__tmp1) :
        __tmp1.assertEqual(len(__tmp1.mm), 5)

    def test_lazy_get_item_call(__tmp1) :
        __tmp1.assertEqual(__tmp1.mm[3], 3)

    def test_get_item(__tmp1) -> None:
        __tmp1.assertEqual(__tmp1.cmm.get(val=3), __tmp1.mt)

    def test_get_item_none_found(__tmp1) :
        with __tmp1.assertRaises(NoneFoundException):
            __tmp1.cmm.get(val=5)

    def test_get_item_multiple_found(__tmp1) :
        with __tmp1.assertRaises(MultipleFoundException):
            __tmp1.cmm_multiple.get(val=14)

    def test_filter_single(__tmp1) :
        __tmp1.assertEqual(__tmp1.cmm.filter(val=3)._content, [__tmp1.mt])

    def test_filter_multiple(__tmp1) :
        __tmp1.assertEqual(
            __tmp1.cmm_multiple.filter(val=14)._content,
            [__tmp1.cmm_multiple[0], __tmp1.cmm_multiple[1]],
        )

from typing import TypeAlias
__typ0 : TypeAlias = "A"
__typ1 : TypeAlias = "str"

import sys
from unittest import TestCase
from io import StringIO

from zerver.lib.type_debug import print_types

from typing import Any, Callable, Dict, Iterable, Tuple, TypeVar, List

T = TypeVar('T')

def add(x: Any=0, y: Any=0) :
    return x + y

def __tmp11(v: Iterable[Tuple[Any, Any]]=[]) -> Dict[Any, Any]:
    return dict(v)

class __typ2(TestCase):

    # These 2 methods are needed to run tests with our custom test-runner
    def __tmp2(__tmp1) :
        pass

    def __tmp10(__tmp1) :
        pass

    def check_signature(__tmp1, signature: __typ1, retval: T, __tmp8,
                        *args, **kwargs: <FILL>) -> None:
        """
        Checks if print_types outputs `signature` when func is called with *args and **kwargs.
        Do not decorate func with print_types before passing into this function.
        func will be decorated with print_types within this function.
        """
        try:
            original_stdout = sys.stdout
            sys.stdout = StringIO()
            __tmp1.assertEqual(retval, print_types(__tmp8)(*args, **kwargs))
            __tmp1.assertEqual(sys.stdout.getvalue().strip(), signature)
        finally:
            sys.stdout = original_stdout

    def test_empty(__tmp1) -> None:
        def __tmp9() -> None:
            pass
        __tmp1.check_signature("empty_func() -> None", None, __tmp9)
        __tmp1.check_signature("<lambda>() -> None", None, (lambda: None))

    def __tmp3(__tmp1) :
        __tmp1.check_signature("add(float, int) -> float",
                             5.0, add, 2.0, 3)
        __tmp1.check_signature("add(float, y=int) -> float",
                             5.0, add, 2.0, y=3)
        __tmp1.check_signature("add(x=int) -> int", 2, add, x=2)
        __tmp1.check_signature("add() -> int", 0, add)

    def test_list(__tmp1) -> None:
        __tmp1.check_signature("add([], [str]) -> [str]",
                             ['two'], add, [], ['two'])
        __tmp1.check_signature("add([int], [str]) -> [int, ...]",
                             [2, 'two'], add, [2], ['two'])
        __tmp1.check_signature("add([int, ...], y=[]) -> [int, ...]",
                             [2, 'two'], add, [2, 'two'], y=[])

    def __tmp5(__tmp1) :
        __tmp1.check_signature("to_dict() -> {}", {}, __tmp11)
        __tmp1.check_signature("to_dict([(int, str)]) -> {int: str}",
                             {2: 'two'}, __tmp11, [(2, 'two')])
        __tmp1.check_signature("to_dict(((int, str),)) -> {int: str}",
                             {2: 'two'}, __tmp11, ((2, 'two'),))
        __tmp1.check_signature("to_dict([(int, str), ...]) -> {int: str, ...}",
                             {1: 'one', 2: 'two'}, __tmp11, [(1, 'one'), (2, 'two')])

    def __tmp6(__tmp1) :
        __tmp1.check_signature("add((), ()) -> ()",
                             (), add, (), ())
        __tmp1.check_signature("add((int,), (str,)) -> (int, str)",
                             (1, 'one'), add, (1,), ('one',))
        __tmp1.check_signature("add(((),), ((),)) -> ((), ())",
                             ((), ()), add, ((),), ((),))

    def __tmp7(__tmp1) :
        class __typ0:
            pass

        class B(__typ1):
            pass

        __tmp1.check_signature("<lambda>(A) -> str", 'A', (lambda x: x.__class__.__name__), __typ0())
        __tmp1.check_signature("<lambda>(B) -> int", 5, (lambda x: len(x)), B("hello"))

    def __tmp4(__tmp1) -> None:
        class __typ0(List[Any]):
            pass

        class B(List[Any]):
            pass

        __tmp1.check_signature("add(A([]), B([str])) -> [str]",
                             ['two'], add, __typ0([]), B(['two']))
        __tmp1.check_signature("add(A([int]), B([str])) -> [int, ...]",
                             [2, 'two'], add, __typ0([2]), B(['two']))
        __tmp1.check_signature("add(A([int, ...]), y=B([])) -> [int, ...]",
                             [2, 'two'], add, __typ0([2, 'two']), y=B([]))

    def test_mapping(__tmp1) :
        class __typ0(Dict[Any, Any]):
            pass

        def __tmp0(v: Iterable[Tuple[Any, Any]]=[]) :
            return __typ0(v)

        __tmp1.check_signature("to_A() -> A([])", __typ0(()), __tmp0)
        __tmp1.check_signature("to_A([(int, str)]) -> A([(int, str)])",
                             {2: 'two'}, __tmp0, [(2, 'two')])
        __tmp1.check_signature("to_A([(int, str), ...]) -> A([(int, str), ...])",
                             {1: 'one', 2: 'two'}, __tmp0, [(1, 'one'), (2, 'two')])
        __tmp1.check_signature("to_A(((int, str), (int, str))) -> A([(int, str), ...])",
                             {1: 'one', 2: 'two'}, __tmp0, ((1, 'one'), (2, 'two')))

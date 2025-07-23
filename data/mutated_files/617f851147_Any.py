from typing import TypeAlias
__typ1 : TypeAlias = "T"
__typ0 : TypeAlias = "A"

import sys
from unittest import TestCase
from io import StringIO

from zerver.lib.type_debug import print_types

from typing import Any, Callable, Dict, Iterable, Tuple, TypeVar, List

__typ1 = TypeVar('T')

def add(x: Any=0, y: Any=0) :
    return x + y

def to_dict(v: Iterable[Tuple[Any, Any]]=[]) :
    return dict(v)

class __typ2(TestCase):

    # These 2 methods are needed to run tests with our custom test-runner
    def __tmp4(__tmp0) :
        pass

    def _post_teardown(__tmp0) :
        pass

    def check_signature(__tmp0, signature, retval, func,
                        *args: <FILL>, **kwargs) :
        """
        Checks if print_types outputs `signature` when func is called with *args and **kwargs.
        Do not decorate func with print_types before passing into this function.
        func will be decorated with print_types within this function.
        """
        try:
            original_stdout = sys.stdout
            sys.stdout = StringIO()
            __tmp0.assertEqual(retval, print_types(func)(*args, **kwargs))
            __tmp0.assertEqual(sys.stdout.getvalue().strip(), signature)
        finally:
            sys.stdout = original_stdout

    def test_empty(__tmp0) :
        def empty_func() :
            pass
        __tmp0.check_signature("empty_func() -> None", None, empty_func)
        __tmp0.check_signature("<lambda>() -> None", None, (lambda: None))

    def test_basic(__tmp0) :
        __tmp0.check_signature("add(float, int) -> float",
                             5.0, add, 2.0, 3)
        __tmp0.check_signature("add(float, y=int) -> float",
                             5.0, add, 2.0, y=3)
        __tmp0.check_signature("add(x=int) -> int", 2, add, x=2)
        __tmp0.check_signature("add() -> int", 0, add)

    def __tmp2(__tmp0) :
        __tmp0.check_signature("add([], [str]) -> [str]",
                             ['two'], add, [], ['two'])
        __tmp0.check_signature("add([int], [str]) -> [int, ...]",
                             [2, 'two'], add, [2], ['two'])
        __tmp0.check_signature("add([int, ...], y=[]) -> [int, ...]",
                             [2, 'two'], add, [2, 'two'], y=[])

    def __tmp1(__tmp0) :
        __tmp0.check_signature("to_dict() -> {}", {}, to_dict)
        __tmp0.check_signature("to_dict([(int, str)]) -> {int: str}",
                             {2: 'two'}, to_dict, [(2, 'two')])
        __tmp0.check_signature("to_dict(((int, str),)) -> {int: str}",
                             {2: 'two'}, to_dict, ((2, 'two'),))
        __tmp0.check_signature("to_dict([(int, str), ...]) -> {int: str, ...}",
                             {1: 'one', 2: 'two'}, to_dict, [(1, 'one'), (2, 'two')])

    def test_tuple(__tmp0) :
        __tmp0.check_signature("add((), ()) -> ()",
                             (), add, (), ())
        __tmp0.check_signature("add((int,), (str,)) -> (int, str)",
                             (1, 'one'), add, (1,), ('one',))
        __tmp0.check_signature("add(((),), ((),)) -> ((), ())",
                             ((), ()), add, ((),), ((),))

    def __tmp3(__tmp0) :
        class __typ0:
            pass

        class __typ3(str):
            pass

        __tmp0.check_signature("<lambda>(A) -> str", 'A', (lambda x: x.__class__.__name__), __typ0())
        __tmp0.check_signature("<lambda>(B) -> int", 5, (lambda x: len(x)), __typ3("hello"))

    def test_sequence(__tmp0) :
        class __typ0(List[Any]):
            pass

        class __typ3(List[Any]):
            pass

        __tmp0.check_signature("add(A([]), B([str])) -> [str]",
                             ['two'], add, __typ0([]), __typ3(['two']))
        __tmp0.check_signature("add(A([int]), B([str])) -> [int, ...]",
                             [2, 'two'], add, __typ0([2]), __typ3(['two']))
        __tmp0.check_signature("add(A([int, ...]), y=B([])) -> [int, ...]",
                             [2, 'two'], add, __typ0([2, 'two']), y=__typ3([]))

    def test_mapping(__tmp0) :
        class __typ0(Dict[Any, Any]):
            pass

        def to_A(v: Iterable[Tuple[Any, Any]]=[]) :
            return __typ0(v)

        __tmp0.check_signature("to_A() -> A([])", __typ0(()), to_A)
        __tmp0.check_signature("to_A([(int, str)]) -> A([(int, str)])",
                             {2: 'two'}, to_A, [(2, 'two')])
        __tmp0.check_signature("to_A([(int, str), ...]) -> A([(int, str), ...])",
                             {1: 'one', 2: 'two'}, to_A, [(1, 'one'), (2, 'two')])
        __tmp0.check_signature("to_A(((int, str), (int, str))) -> A([(int, str), ...])",
                             {1: 'one', 2: 'two'}, to_A, ((1, 'one'), (2, 'two')))

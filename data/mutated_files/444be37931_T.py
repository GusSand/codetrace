
import sys
from unittest import TestCase
from io import StringIO

from zerver.lib.type_debug import print_types

from typing import Any, Callable, Dict, Iterable, Tuple, TypeVar, List

T = TypeVar('T')

def __tmp8(x: Any=0, y: Any=0) :
    return x + y

def to_dict(v: Iterable[Tuple[Any, Any]]=[]) :
    return dict(v)

class TypesPrintTest(TestCase):

    # These 2 methods are needed to run tests with our custom test-runner
    def __tmp13(__tmp1) -> None:
        pass

    def __tmp12(__tmp1) :
        pass

    def check_signature(__tmp1, signature, __tmp11: <FILL>, __tmp9: Callable[..., T],
                        *args, **kwargs) -> None:
        """
        Checks if print_types outputs `signature` when func is called with *args and **kwargs.
        Do not decorate func with print_types before passing into this function.
        func will be decorated with print_types within this function.
        """
        try:
            original_stdout = sys.stdout
            sys.stdout = StringIO()
            __tmp1.assertEqual(__tmp11, print_types(__tmp9)(*args, **kwargs))
            __tmp1.assertEqual(sys.stdout.getvalue().strip(), signature)
        finally:
            sys.stdout = original_stdout

    def __tmp0(__tmp1) :
        def __tmp10() :
            pass
        __tmp1.check_signature("empty_func() -> None", None, __tmp10)
        __tmp1.check_signature("<lambda>() -> None", None, (lambda: None))

    def __tmp2(__tmp1) -> None:
        __tmp1.check_signature("add(float, int) -> float",
                             5.0, __tmp8, 2.0, 3)
        __tmp1.check_signature("add(float, y=int) -> float",
                             5.0, __tmp8, 2.0, y=3)
        __tmp1.check_signature("add(x=int) -> int", 2, __tmp8, x=2)
        __tmp1.check_signature("add() -> int", 0, __tmp8)

    def __tmp7(__tmp1) :
        __tmp1.check_signature("add([], [str]) -> [str]",
                             ['two'], __tmp8, [], ['two'])
        __tmp1.check_signature("add([int], [str]) -> [int, ...]",
                             [2, 'two'], __tmp8, [2], ['two'])
        __tmp1.check_signature("add([int, ...], y=[]) -> [int, ...]",
                             [2, 'two'], __tmp8, [2, 'two'], y=[])

    def __tmp5(__tmp1) :
        __tmp1.check_signature("to_dict() -> {}", {}, to_dict)
        __tmp1.check_signature("to_dict([(int, str)]) -> {int: str}",
                             {2: 'two'}, to_dict, [(2, 'two')])
        __tmp1.check_signature("to_dict(((int, str),)) -> {int: str}",
                             {2: 'two'}, to_dict, ((2, 'two'),))
        __tmp1.check_signature("to_dict([(int, str), ...]) -> {int: str, ...}",
                             {1: 'one', 2: 'two'}, to_dict, [(1, 'one'), (2, 'two')])

    def __tmp6(__tmp1) :
        __tmp1.check_signature("add((), ()) -> ()",
                             (), __tmp8, (), ())
        __tmp1.check_signature("add((int,), (str,)) -> (int, str)",
                             (1, 'one'), __tmp8, (1,), ('one',))
        __tmp1.check_signature("add(((),), ((),)) -> ((), ())",
                             ((), ()), __tmp8, ((),), ((),))

    def test_class(__tmp1) :
        class A:
            pass

        class __typ0(str):
            pass

        __tmp1.check_signature("<lambda>(A) -> str", 'A', (lambda x: x.__class__.__name__), A())
        __tmp1.check_signature("<lambda>(B) -> int", 5, (lambda x: len(x)), __typ0("hello"))

    def __tmp4(__tmp1) :
        class A(List[Any]):
            pass

        class __typ0(List[Any]):
            pass

        __tmp1.check_signature("add(A([]), B([str])) -> [str]",
                             ['two'], __tmp8, A([]), __typ0(['two']))
        __tmp1.check_signature("add(A([int]), B([str])) -> [int, ...]",
                             [2, 'two'], __tmp8, A([2]), __typ0(['two']))
        __tmp1.check_signature("add(A([int, ...]), y=B([])) -> [int, ...]",
                             [2, 'two'], __tmp8, A([2, 'two']), y=__typ0([]))

    def __tmp3(__tmp1) -> None:
        class A(Dict[Any, Any]):
            pass

        def to_A(v: Iterable[Tuple[Any, Any]]=[]) :
            return A(v)

        __tmp1.check_signature("to_A() -> A([])", A(()), to_A)
        __tmp1.check_signature("to_A([(int, str)]) -> A([(int, str)])",
                             {2: 'two'}, to_A, [(2, 'two')])
        __tmp1.check_signature("to_A([(int, str), ...]) -> A([(int, str), ...])",
                             {1: 'one', 2: 'two'}, to_A, [(1, 'one'), (2, 'two')])
        __tmp1.check_signature("to_A(((int, str), (int, str))) -> A([(int, str), ...])",
                             {1: 'one', 2: 'two'}, to_A, ((1, 'one'), (2, 'two')))

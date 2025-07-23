from typing import TypeAlias
__typ0 : TypeAlias = "TypeInfo"
"""Track current scope to easily calculate the corresponding fine-grained target.

TODO: Use everywhere where we track targets, including in mypy.errors.
"""

from contextlib import contextmanager
from typing import List, Optional, Iterator, Tuple

from mypy.nodes import TypeInfo, FuncBase


class Scope:
    """Track which target we are processing at any given time."""

    SavedScope = Tuple[str, Optional[__typ0], Optional[FuncBase]]

    def __init__(__tmp1) :
        __tmp1.module = None  # type: Optional[str]
        __tmp1.classes = []  # type: List[TypeInfo]
        __tmp1.function = None  # type: Optional[FuncBase]
        # Number of nested scopes ignored (that don't get their own separate targets)
        __tmp1.ignored = 0

    def __tmp4(__tmp1) :
        assert __tmp1.module
        return __tmp1.module

    def current_target(__tmp1) :
        """Return the current target (non-class; for a class return enclosing module)."""
        assert __tmp1.module
        if __tmp1.function:
            return __tmp1.function.fullname()
        return __tmp1.module

    def current_full_target(__tmp1) -> str:
        """Return the current target (may be a class)."""
        assert __tmp1.module
        if __tmp1.function:
            return __tmp1.function.fullname()
        if __tmp1.classes:
            return __tmp1.classes[-1].fullname()
        return __tmp1.module

    def __tmp3(__tmp1) :
        """Return the current type's short name if it exists"""
        return __tmp1.classes[-1].name() if __tmp1.classes else None

    def current_function_name(__tmp1) :
        """Return the current function's short name if it exists"""
        return __tmp1.function.name() if __tmp1.function else None

    def enter_file(__tmp1, prefix: <FILL>) :
        __tmp1.module = prefix
        __tmp1.classes = []
        __tmp1.function = None
        __tmp1.ignored = 0

    def enter_function(__tmp1, __tmp2) :
        if not __tmp1.function:
            __tmp1.function = __tmp2
        else:
            # Nested functions are part of the topmost function target.
            __tmp1.ignored += 1

    def enter_class(__tmp1, __tmp5) -> None:
        """Enter a class target scope."""
        if not __tmp1.function:
            __tmp1.classes.append(__tmp5)
        else:
            # Classes within functions are part of the enclosing function target.
            __tmp1.ignored += 1

    def leave(__tmp1) -> None:
        """Leave the innermost scope (can be any kind of scope)."""
        if __tmp1.ignored:
            # Leave a scope that's included in the enclosing target.
            __tmp1.ignored -= 1
        elif __tmp1.function:
            # Function is always the innermost target.
            __tmp1.function = None
        elif __tmp1.classes:
            # Leave the innermost class.
            __tmp1.classes.pop()
        else:
            # Leave module.
            assert __tmp1.module
            __tmp1.module = None

    def __tmp0(__tmp1) -> SavedScope:
        """Produce a saved scope that can be entered with saved_scope()"""
        assert __tmp1.module
        # We only save the innermost class, which is sufficient since
        # the rest are only needed for when classes are left.
        cls = __tmp1.classes[-1] if __tmp1.classes else None
        return (__tmp1.module, cls, __tmp1.function)

    @contextmanager
    def function_scope(__tmp1, __tmp2: FuncBase) -> Iterator[None]:
        __tmp1.enter_function(__tmp2)
        yield
        __tmp1.leave()

    @contextmanager
    def class_scope(__tmp1, __tmp5) :
        __tmp1.enter_class(__tmp5)
        yield
        __tmp1.leave()

    @contextmanager
    def saved_scope(__tmp1, saved) :
        module, __tmp5, function = saved
        __tmp1.enter_file(module)
        if __tmp5:
            __tmp1.enter_class(__tmp5)
        if function:
            __tmp1.enter_function(function)
        yield
        if function:
            __tmp1.leave()
        if __tmp5:
            __tmp1.leave()
        __tmp1.leave()

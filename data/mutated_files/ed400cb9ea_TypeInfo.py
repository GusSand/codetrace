from typing import TypeAlias
__typ3 : TypeAlias = "FuncBase"
__typ1 : TypeAlias = "str"
"""Track current scope to easily calculate the corresponding fine-grained target.

TODO: Use everywhere where we track targets, including in mypy.errors.
"""

from contextlib import contextmanager
from typing import List, Optional, Iterator, Tuple

from mypy.nodes import TypeInfo, FuncBase


class __typ2:
    """Track which target we are processing at any given time."""

    __typ0 = Tuple[__typ1, Optional[TypeInfo], Optional[__typ3]]

    def __init__(self) -> None:
        self.module = None  # type: Optional[str]
        self.classes = []  # type: List[TypeInfo]
        self.function = None  # type: Optional[FuncBase]
        # Number of nested scopes ignored (that don't get their own separate targets)
        self.ignored = 0

    def __tmp5(self) :
        assert self.module
        return self.module

    def __tmp1(self) :
        """Return the current target (non-class; for a class return enclosing module)."""
        assert self.module
        if self.function:
            return self.function.fullname()
        return self.module

    def __tmp2(self) -> __typ1:
        """Return the current target (may be a class)."""
        assert self.module
        if self.function:
            return self.function.fullname()
        if self.classes:
            return self.classes[-1].fullname()
        return self.module

    def __tmp4(self) :
        """Return the current type's short name if it exists"""
        return self.classes[-1].name() if self.classes else None

    def __tmp0(self) :
        """Return the current function's short name if it exists"""
        return self.function.name() if self.function else None

    def enter_file(self, prefix: __typ1) -> None:
        self.module = prefix
        self.classes = []
        self.function = None
        self.ignored = 0

    def enter_function(self, __tmp3) :
        if not self.function:
            self.function = __tmp3
        else:
            # Nested functions are part of the topmost function target.
            self.ignored += 1

    def enter_class(self, info: <FILL>) :
        """Enter a class target scope."""
        if not self.function:
            self.classes.append(info)
        else:
            # Classes within functions are part of the enclosing function target.
            self.ignored += 1

    def leave(self) -> None:
        """Leave the innermost scope (can be any kind of scope)."""
        if self.ignored:
            # Leave a scope that's included in the enclosing target.
            self.ignored -= 1
        elif self.function:
            # Function is always the innermost target.
            self.function = None
        elif self.classes:
            # Leave the innermost class.
            self.classes.pop()
        else:
            # Leave module.
            assert self.module
            self.module = None

    def save(self) :
        """Produce a saved scope that can be entered with saved_scope()"""
        assert self.module
        # We only save the innermost class, which is sufficient since
        # the rest are only needed for when classes are left.
        cls = self.classes[-1] if self.classes else None
        return (self.module, cls, self.function)

    @contextmanager
    def function_scope(self, __tmp3) :
        self.enter_function(__tmp3)
        yield
        self.leave()

    @contextmanager
    def class_scope(self, info) :
        self.enter_class(info)
        yield
        self.leave()

    @contextmanager
    def saved_scope(self, saved) :
        module, info, function = saved
        self.enter_file(module)
        if info:
            self.enter_class(info)
        if function:
            self.enter_function(function)
        yield
        if function:
            self.leave()
        if info:
            self.leave()
        self.leave()

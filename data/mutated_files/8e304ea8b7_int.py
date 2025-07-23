from typing import TypeAlias
__typ4 : TypeAlias = "MypyFile"
__typ2 : TypeAlias = "str"
__typ0 : TypeAlias = "Context"
__typ1 : TypeAlias = "SymbolTableNode"
"""Shared definitions used by different parts of semantic analysis."""

from abc import abstractmethod
from typing import Optional

from mypy.nodes import Context, SymbolTableNode, MypyFile, ImportedName, GDEF
from mypy.util import correct_relative_import


# Priorities for ordering of patches within the final "patch" phase of semantic analysis
# (after pass 3):

# Fix forward references (needs to happen first)
PRIORITY_FORWARD_REF = 0
# Fix fallbacks (does joins)
PRIORITY_FALLBACKS = 1
# Checks type var values (does subtype checks)
PRIORITY_TYPEVAR_VALUES = 2


class __typ3:
    """A limited abstract interface to some generic semantic analyzer functionality.

    We use this interface for various reasons:

    * Looser coupling
    * Cleaner import graph
    * Less need to pass around callback functions
    """

    @abstractmethod
    def __tmp2(__tmp1, __tmp11, __tmp4: __typ0,
                         suppress_errors: bool = False) :
        raise NotImplementedError

    @abstractmethod
    def __tmp0(__tmp1, __tmp11: __typ2) :
        raise NotImplementedError

    @abstractmethod
    def __tmp7(
            __tmp1, node: Optional[__typ1]) :
        raise NotImplementedError

    @abstractmethod
    def __tmp3(__tmp1, __tmp9, __tmp4, serious: bool = False, *,
             blocker: bool = False) :
        raise NotImplementedError

    @abstractmethod
    def __tmp10(__tmp1, __tmp9: __typ2, __tmp4) -> None:
        raise NotImplementedError


def __tmp8(__tmp12: __typ4,
                                  __tmp5,
                                  relative: <FILL>,
                                  __tmp6: __typ2) :
    """Create symbol table entry for a name imported from another module.

    These entries act as indirect references.
    """
    target_module, ok = correct_relative_import(
        __tmp12.fullname(),
        relative,
        __tmp5,
        __tmp12.is_package_init_file())
    if not ok:
        return None
    target_name = '%s.%s' % (target_module, __tmp6)
    link = ImportedName(target_name)
    # Use GDEF since this refers to a module-level definition.
    return __typ1(GDEF, link)

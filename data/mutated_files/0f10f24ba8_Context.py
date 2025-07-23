from typing import TypeAlias
__typ2 : TypeAlias = "SymbolTableNode"
__typ0 : TypeAlias = "MypyFile"
__typ3 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
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


class SemanticAnalyzerInterface:
    """A limited abstract interface to some generic semantic analyzer functionality.

    We use this interface for various reasons:

    * Looser coupling
    * Cleaner import graph
    * Less need to pass around callback functions
    """

    @abstractmethod
    def __tmp1(__tmp0, __tmp9: __typ3, __tmp3: Context,
                         suppress_errors: bool = False) -> Optional[__typ2]:
        raise NotImplementedError

    @abstractmethod
    def lookup_fully_qualified(__tmp0, __tmp9) :
        raise NotImplementedError

    @abstractmethod
    def __tmp6(
            __tmp0, node: Optional[__typ2]) -> Optional[__typ2]:
        raise NotImplementedError

    @abstractmethod
    def __tmp2(__tmp0, __tmp7: __typ3, __tmp3, serious: bool = False, *,
             blocker: bool = False) :
        raise NotImplementedError

    @abstractmethod
    def __tmp8(__tmp0, __tmp7: __typ3, __tmp3: <FILL>) -> None:
        raise NotImplementedError


def create_indirect_imported_name(__tmp10,
                                  __tmp4,
                                  relative,
                                  __tmp5) :
    """Create symbol table entry for a name imported from another module.

    These entries act as indirect references.
    """
    target_module, ok = correct_relative_import(
        __tmp10.fullname(),
        relative,
        __tmp4,
        __tmp10.is_package_init_file())
    if not ok:
        return None
    target_name = '%s.%s' % (target_module, __tmp5)
    link = ImportedName(target_name)
    # Use GDEF since this refers to a module-level definition.
    return __typ2(GDEF, link)

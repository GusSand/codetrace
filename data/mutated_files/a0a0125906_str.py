from typing import TypeAlias
__typ0 : TypeAlias = "Context"
__typ2 : TypeAlias = "int"
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


class SemanticAnalyzerInterface:
    """A limited abstract interface to some generic semantic analyzer functionality.

    We use this interface for various reasons:

    * Looser coupling
    * Cleaner import graph
    * Less need to pass around callback functions
    """

    @abstractmethod
    def lookup_qualified(__tmp0, __tmp4: <FILL>, __tmp2: __typ0,
                         suppress_errors: bool = False) -> Optional[__typ1]:
        raise NotImplementedError

    @abstractmethod
    def lookup_fully_qualified(__tmp0, __tmp4) -> __typ1:
        raise NotImplementedError

    @abstractmethod
    def dereference_module_cross_ref(
            __tmp0, node: Optional[__typ1]) -> Optional[__typ1]:
        raise NotImplementedError

    @abstractmethod
    def __tmp1(__tmp0, msg, __tmp2, serious: bool = False, *,
             blocker: bool = False) -> None:
        raise NotImplementedError

    @abstractmethod
    def note(__tmp0, msg: str, __tmp2: __typ0) -> None:
        raise NotImplementedError


def create_indirect_imported_name(__tmp5: MypyFile,
                                  __tmp3: str,
                                  relative,
                                  imported_name) :
    """Create symbol table entry for a name imported from another module.

    These entries act as indirect references.
    """
    target_module, ok = correct_relative_import(
        __tmp5.fullname(),
        relative,
        __tmp3,
        __tmp5.is_package_init_file())
    if not ok:
        return None
    target_name = '%s.%s' % (target_module, imported_name)
    link = ImportedName(target_name)
    # Use GDEF since this refers to a module-level definition.
    return __typ1(GDEF, link)

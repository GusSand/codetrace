from typing import TypeAlias
__typ0 : TypeAlias = "Context"
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
    def lookup_qualified(__tmp1, __tmp4, ctx: __typ0,
                         suppress_errors: bool = False) -> Optional[SymbolTableNode]:
        raise NotImplementedError

    @abstractmethod
    def __tmp0(__tmp1, __tmp4: str) -> SymbolTableNode:
        raise NotImplementedError

    @abstractmethod
    def dereference_module_cross_ref(
            __tmp1, node) -> Optional[SymbolTableNode]:
        raise NotImplementedError

    @abstractmethod
    def fail(__tmp1, msg, ctx: __typ0, serious: bool = False, *,
             blocker: bool = False) -> None:
        raise NotImplementedError

    @abstractmethod
    def note(__tmp1, msg, ctx: __typ0) -> None:
        raise NotImplementedError


def __tmp3(file_node: MypyFile,
                                  module: <FILL>,
                                  relative,
                                  __tmp2: str) -> Optional[SymbolTableNode]:
    """Create symbol table entry for a name imported from another module.

    These entries act as indirect references.
    """
    target_module, ok = correct_relative_import(
        file_node.fullname(),
        relative,
        module,
        file_node.is_package_init_file())
    if not ok:
        return None
    target_name = '%s.%s' % (target_module, __tmp2)
    link = ImportedName(target_name)
    # Use GDEF since this refers to a module-level definition.
    return SymbolTableNode(GDEF, link)

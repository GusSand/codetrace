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
    def __tmp1(__tmp0, __tmp5, ctx: Context,
                         suppress_errors: bool = False) :
        raise NotImplementedError

    @abstractmethod
    def lookup_fully_qualified(__tmp0, __tmp5: <FILL>) :
        raise NotImplementedError

    @abstractmethod
    def __tmp3(
            __tmp0, node) :
        raise NotImplementedError

    @abstractmethod
    def __tmp2(__tmp0, msg, ctx, serious: bool = False, *,
             blocker: bool = False) -> None:
        raise NotImplementedError

    @abstractmethod
    def note(__tmp0, msg, ctx) :
        raise NotImplementedError


def __tmp4(file_node,
                                  module,
                                  relative,
                                  imported_name) :
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
    target_name = '%s.%s' % (target_module, imported_name)
    link = ImportedName(target_name)
    # Use GDEF since this refers to a module-level definition.
    return SymbolTableNode(GDEF, link)

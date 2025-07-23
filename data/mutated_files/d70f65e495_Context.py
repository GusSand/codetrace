from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
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
    def lookup_qualified(__tmp1, name, __tmp8: Context,
                         suppress_errors: bool = False) :
        raise NotImplementedError

    @abstractmethod
    def __tmp0(__tmp1, name) :
        raise NotImplementedError

    @abstractmethod
    def dereference_module_cross_ref(
            __tmp1, node) :
        raise NotImplementedError

    @abstractmethod
    def __tmp2(__tmp1, __tmp6, __tmp8: <FILL>, serious: bool = False, *,
             blocker: bool = False) :
        raise NotImplementedError

    @abstractmethod
    def __tmp7(__tmp1, __tmp6, __tmp8) :
        raise NotImplementedError


def __tmp5(__tmp9,
                                  __tmp3,
                                  relative,
                                  __tmp4) :
    """Create symbol table entry for a name imported from another module.

    These entries act as indirect references.
    """
    target_module, ok = correct_relative_import(
        __tmp9.fullname(),
        relative,
        __tmp3,
        __tmp9.is_package_init_file())
    if not ok:
        return None
    target_name = '%s.%s' % (target_module, __tmp4)
    link = ImportedName(target_name)
    # Use GDEF since this refers to a module-level definition.
    return __typ1(GDEF, link)

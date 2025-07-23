from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "TypeVarExpr"
from typing import Optional, Dict, Union
from mypy.types import TypeVarDef, TypeVarId
from mypy.nodes import TypeVarExpr, SymbolTableNode


class __typ1:
    """Scope that holds bindings for type variables. Node fullname -> TypeVarDef."""

    def __tmp3(__tmp0,
                 parent: 'Optional[TypeVarScope]' = None,
                 is_class_scope: __typ2 = False,
                 prohibited: 'Optional[TypeVarScope]' = None) -> None:
        """Initializer for TypeVarScope

        Parameters:
          parent: the outer scope for this scope
          is_class_scope: True if this represents a generic class
          prohibited: Type variables that aren't strictly in scope exactly,
                      but can't be bound because they're part of an outer class's scope.
        """
        __tmp0.scope = {}  # type: Dict[str, TypeVarDef]
        __tmp0.parent = parent
        __tmp0.func_id = 0
        __tmp0.class_id = 0
        __tmp0.is_class_scope = is_class_scope
        __tmp0.prohibited = prohibited
        if parent is not None:
            __tmp0.func_id = parent.func_id
            __tmp0.class_id = parent.class_id

    def get_function_scope(__tmp0) -> 'Optional[TypeVarScope]':
        """Get the nearest parent that's a function scope, not a class scope"""
        it = __tmp0  # type: Optional[TypeVarScope]
        while it is not None and it.is_class_scope:
            it = it.parent
        return it

    def allow_binding(__tmp0, fullname: <FILL>) :
        if fullname in __tmp0.scope:
            return False
        elif __tmp0.parent and not __tmp0.parent.allow_binding(fullname):
            return False
        elif __tmp0.prohibited and not __tmp0.prohibited.allow_binding(fullname):
            return False
        return True

    def __tmp2(__tmp0) :
        """A new scope frame for binding a method"""
        return __typ1(__tmp0, False, None)

    def class_frame(__tmp0) -> 'TypeVarScope':
        """A new scope frame for binding a class. Prohibits *this* class's tvars"""
        return __typ1(__tmp0.get_function_scope(), True, __tmp0)

    def bind_new(__tmp0, name: str, tvar_expr) :
        if __tmp0.is_class_scope:
            __tmp0.class_id += 1
            i = __tmp0.class_id
        else:
            __tmp0.func_id -= 1
            i = __tmp0.func_id
        __tmp4 = TypeVarDef(name,
                              tvar_expr.fullname(),
                              i,
                              values=tvar_expr.values,
                              upper_bound=tvar_expr.upper_bound,
                              variance=tvar_expr.variance,
                              line=tvar_expr.line,
                              column=tvar_expr.column)
        __tmp0.scope[tvar_expr.fullname()] = __tmp4
        return __tmp4

    def bind_existing(__tmp0, __tmp4) :
        __tmp0.scope[__tmp4.fullname] = __tmp4

    def get_binding(__tmp0, __tmp1: Union[str, SymbolTableNode]) -> Optional[TypeVarDef]:
        fullname = __tmp1.fullname if isinstance(__tmp1, SymbolTableNode) else __tmp1
        assert fullname is not None
        if fullname in __tmp0.scope:
            return __tmp0.scope[fullname]
        elif __tmp0.parent is not None:
            return __tmp0.parent.get_binding(fullname)
        else:
            return None

    def __tmp5(__tmp0) :
        me = ", ".join('{}: {}`{}'.format(k, v.name, v.id) for k, v in __tmp0.scope.items())
        if __tmp0.parent is None:
            return me
        return "{} <- {}".format(str(__tmp0.parent), me)

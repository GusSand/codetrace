from typing import Optional, Dict, Union
from mypy.types import TypeVarDef, TypeVarId
from mypy.nodes import TypeVarExpr, SymbolTableNode


class TypeVarScope:
    """Scope that holds bindings for type variables. Node fullname -> TypeVarDef."""

    def __tmp6(__tmp1,
                 parent: 'Optional[TypeVarScope]' = None,
                 is_class_scope: bool = False,
                 prohibited: 'Optional[TypeVarScope]' = None) -> None:
        """Initializer for TypeVarScope

        Parameters:
          parent: the outer scope for this scope
          is_class_scope: True if this represents a generic class
          prohibited: Type variables that aren't strictly in scope exactly,
                      but can't be bound because they're part of an outer class's scope.
        """
        __tmp1.scope = {}  # type: Dict[str, TypeVarDef]
        __tmp1.parent = parent
        __tmp1.func_id = 0
        __tmp1.class_id = 0
        __tmp1.is_class_scope = is_class_scope
        __tmp1.prohibited = prohibited
        if parent is not None:
            __tmp1.func_id = parent.func_id
            __tmp1.class_id = parent.class_id

    def get_function_scope(__tmp1) -> 'Optional[TypeVarScope]':
        """Get the nearest parent that's a function scope, not a class scope"""
        it = __tmp1  # type: Optional[TypeVarScope]
        while it is not None and it.is_class_scope:
            it = it.parent
        return it

    def allow_binding(__tmp1, fullname: str) :
        if fullname in __tmp1.scope:
            return False
        elif __tmp1.parent and not __tmp1.parent.allow_binding(fullname):
            return False
        elif __tmp1.prohibited and not __tmp1.prohibited.allow_binding(fullname):
            return False
        return True

    def __tmp4(__tmp1) -> 'TypeVarScope':
        """A new scope frame for binding a method"""
        return TypeVarScope(__tmp1, False, None)

    def __tmp0(__tmp1) :
        """A new scope frame for binding a class. Prohibits *this* class's tvars"""
        return TypeVarScope(__tmp1.get_function_scope(), True, __tmp1)

    def __tmp3(__tmp1, name: <FILL>, __tmp5) :
        if __tmp1.is_class_scope:
            __tmp1.class_id += 1
            i = __tmp1.class_id
        else:
            __tmp1.func_id -= 1
            i = __tmp1.func_id
        __tmp7 = TypeVarDef(name,
                              __tmp5.fullname(),
                              i,
                              values=__tmp5.values,
                              upper_bound=__tmp5.upper_bound,
                              variance=__tmp5.variance,
                              line=__tmp5.line,
                              column=__tmp5.column)
        __tmp1.scope[__tmp5.fullname()] = __tmp7
        return __tmp7

    def __tmp9(__tmp1, __tmp7: TypeVarDef) :
        __tmp1.scope[__tmp7.fullname] = __tmp7

    def get_binding(__tmp1, __tmp2) :
        fullname = __tmp2.fullname if isinstance(__tmp2, SymbolTableNode) else __tmp2
        assert fullname is not None
        if fullname in __tmp1.scope:
            return __tmp1.scope[fullname]
        elif __tmp1.parent is not None:
            return __tmp1.parent.get_binding(fullname)
        else:
            return None

    def __tmp8(__tmp1) -> str:
        me = ", ".join('{}: {}`{}'.format(k, v.name, v.id) for k, v in __tmp1.scope.items())
        if __tmp1.parent is None:
            return me
        return "{} <- {}".format(str(__tmp1.parent), me)

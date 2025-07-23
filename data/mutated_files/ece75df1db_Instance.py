from typing import TypeAlias
__typ0 : TypeAlias = "TypeInfo"
from typing import Dict, List

from mypy.expandtype import expand_type
from mypy.nodes import TypeInfo
from mypy.types import Type, TypeVarId, Instance, AnyType, TypeOfAny


def __tmp5(__tmp0: <FILL>,
                              __tmp4: __typ0) -> Instance:
    """Produce a supertype of `instance` that is an Instance
    of `superclass`, mapping type arguments up the chain of bases.

    If `superclass` is not a nominal superclass of `instance.type`,
    then all type arguments are mapped to 'Any'.
    """
    if __tmp0.type == __tmp4:
        # Fast path: `instance` already belongs to `superclass`.
        return __tmp0

    if not __tmp4.type_vars:
        # Fast path: `superclass` has no type variables to map to.
        return Instance(__tmp4, [])

    return __tmp1(__tmp0, __tmp4)[0]


def __tmp1(__tmp0: Instance,
                               __tmp3: __typ0) -> List[Instance]:
    # FIX: Currently we should only have one supertype per interface, so no
    #      need to return an array
    result = []  # type: List[Instance]
    for path in class_derivation_paths(__tmp0.type, __tmp3):
        types = [__tmp0]
        for sup in path:
            a = []  # type: List[Instance]
            for t in types:
                a.extend(__tmp2(t, sup))
            types = a
        result.extend(types)
    if result:
        return result
    else:
        # Nothing. Presumably due to an error. Construct a dummy using Any.
        any_type = AnyType(TypeOfAny.from_error)
        return [Instance(__tmp3, [any_type] * len(__tmp3.type_vars))]


def class_derivation_paths(typ: __typ0,
                           __tmp3: __typ0) -> List[List[__typ0]]:
    """Return an array of non-empty paths of direct base classes from
    type to supertype.  Return [] if no such path could be found.

      InterfaceImplementationPaths(A, B) == [[B]] if A inherits B
      InterfaceImplementationPaths(A, C) == [[B, C]] if A inherits B and
                                                        B inherits C
    """
    # FIX: Currently we might only ever have a single path, so this could be
    #      simplified
    result = []  # type: List[List[TypeInfo]]

    for base in typ.bases:
        btype = base.type
        if btype == __tmp3:
            result.append([btype])
        else:
            # Try constructing a longer path via the base class.
            for path in class_derivation_paths(btype, __tmp3):
                result.append([btype] + path)

    return result


def __tmp2(__tmp0: Instance,
                                      __tmp3: __typ0) -> List[Instance]:
    # FIX: There should only be one supertypes, always.
    typ = __tmp0.type
    result = []  # type: List[Instance]

    for b in typ.bases:
        if b.type == __tmp3:
            env = __tmp6(__tmp0)
            t = expand_type(b, env)
            assert isinstance(t, Instance)
            result.append(t)

    if result:
        return result
    else:
        # Relationship with the supertype not specified explicitly. Use dynamic
        # type arguments implicitly.
        any_type = AnyType(TypeOfAny.unannotated)
        return [Instance(__tmp3, [any_type] * len(__tmp3.type_vars))]


def __tmp6(__tmp0: Instance) :
    """Given an Instance, produce the resulting type environment for type
    variables bound by the Instance's class definition.

    An Instance is a type application of a class (a TypeInfo) to its
    required number of type arguments.  So this environment consists
    of the class's type variables mapped to the Instance's actual
    arguments.  The type variables are mapped by their `id`.

    """
    return {binder.id: arg for binder, arg in zip(__tmp0.type.defn.type_vars, __tmp0.args)}

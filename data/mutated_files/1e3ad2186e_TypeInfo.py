from typing import TypeAlias
__typ0 : TypeAlias = "Instance"
from typing import Dict, List

from mypy.expandtype import expand_type
from mypy.nodes import TypeInfo
from mypy.types import Type, TypeVarId, Instance, AnyType, TypeOfAny


def __tmp4(__tmp1,
                              __tmp3) :
    """Produce a supertype of `instance` that is an Instance
    of `superclass`, mapping type arguments up the chain of bases.

    If `superclass` is not a nominal superclass of `instance.type`,
    then all type arguments are mapped to 'Any'.
    """
    if __tmp1.type == __tmp3:
        # Fast path: `instance` already belongs to `superclass`.
        return __tmp1

    if not __tmp3.type_vars:
        # Fast path: `superclass` has no type variables to map to.
        return __typ0(__tmp3, [])

    return map_instance_to_supertypes(__tmp1, __tmp3)[0]


def map_instance_to_supertypes(__tmp1,
                               __tmp2: <FILL>) :
    # FIX: Currently we should only have one supertype per interface, so no
    #      need to return an array
    result = []  # type: List[Instance]
    for path in __tmp0(__tmp1.type, __tmp2):
        types = [__tmp1]
        for sup in path:
            a = []  # type: List[Instance]
            for t in types:
                a.extend(map_instance_to_direct_supertypes(t, sup))
            types = a
        result.extend(types)
    if result:
        return result
    else:
        # Nothing. Presumably due to an error. Construct a dummy using Any.
        any_type = AnyType(TypeOfAny.from_error)
        return [__typ0(__tmp2, [any_type] * len(__tmp2.type_vars))]


def __tmp0(typ,
                           __tmp2) :
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
        if btype == __tmp2:
            result.append([btype])
        else:
            # Try constructing a longer path via the base class.
            for path in __tmp0(btype, __tmp2):
                result.append([btype] + path)

    return result


def map_instance_to_direct_supertypes(__tmp1,
                                      __tmp2) :
    # FIX: There should only be one supertypes, always.
    typ = __tmp1.type
    result = []  # type: List[Instance]

    for b in typ.bases:
        if b.type == __tmp2:
            env = __tmp5(__tmp1)
            t = expand_type(b, env)
            assert isinstance(t, __typ0)
            result.append(t)

    if result:
        return result
    else:
        # Relationship with the supertype not specified explicitly. Use dynamic
        # type arguments implicitly.
        any_type = AnyType(TypeOfAny.unannotated)
        return [__typ0(__tmp2, [any_type] * len(__tmp2.type_vars))]


def __tmp5(__tmp1) :
    """Given an Instance, produce the resulting type environment for type
    variables bound by the Instance's class definition.

    An Instance is a type application of a class (a TypeInfo) to its
    required number of type arguments.  So this environment consists
    of the class's type variables mapped to the Instance's actual
    arguments.  The type variables are mapped by their `id`.

    """
    return {binder.id: arg for binder, arg in zip(__tmp1.type.defn.type_vars, __tmp1.args)}

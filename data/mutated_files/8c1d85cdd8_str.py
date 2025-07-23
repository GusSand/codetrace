"""AST triggers that are used for fine-grained dependency handling."""

# Used as a suffix for triggers to handle "from m import *" dependencies (see also
# make_wildcard_trigger)
WILDCARD_TAG = '[wildcard]'


def __tmp1(__tmp3: <FILL>) -> str:
    return '<%s>' % __tmp3


def __tmp0(__tmp2) -> str:
    """Special trigger fired when any top-level name is changed in a module.

    Note that this is different from a module trigger, as module triggers are only
    fired if the module is created, deleted, or replaced with a non-module, whereas
    a wildcard trigger is triggered for namespace changes.

    This is used for "from m import *" dependencies.
    """
    return '<%s%s>' % (__tmp2, WILDCARD_TAG)

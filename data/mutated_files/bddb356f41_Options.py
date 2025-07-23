from typing import TypeAlias
__typ0 : TypeAlias = "MypyFile"
from typing import List, Tuple, Set, cast, Union, Optional

from mypy.errors import Errors
from mypy.options import Options
from mypy.nodes import MypyFile


def parse(__tmp0: Union[str, bytes],
          __tmp2: str,
          __tmp1,
          errors: Optional[Errors],
          options: <FILL>) :
    """Parse a source file, without doing any semantic analysis.

    Return the parse tree. If errors is not provided, raise ParseError
    on failure. Otherwise, use the errors object to report parse errors.

    The python_version (major, minor) option determines the Python syntax variant.
    """
    is_stub_file = __tmp2.endswith('.pyi')
    if options.python_version[0] >= 3 or is_stub_file:
        import mypy.fastparse
        return mypy.fastparse.parse(__tmp0,
                                    __tmp2=__tmp2,
                                    __tmp1=__tmp1,
                                    errors=errors,
                                    options=options)
    else:
        import mypy.fastparse2
        return mypy.fastparse2.parse(__tmp0,
                                     __tmp2=__tmp2,
                                     __tmp1=__tmp1,
                                     errors=errors,
                                     options=options)

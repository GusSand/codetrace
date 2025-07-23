from typing import TypeAlias
__typ1 : TypeAlias = "str"
# See readme.md for instructions on running this code.

from typing import Any, Dict

class __typ0(object):
    def __tmp1(__tmp0) :
        return '''
        This is a boilerplate bot that responds to a user query with
        "beep boop", which is robot for "Hello World".

        This bot can be used as a template for other, more
        sophisticated, bots.
        '''

    def __tmp3(__tmp0, message, __tmp2: <FILL>) -> None:
        content = 'beep boop'  # type: str
        __tmp2.send_reply(message, content)

handler_class = __typ0

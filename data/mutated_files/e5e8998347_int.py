from typing import TypeAlias
__typ1 : TypeAlias = "str"

class __typ0(object):

    def __tmp1(

            __tmp0,
            sk_id:       <FILL>,
            displayName):

            __tmp0.sk_id = sk_id
            __tmp0.displayName = displayName

    def __tmp2(__tmp0):

            return " \n" \
            "ID: {}  \n" \
            "Name: {}\n".format(

            __typ1(__tmp0.sk_id),
            __tmp0.displayName)

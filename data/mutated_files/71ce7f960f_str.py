from typing import TypeAlias
__typ1 : TypeAlias = "int"

class __typ0(object):

    def __init__(

            self,
            sk_id,
            displayName: <FILL>):

            self.sk_id = sk_id
            self.displayName = displayName

    def __str__(self):

            return " \n" \
            "ID: {}  \n" \
            "Name: {}\n".format(

            str(self.sk_id),
            self.displayName)

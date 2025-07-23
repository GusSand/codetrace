from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "Command"
__typ1 : TypeAlias = "str"
from argparse import ArgumentParser
from typing import Any

from zerver.lib.initial_password import initial_password
from zerver.lib.management import ZulipBaseCommand
from zerver.lib.users import get_api_key

class __typ0(ZulipBaseCommand):
    help = "Print the initial password and API key for accounts as created by populate_db"

    fmt = '%-30s %-16s  %-32s'

    def __tmp0(__tmp1, __tmp2: <FILL>) :
        __tmp2.add_argument('emails', metavar='<email>', type=__typ1, nargs='*',
                            help="email of user to show password and API key for")
        __tmp1.add_realm_args(__tmp2)

    def __tmp3(__tmp1, *args, **options) :
        realm = __tmp1.get_realm(options)
        print(__tmp1.fmt % ('email', 'password', 'API key'))
        for email in options['emails']:
            if '@' not in email:
                print('ERROR: %s does not look like an email address' % (email,))
                continue
            user = __tmp1.get_user(email, realm)
            print(__tmp1.fmt % (email, initial_password(email), get_api_key(user)))

from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"

from argparse import ArgumentParser
from typing import Any

from django.core.management.base import CommandError

from zerver.lib.actions import do_mark_all_as_read
from zerver.lib.management import ZulipBaseCommand
from zerver.models import Message

class __typ0(ZulipBaseCommand):
    help = """Bankrupt one or many users."""

    def __tmp0(__tmp1, __tmp2: __typ1) -> None:
        __tmp2.add_argument('emails', metavar='<email>', type=str, nargs='+',
                            help='email address to bankrupt')
        __tmp1.add_realm_args(__tmp2, True)

    def __tmp3(__tmp1, *args: __typ2, **options: <FILL>) -> None:
        realm = __tmp1.get_realm(options)
        for email in options['emails']:
            try:
                user_profile = __tmp1.get_user(email, realm)
            except CommandError:
                print("e-mail %s doesn't exist in the realm %s, skipping" % (email, realm))
                continue
            do_mark_all_as_read(user_profile, __tmp1.get_client())

            messages = Message.objects.filter(
                usermessage__user_profile=user_profile).order_by('-id')[:1]
            if messages:
                old_pointer = user_profile.pointer
                new_pointer = messages[0].id
                user_profile.pointer = new_pointer
                user_profile.save(update_fields=["pointer"])
                print("%s: %d => %d" % (email, old_pointer, new_pointer))
            else:
                print("%s has no messages, can't bankrupt!" % (email,))

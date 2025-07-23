from typing import TypeAlias
__typ0 : TypeAlias = "str"
from typing import Any, Dict
from django.utils.translation import ugettext as _

from zerver.models import UserProfile
from zerver.lib.actions import do_set_user_display_setting
from zerver.lib.exceptions import JsonableError

def process_zcommands(__tmp0: __typ0, __tmp1: <FILL>) -> Dict[__typ0, Any]:
    if not __tmp0.startswith('/'):
        raise JsonableError(_('There should be a leading slash in the zcommand.'))
    command = __tmp0[1:]

    if command == 'ping':
        ret = dict()  # type: Dict[str, Any]
        return ret

    night_commands = ['night', 'dark']
    day_commands = ['day', 'light']

    if command in night_commands:
        if __tmp1.night_mode:
            msg = 'You are still in night mode.'
        else:
            switch_command = day_commands[night_commands.index(command)]
            msg = 'Changed to night mode! To revert night mode, type `/%s`.' % (switch_command,)
            do_set_user_display_setting(__tmp1, 'night_mode', True)
        ret = dict(msg=msg)
        return ret

    if command in day_commands:
        if __tmp1.night_mode:
            switch_command = night_commands[day_commands.index(command)]
            msg = 'Changed to day mode! To revert day mode, type `/%s`.' % (switch_command,)
            do_set_user_display_setting(__tmp1, 'night_mode', False)
        else:
            msg = 'You are still in day mode.'
        ret = dict(msg=msg)
        return ret

    raise JsonableError(_('No such command: %s') % (command,))

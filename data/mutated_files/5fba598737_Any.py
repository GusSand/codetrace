from typing import TypeAlias
__typ0 : TypeAlias = "str"
# See readme.md for instructions on running this code.

from typing import Dict, Any

class __typ1(object):
    META = {
        'name': 'Incrementor',
        'description': 'Example bot to test the update_message() function.',
    }

    def usage(__tmp1) :
        return '''
        This is a boilerplate bot that makes use of the
        update_message function. For the first @-mention, it initially
        replies with one message containing a `1`. Every time the bot
        is @-mentioned, this number will be incremented in the same message.
        '''

    def __tmp0(__tmp1, __tmp2: <FILL>) -> None:
        storage = __tmp2.storage
        if not storage.contains('number') or not storage.contains('message_id'):
            storage.put('number', 0)
            storage.put('message_id', None)

    def handle_message(__tmp1, message, __tmp2) :
        storage = __tmp2.storage
        num = storage.get('number')

        # num should already be an int, but we do `int()` to force an
        # explicit type check
        num = int(num) + 1

        storage.put('number', num)
        if storage.get('message_id') is None:
            result = __tmp2.send_reply(message, __typ0(num))
            storage.put('message_id', result['id'])
        else:
            __tmp2.update_message(dict(
                message_id=storage.get('message_id'),
                content=__typ0(num)
            ))


handler_class = __typ1

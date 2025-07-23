# See readme.md for instructions on running this code.

from typing import Dict, Any

class IncrementorHandler(object):
    META = {
        'name': 'Incrementor',
        'description': 'Example bot to test the update_message() function.',
    }

    def __tmp5(__tmp2) -> str:
        return '''
        This is a boilerplate bot that makes use of the
        update_message function. For the first @-mention, it initially
        replies with one message containing a `1`. Every time the bot
        is @-mentioned, this number will be incremented in the same message.
        '''

    def __tmp4(__tmp2, __tmp3: Any) :
        storage = __tmp3.storage
        if not storage.contains('number') or not storage.contains('message_id'):
            storage.put('number', 0)
            storage.put('message_id', None)

    def __tmp1(__tmp2, __tmp0, __tmp3: <FILL>) -> None:
        storage = __tmp3.storage
        num = storage.get('number')

        # num should already be an int, but we do `int()` to force an
        # explicit type check
        num = int(num) + 1

        storage.put('number', num)
        if storage.get('message_id') is None:
            result = __tmp3.send_reply(__tmp0, str(num))
            storage.put('message_id', result['id'])
        else:
            __tmp3.update_message(dict(
                message_id=storage.get('message_id'),
                content=str(num)
            ))


handler_class = IncrementorHandler

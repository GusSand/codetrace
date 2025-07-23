from typing import TypeAlias
__typ0 : TypeAlias = "str"
# See readme.md for instructions on running this code.
from typing import Dict, Any

class __typ1(object):
    '''
    This plugin facilitates creating follow-up tasks when
    you are using Zulip to conduct a virtual meeting.  It
    looks for messages starting with '@mention-bot'.

    In this example, we write follow up items to a special
    Zulip stream called "followup," but this code could
    be adapted to write follow up items to some kind of
    external issue tracker as well.
    '''

    def usage(__tmp2) :
        return '''
            This plugin will allow users to flag messages
            as being follow-up items.  Users should preface
            messages with "@mention-bot".

            Before running this, make sure to create a stream
            called "followup" that your API user can send to.
            '''

    def __tmp1(__tmp2, __tmp3: <FILL>) :
        __tmp2.config_info = __tmp3.get_config_info('followup', optional=False)
        __tmp2.stream = __tmp2.config_info.get("stream", 'followup')

    def handle_message(__tmp2, __tmp0, __tmp3) -> None:
        if __tmp0['content'] == '':
            bot_response = "Please specify the message you want to send to followup stream after @mention-bot"
            __tmp3.send_reply(__tmp0, bot_response)
        elif __tmp0['content'] == 'help':
            __tmp3.send_reply(__tmp0, __tmp2.usage())
        else:
            bot_response = __tmp2.get_bot_followup_response(__tmp0)
            __tmp3.send_message(dict(
                type='stream',
                to=__tmp2.stream,
                subject=__tmp0['sender_email'],
                content=bot_response,
            ))

    def get_bot_followup_response(__tmp2, __tmp0) :
        original_content = __tmp0['content']
        original_sender = __tmp0['sender_email']
        temp_content = 'from %s: ' % (original_sender,)
        new_content = temp_content + original_content

        return new_content

handler_class = __typ1

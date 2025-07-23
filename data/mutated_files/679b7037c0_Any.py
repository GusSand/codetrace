# See readme.md for instructions on running this code.
from typing import Dict, Any

class FollowupHandler(object):
    '''
    This plugin facilitates creating follow-up tasks when
    you are using Zulip to conduct a virtual meeting.  It
    looks for messages starting with '@mention-bot'.

    In this example, we write follow up items to a special
    Zulip stream called "followup," but this code could
    be adapted to write follow up items to some kind of
    external issue tracker as well.
    '''

    def usage(__tmp1) -> str:
        return '''
            This plugin will allow users to flag messages
            as being follow-up items.  Users should preface
            messages with "@mention-bot".

            Before running this, make sure to create a stream
            called "followup" that your API user can send to.
            '''

    def initialize(__tmp1, __tmp2: Any) -> None:
        __tmp1.config_info = __tmp2.get_config_info('followup', optional=False)
        __tmp1.stream = __tmp1.config_info.get("stream", 'followup')

    def handle_message(__tmp1, __tmp0: Dict[str, str], __tmp2: <FILL>) -> None:
        if __tmp0['content'] == '':
            bot_response = "Please specify the message you want to send to followup stream after @mention-bot"
            __tmp2.send_reply(__tmp0, bot_response)
        elif __tmp0['content'] == 'help':
            __tmp2.send_reply(__tmp0, __tmp1.usage())
        else:
            bot_response = __tmp1.get_bot_followup_response(__tmp0)
            __tmp2.send_message(dict(
                type='stream',
                to=__tmp1.stream,
                subject=__tmp0['sender_email'],
                content=bot_response,
            ))

    def get_bot_followup_response(__tmp1, __tmp0) -> str:
        original_content = __tmp0['content']
        original_sender = __tmp0['sender_email']
        temp_content = 'from %s: ' % (original_sender,)
        new_content = temp_content + original_content

        return new_content

handler_class = FollowupHandler

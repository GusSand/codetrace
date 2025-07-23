from typing import TypeAlias
__typ0 : TypeAlias = "str"
import requests
import re
from typing import Any, Dict, Optional

class FrontHandler(object):
    FRONT_API = "https://api2.frontapp.com/conversations/{}"
    COMMANDS = [
        ('archive', "Archive a conversation."),
        ('delete', "Delete a conversation."),
        ('spam', "Mark a conversation as spam."),
        ('open', "Restore a conversation."),
        ('comment <text>', "Leave a comment.")
    ]
    CNV_ID_REGEXP = 'cnv_(?P<id>[0-9a-z]+)'
    COMMENT_PREFIX = "comment "

    def usage(__tmp2) :
        return '''
            Front Bot uses the Front REST API to interact with Front. In order to use
            Front Bot, `front.conf` must be set up. See `doc.md` for more details.
            '''

    def __tmp1(__tmp2, __tmp3: Any) -> None:
        config = __tmp3.get_config_info('front')
        api_key = config.get('api_key')
        if not api_key:
            raise KeyError("No API key specified.")

        __tmp2.auth = "Bearer " + api_key

    def help(__tmp2, __tmp3: <FILL>) :
        response = ""
        for command, description in __tmp2.COMMANDS:
            response += "`{}` {}\n".format(command, description)

        return response

    def archive(__tmp2, __tmp3) -> __typ0:
        response = requests.patch(__tmp2.FRONT_API.format(__tmp2.conversation_id),
                                  headers={"Authorization": __tmp2.auth},
                                  json={"status": "archived"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was archived."

    def delete(__tmp2, __tmp3: Any) :
        response = requests.patch(__tmp2.FRONT_API.format(__tmp2.conversation_id),
                                  headers={"Authorization": __tmp2.auth},
                                  json={"status": "deleted"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was deleted."

    def spam(__tmp2, __tmp3: Any) :
        response = requests.patch(__tmp2.FRONT_API.format(__tmp2.conversation_id),
                                  headers={"Authorization": __tmp2.auth},
                                  json={"status": "spam"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was marked as spam."

    def restore(__tmp2, __tmp3) :
        response = requests.patch(__tmp2.FRONT_API.format(__tmp2.conversation_id),
                                  headers={"Authorization": __tmp2.auth},
                                  json={"status": "open"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was restored."

    def comment(__tmp2, __tmp3, **kwargs) :
        response = requests.post(__tmp2.FRONT_API.format(__tmp2.conversation_id) + "/comments",
                                 headers={"Authorization": __tmp2.auth}, json=kwargs)

        if response.status_code not in (200, 201):
            return "Something went wrong."

        return "Comment was sent."

    def handle_message(__tmp2, __tmp0: Dict[__typ0, __typ0], __tmp3: Any) -> None:
        command = __tmp0['content']

        result = re.search(__tmp2.CNV_ID_REGEXP, __tmp0['subject'])
        if not result:
            __tmp3.send_reply(__tmp0, "No coversation ID found. Please make "
                                            "sure that the name of the topic "
                                            "contains a valid coversation ID.")
            return None

        __tmp2.conversation_id = result.group()

        if command == 'help':
            __tmp3.send_reply(__tmp0, __tmp2.help(__tmp3))

        elif command == 'archive':
            __tmp3.send_reply(__tmp0, __tmp2.archive(__tmp3))

        elif command == 'delete':
            __tmp3.send_reply(__tmp0, __tmp2.delete(__tmp3))

        elif command == 'spam':
            __tmp3.send_reply(__tmp0, __tmp2.spam(__tmp3))

        elif command == 'open':
            __tmp3.send_reply(__tmp0, __tmp2.restore(__tmp3))

        elif command.startswith(__tmp2.COMMENT_PREFIX):
            kwargs = {
                'author_id': "alt:email:" + __tmp0['sender_email'],
                'body': command[len(__tmp2.COMMENT_PREFIX):]
            }
            __tmp3.send_reply(__tmp0, __tmp2.comment(__tmp3, **kwargs))
        else:
            __tmp3.send_reply(__tmp0, "Unknown command. Use `help` for instructions.")

handler_class = FrontHandler

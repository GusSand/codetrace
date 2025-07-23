from typing import TypeAlias
__typ0 : TypeAlias = "str"
import requests
import re
from typing import Any, Dict, Optional

class __typ1(object):
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

    def __tmp5(__tmp1) :
        return '''
            Front Bot uses the Front REST API to interact with Front. In order to use
            Front Bot, `front.conf` must be set up. See `doc.md` for more details.
            '''

    def __tmp4(__tmp1, __tmp3: Any) -> None:
        config = __tmp3.get_config_info('front')
        api_key = config.get('api_key')
        if not api_key:
            raise KeyError("No API key specified.")

        __tmp1.auth = "Bearer " + api_key

    def help(__tmp1, __tmp3: Any) -> __typ0:
        response = ""
        for command, description in __tmp1.COMMANDS:
            response += "`{}` {}\n".format(command, description)

        return response

    def archive(__tmp1, __tmp3: Any) -> __typ0:
        response = requests.patch(__tmp1.FRONT_API.format(__tmp1.conversation_id),
                                  headers={"Authorization": __tmp1.auth},
                                  json={"status": "archived"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was archived."

    def delete(__tmp1, __tmp3: Any) -> __typ0:
        response = requests.patch(__tmp1.FRONT_API.format(__tmp1.conversation_id),
                                  headers={"Authorization": __tmp1.auth},
                                  json={"status": "deleted"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was deleted."

    def spam(__tmp1, __tmp3) -> __typ0:
        response = requests.patch(__tmp1.FRONT_API.format(__tmp1.conversation_id),
                                  headers={"Authorization": __tmp1.auth},
                                  json={"status": "spam"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was marked as spam."

    def restore(__tmp1, __tmp3: <FILL>) -> __typ0:
        response = requests.patch(__tmp1.FRONT_API.format(__tmp1.conversation_id),
                                  headers={"Authorization": __tmp1.auth},
                                  json={"status": "open"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was restored."

    def comment(__tmp1, __tmp3: Any, **kwargs: Any) -> __typ0:
        response = requests.post(__tmp1.FRONT_API.format(__tmp1.conversation_id) + "/comments",
                                 headers={"Authorization": __tmp1.auth}, json=kwargs)

        if response.status_code not in (200, 201):
            return "Something went wrong."

        return "Comment was sent."

    def __tmp2(__tmp1, __tmp0, __tmp3) -> None:
        command = __tmp0['content']

        result = re.search(__tmp1.CNV_ID_REGEXP, __tmp0['subject'])
        if not result:
            __tmp3.send_reply(__tmp0, "No coversation ID found. Please make "
                                            "sure that the name of the topic "
                                            "contains a valid coversation ID.")
            return None

        __tmp1.conversation_id = result.group()

        if command == 'help':
            __tmp3.send_reply(__tmp0, __tmp1.help(__tmp3))

        elif command == 'archive':
            __tmp3.send_reply(__tmp0, __tmp1.archive(__tmp3))

        elif command == 'delete':
            __tmp3.send_reply(__tmp0, __tmp1.delete(__tmp3))

        elif command == 'spam':
            __tmp3.send_reply(__tmp0, __tmp1.spam(__tmp3))

        elif command == 'open':
            __tmp3.send_reply(__tmp0, __tmp1.restore(__tmp3))

        elif command.startswith(__tmp1.COMMENT_PREFIX):
            kwargs = {
                'author_id': "alt:email:" + __tmp0['sender_email'],
                'body': command[len(__tmp1.COMMENT_PREFIX):]
            }
            __tmp3.send_reply(__tmp0, __tmp1.comment(__tmp3, **kwargs))
        else:
            __tmp3.send_reply(__tmp0, "Unknown command. Use `help` for instructions.")

handler_class = __typ1

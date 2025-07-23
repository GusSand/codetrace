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

    def usage(__tmp0) -> __typ0:
        return '''
            Front Bot uses the Front REST API to interact with Front. In order to use
            Front Bot, `front.conf` must be set up. See `doc.md` for more details.
            '''

    def initialize(__tmp0, __tmp1) -> None:
        config = __tmp1.get_config_info('front')
        api_key = config.get('api_key')
        if not api_key:
            raise KeyError("No API key specified.")

        __tmp0.auth = "Bearer " + api_key

    def help(__tmp0, __tmp1: Any) :
        response = ""
        for command, description in __tmp0.COMMANDS:
            response += "`{}` {}\n".format(command, description)

        return response

    def archive(__tmp0, __tmp1: Any) :
        response = requests.patch(__tmp0.FRONT_API.format(__tmp0.conversation_id),
                                  headers={"Authorization": __tmp0.auth},
                                  json={"status": "archived"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was archived."

    def delete(__tmp0, __tmp1) :
        response = requests.patch(__tmp0.FRONT_API.format(__tmp0.conversation_id),
                                  headers={"Authorization": __tmp0.auth},
                                  json={"status": "deleted"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was deleted."

    def spam(__tmp0, __tmp1) :
        response = requests.patch(__tmp0.FRONT_API.format(__tmp0.conversation_id),
                                  headers={"Authorization": __tmp0.auth},
                                  json={"status": "spam"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was marked as spam."

    def restore(__tmp0, __tmp1) :
        response = requests.patch(__tmp0.FRONT_API.format(__tmp0.conversation_id),
                                  headers={"Authorization": __tmp0.auth},
                                  json={"status": "open"})

        if response.status_code not in (200, 204):
            return "Something went wrong."

        return "Conversation was restored."

    def comment(__tmp0, __tmp1: Any, **kwargs: <FILL>) -> __typ0:
        response = requests.post(__tmp0.FRONT_API.format(__tmp0.conversation_id) + "/comments",
                                 headers={"Authorization": __tmp0.auth}, json=kwargs)

        if response.status_code not in (200, 201):
            return "Something went wrong."

        return "Comment was sent."

    def __tmp2(__tmp0, message, __tmp1) :
        command = message['content']

        result = re.search(__tmp0.CNV_ID_REGEXP, message['subject'])
        if not result:
            __tmp1.send_reply(message, "No coversation ID found. Please make "
                                            "sure that the name of the topic "
                                            "contains a valid coversation ID.")
            return None

        __tmp0.conversation_id = result.group()

        if command == 'help':
            __tmp1.send_reply(message, __tmp0.help(__tmp1))

        elif command == 'archive':
            __tmp1.send_reply(message, __tmp0.archive(__tmp1))

        elif command == 'delete':
            __tmp1.send_reply(message, __tmp0.delete(__tmp1))

        elif command == 'spam':
            __tmp1.send_reply(message, __tmp0.spam(__tmp1))

        elif command == 'open':
            __tmp1.send_reply(message, __tmp0.restore(__tmp1))

        elif command.startswith(__tmp0.COMMENT_PREFIX):
            kwargs = {
                'author_id': "alt:email:" + message['sender_email'],
                'body': command[len(__tmp0.COMMENT_PREFIX):]
            }
            __tmp1.send_reply(message, __tmp0.comment(__tmp1, **kwargs))
        else:
            __tmp1.send_reply(message, "Unknown command. Use `help` for instructions.")

handler_class = FrontHandler

from typing import TypeAlias
__typ0 : TypeAlias = "str"
from typing import Any, Dict

import os
from pathlib import Path

class FileUploaderHandler(object):
    def usage(__tmp0) :
        return (
            'This interactive bot is used to upload files (such as images) to the Zulip server:'
            '\n- @uploader <local_file_path> : Upload a file, where <local_file_path> is the path to the file'
            '\n- @uploader help : Display help message'
        )

    def __tmp2(__tmp0, message, __tmp1: <FILL>) :
        HELP_STR = (
            'Use this bot with any of the following commands:'
            '\n* `@uploader <local_file_path>` : Upload a file, where `<local_file_path>` is the path to the file'
            '\n* `@uploader help` : Display help message'
        )

        content = message['content'].strip()
        if content == 'help':
            __tmp1.send_reply(message, HELP_STR)
            return

        path = Path(os.path.expanduser(content))
        if not path.is_file():
            __tmp1.send_reply(message, 'File `{}` not found'.format(content))
            return

        path = path.resolve()
        upload = __tmp1.upload_file_from_path(__typ0(path))
        if upload['result'] != 'success':
            msg = upload['msg']
            __tmp1.send_reply(message, 'Failed to upload `{}` file: {}'.format(path, msg))
            return

        uploaded_file_reply = '[{}]({})'.format(path.name, upload['uri'])
        __tmp1.send_reply(message, uploaded_file_reply)

handler_class = FileUploaderHandler

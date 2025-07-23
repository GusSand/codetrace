from typing import TypeAlias
__typ1 : TypeAlias = "int"
import logging
import shutil
import os

from zerver.data_import.import_util import (
    build_attachment,
    create_converted_data_files,
)

from typing import Any, Dict, List, Optional

class __typ0:
    def __init__(__tmp0) -> None:
        __tmp0.info_dict = dict()  # type: Dict[str, Dict[str, Any]]

    def handle_message_data(__tmp0,
                            realm_id,
                            message_id: __typ1,
                            sender_id,
                            attachment,
                            files_dir: <FILL>) :
        if not attachment:
            return None

        name = attachment['name']

        if 'path' not in attachment:
            logging.info('Skipping HipChat attachment with missing path data: ' + name)
            return None

        size = attachment['size']
        path = attachment['path']

        local_fn = os.path.join(files_dir, path)

        target_path = os.path.join(
            str(realm_id),
            'HipChatImportAttachment',
            path
        )

        if target_path in __tmp0.info_dict:
            logging.info("file used multiple times: " + path)
            info = __tmp0.info_dict[target_path]
            info['message_ids'].add(message_id)
            return info['content']

        # HipChat provides size info, but it's not
        # completely trustworthy, so we we just
        # ask the OS for file details.
        size = os.path.getsize(local_fn)
        mtime = os.path.getmtime(local_fn)

        content = '[{name}](/user_uploads/{path})'.format(
            name=name,
            path=target_path,
        )

        info = dict(
            message_ids={message_id},
            sender_id=sender_id,
            local_fn=local_fn,
            target_path=target_path,
            name=name,
            size=size,
            mtime=mtime,
            content=content,
        )
        __tmp0.info_dict[target_path] = info

        return content

    def write_info(__tmp0, output_dir, realm_id) :
        attachments = []  # type: List[Dict[str, Any]]
        uploads_records = []  # type: List[Dict[str, Any]]

        def add_attachment(info) -> None:
            build_attachment(
                realm_id=realm_id,
                message_ids=info['message_ids'],
                user_id=info['sender_id'],
                fileinfo=dict(
                    created=info['mtime'],  # minor lie
                    size=info['size'],
                    name=info['name'],
                ),
                s3_path=info['target_path'],
                zerver_attachment=attachments,
            )

        def add_upload(info) -> None:
            target_path = info['target_path']
            upload_rec = dict(
                size=info['size'],
                user_profile_id=info['sender_id'],
                realm_id=realm_id,
                s3_path=target_path,
                path=target_path,
                content_type=None,
            )
            uploads_records.append(upload_rec)

        def make_full_target_path(info) -> str:
            target_path = info['target_path']
            full_target_path = os.path.join(
                output_dir,
                'uploads',
                target_path,
            )
            full_target_path = os.path.abspath(full_target_path)
            os.makedirs(os.path.dirname(full_target_path), exist_ok=True)
            return full_target_path

        def copy_file(info: Dict[str, Any]) :
            source_path = info['local_fn']
            target_path = make_full_target_path(info)
            shutil.copyfile(source_path, target_path)

        logging.info('Start processing attachment files')

        for info in __tmp0.info_dict.values():
            add_attachment(info)
            add_upload(info)
            copy_file(info)

        uploads_folder = os.path.join(output_dir, 'uploads')
        os.makedirs(os.path.join(uploads_folder, str(realm_id)), exist_ok=True)

        attachment = dict(
            zerver_attachment=attachments
        )

        create_converted_data_files(uploads_records, output_dir, '/uploads/records.json')
        create_converted_data_files(attachment, output_dir, '/attachment.json')

        logging.info('Done processing attachment files')

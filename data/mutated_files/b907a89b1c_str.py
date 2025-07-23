from typing import TypeAlias
__typ0 : TypeAlias = "DatabaseSchemaEditor"
__typ1 : TypeAlias = "StateApps"
# -*- coding: utf-8 -*-

import os
import re

from django.db import migrations, models
from django.db.backends.postgresql_psycopg2.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps

attachment_url_re = re.compile(r'[/\-]user[\-_]uploads[/\.-].*?(?=[ )]|\Z)')

def __tmp4(__tmp2: <FILL>) -> str:
    path_id_raw = re.sub(r'[/\-]user[\-_]uploads[/\.-]', '', __tmp2)
    # Remove any extra '.' after file extension. These are probably added by the user
    return re.sub('[.]+$', '', path_id_raw, re.M)

def __tmp3(__tmp1,
                                 __tmp0: __typ0) -> None:
    STREAM = 2
    Message = __tmp1.get_model('zerver', 'Message')
    Attachment = __tmp1.get_model('zerver', 'Attachment')
    Stream = __tmp1.get_model('zerver', 'Stream')
    for message in Message.objects.filter(has_attachment=True, attachment=None):
        attachment_url_list = attachment_url_re.findall(message.content)
        for url in attachment_url_list:
            path_id = __tmp4(url)
            user_profile = message.sender
            is_message_realm_public = False
            if message.recipient.type == STREAM:
                stream = Stream.objects.get(id=message.recipient.type_id)
                is_message_realm_public = not stream.invite_only and stream.realm.domain != "mit.edu"

            if path_id is not None:
                attachment = Attachment.objects.create(
                    file_name=os.path.basename(path_id), path_id=path_id, owner=user_profile,
                    realm=user_profile.realm, is_realm_public=is_message_realm_public)
                attachment.messages.add(message)


class Migration(migrations.Migration):

    dependencies = [
        ('zerver', '0040_realm_authentication_methods'),
    ]

    operations = [
        # The TextField change was originally in the next migration,
        # but because it fixes a problem that causes the RunPython
        # part of this migration to crash, we've copied it here.
        migrations.AlterField(
            model_name='attachment',
            name='file_name',
            field=models.TextField(db_index=True),
        ),
        migrations.RunPython(__tmp3)
    ]

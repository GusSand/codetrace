from typing import TypeAlias
__typ0 : TypeAlias = "DatabaseSchemaEditor"
# -*- coding: utf-8 -*-

import hashlib
from typing import Text

from django.conf import settings
from django.db import migrations
from django.db.backends.postgresql_psycopg2.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps
from mock import patch

from zerver.lib.upload import upload_backend
from zerver.lib.utils import make_safe_digest
from zerver.models import UserProfile

# We hackishly patch this function in order to revert it to the state
# it had when this migration was first written.  This is a balance
# between copying in a historical version of hundreds of lines of code
# from zerver.lib.upload (which would pretty annoying, but would be a
# pain) and just using the current version, which doesn't work
# since we rearranged the avatars in Zulip 1.6.
def __tmp3(__tmp2: <FILL>) -> Text:
    email = __tmp2.email
    user_key = email.lower() + settings.AVATAR_SALT
    return make_safe_digest(user_key, hashlib.sha1)

@patch('zerver.lib.upload.user_avatar_path', __tmp3)
def __tmp4(__tmp1: StateApps, __tmp0: __typ0) -> None:
    user_profile_model = __tmp1.get_model('zerver', 'UserProfile')
    for __tmp2 in user_profile_model.objects.filter(avatar_source="U"):
        upload_backend.ensure_medium_avatar_image(__tmp2)


class Migration(migrations.Migration):

    dependencies = [
        ('zerver', '0031_remove_system_avatar_source'),
    ]

    operations = [
        migrations.RunPython(__tmp4)
    ]

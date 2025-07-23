from typing import TypeAlias
__typ0 : TypeAlias = "StateApps"
__typ4 : TypeAlias = "DatabaseSchemaEditor"
# -*- coding: utf-8 -*-
import os
import shutil
import tempfile

from boto.s3.connection import S3Connection
from django.conf import settings
from django.db import migrations, models
from django.db.backends.postgresql_psycopg2.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps

class __typ2:
    def __init__(__tmp2) :
        __tmp2.old_orig_image_path_template = "{realm_id}/emoji/{emoji_file_name}.original"
        __tmp2.old_path_template = "{realm_id}/emoji/{emoji_file_name}"
        __tmp2.new_orig_image_path_template = "{realm_id}/emoji/images/{emoji_file_name}.original"
        __tmp2.new_path_template = "{realm_id}/emoji/images/{emoji_file_name}"

    def copy_files(__tmp2, src_path: str, __tmp7: str) :
        raise NotImplementedError()

    def ensure_emoji_images(__tmp2, realm_id, __tmp0: str, __tmp12: str) :
        # Copy original image file.
        old_file_path = __tmp2.old_orig_image_path_template.format(realm_id=realm_id,
                                                                 __tmp8=__tmp0)
        new_file_path = __tmp2.new_orig_image_path_template.format(realm_id=realm_id,
                                                                 __tmp8=__tmp12)
        __tmp2.copy_files(old_file_path, new_file_path)

        # Copy resized image file.
        old_file_path = __tmp2.old_path_template.format(realm_id=realm_id,
                                                      __tmp8=__tmp0)
        new_file_path = __tmp2.new_path_template.format(realm_id=realm_id,
                                                      __tmp8=__tmp12)
        __tmp2.copy_files(old_file_path, new_file_path)

class __typ1(__typ2):
    def __init__(__tmp2) :
        super().__init__()

    @staticmethod
    def mkdirs(path: <FILL>) :
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def copy_files(__tmp2, src_path, __tmp7) :
        src_path = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', src_path)
        __tmp2.mkdirs(src_path)
        __tmp7 = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', __tmp7)
        __tmp2.mkdirs(__tmp7)
        shutil.copyfile(src_path, __tmp7)

class __typ3(__typ2):
    def __init__(__tmp2) -> None:
        super().__init__()
        conn = S3Connection(settings.S3_KEY, settings.S3_SECRET_KEY)
        __tmp2.bucket_name = settings.S3_AVATAR_BUCKET
        __tmp2.bucket = conn.get_bucket(__tmp2.bucket_name, validate=False)

    def copy_files(__tmp2, __tmp5: str, __tmp6) :
        __tmp2.bucket.copy_key(__tmp6, __tmp2.bucket_name, __tmp5)

def __tmp11() -> __typ2:
    if settings.LOCAL_UPLOADS_DIR is None:
        return __typ3()
    return __typ1()

def __tmp9(__tmp8, __tmp10) -> str:
    _, image_ext = os.path.splitext(__tmp8)
    return ''.join((__tmp10, image_ext))

def __tmp4(__tmp3, __tmp1) :
    RealmEmoji = __tmp3.get_model('zerver', 'RealmEmoji')
    uploader = __tmp11()
    for realm_emoji in RealmEmoji.objects.all():
        old_file_name = realm_emoji.file_name
        new_file_name = __tmp9(old_file_name, str(realm_emoji.id))
        uploader.ensure_emoji_images(realm_emoji.realm_id, old_file_name, new_file_name)
        realm_emoji.file_name = new_file_name
        realm_emoji.save(update_fields=['file_name'])

def __tmp13(__tmp3: __typ0, __tmp1) :
    # Ensures that migration can be re-run in case of a failure.
    RealmEmoji = __tmp3.get_model('zerver', 'RealmEmoji')
    for realm_emoji in RealmEmoji.objects.all():
        corrupt_file_name = realm_emoji.file_name
        correct_file_name = __tmp9(corrupt_file_name, realm_emoji.name)
        realm_emoji.file_name = correct_file_name
        realm_emoji.save(update_fields=['file_name'])

class Migration(migrations.Migration):

    dependencies = [
        ('zerver', '0148_max_invites_forget_default'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='realmemoji',
            unique_together=set([]),
        ),
        migrations.AlterField(
            model_name='realmemoji',
            name='file_name',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.RunPython(
            __tmp4,
            reverse_code=__tmp13),
    ]

from typing import TypeAlias
__typ1 : TypeAlias = "StateApps"
__typ4 : TypeAlias = "DatabaseSchemaEditor"
__typ0 : TypeAlias = "int"
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
    def __init__(__tmp1) -> None:
        __tmp1.old_orig_image_path_template = "{realm_id}/emoji/{emoji_file_name}.original"
        __tmp1.old_path_template = "{realm_id}/emoji/{emoji_file_name}"
        __tmp1.new_orig_image_path_template = "{realm_id}/emoji/images/{emoji_file_name}.original"
        __tmp1.new_path_template = "{realm_id}/emoji/images/{emoji_file_name}"

    def copy_files(__tmp1, __tmp0: str, dst_path) -> None:
        raise NotImplementedError()

    def ensure_emoji_images(__tmp1, realm_id, old_filename: str, new_filename) -> None:
        # Copy original image file.
        old_file_path = __tmp1.old_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=old_filename)
        new_file_path = __tmp1.new_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=new_filename)
        __tmp1.copy_files(old_file_path, new_file_path)

        # Copy resized image file.
        old_file_path = __tmp1.old_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=old_filename)
        new_file_path = __tmp1.new_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=new_filename)
        __tmp1.copy_files(old_file_path, new_file_path)

class LocalUploader(__typ2):
    def __init__(__tmp1) -> None:
        super().__init__()

    @staticmethod
    def mkdirs(path: str) -> None:
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def copy_files(__tmp1, __tmp0: <FILL>, dst_path: str) -> None:
        __tmp0 = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', __tmp0)
        __tmp1.mkdirs(__tmp0)
        dst_path = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', dst_path)
        __tmp1.mkdirs(dst_path)
        shutil.copyfile(__tmp0, dst_path)

class __typ3(__typ2):
    def __init__(__tmp1) :
        super().__init__()
        conn = S3Connection(settings.S3_KEY, settings.S3_SECRET_KEY)
        __tmp1.bucket_name = settings.S3_AVATAR_BUCKET
        __tmp1.bucket = conn.get_bucket(__tmp1.bucket_name, validate=False)

    def copy_files(__tmp1, src_key: str, dst_key: str) -> None:
        __tmp1.bucket.copy_key(dst_key, __tmp1.bucket_name, src_key)

def get_uploader() :
    if settings.LOCAL_UPLOADS_DIR is None:
        return __typ3()
    return LocalUploader()

def get_emoji_file_name(emoji_file_name: str, new_name: str) -> str:
    _, image_ext = os.path.splitext(emoji_file_name)
    return ''.join((new_name, image_ext))

def __tmp3(__tmp2: __typ1, schema_editor) -> None:
    RealmEmoji = __tmp2.get_model('zerver', 'RealmEmoji')
    uploader = get_uploader()
    for realm_emoji in RealmEmoji.objects.all():
        old_file_name = realm_emoji.file_name
        new_file_name = get_emoji_file_name(old_file_name, str(realm_emoji.id))
        uploader.ensure_emoji_images(realm_emoji.realm_id, old_file_name, new_file_name)
        realm_emoji.file_name = new_file_name
        realm_emoji.save(update_fields=['file_name'])

def reversal(__tmp2, schema_editor: __typ4) :
    # Ensures that migration can be re-run in case of a failure.
    RealmEmoji = __tmp2.get_model('zerver', 'RealmEmoji')
    for realm_emoji in RealmEmoji.objects.all():
        corrupt_file_name = realm_emoji.file_name
        correct_file_name = get_emoji_file_name(corrupt_file_name, realm_emoji.name)
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
            __tmp3,
            reverse_code=reversal),
    ]

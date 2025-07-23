from typing import TypeAlias
__typ1 : TypeAlias = "StateApps"
__typ5 : TypeAlias = "DatabaseSchemaEditor"
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

class __typ3:
    def __init__(__tmp1) :
        __tmp1.old_orig_image_path_template = "{realm_id}/emoji/{emoji_file_name}.original"
        __tmp1.old_path_template = "{realm_id}/emoji/{emoji_file_name}"
        __tmp1.new_orig_image_path_template = "{realm_id}/emoji/images/{emoji_file_name}.original"
        __tmp1.new_path_template = "{realm_id}/emoji/images/{emoji_file_name}"

    def copy_files(__tmp1, src_path, __tmp2: str) :
        raise NotImplementedError()

    def ensure_emoji_images(__tmp1, realm_id, __tmp0: str, new_filename) :
        # Copy original image file.
        old_file_path = __tmp1.old_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=__tmp0)
        new_file_path = __tmp1.new_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=new_filename)
        __tmp1.copy_files(old_file_path, new_file_path)

        # Copy resized image file.
        old_file_path = __tmp1.old_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=__tmp0)
        new_file_path = __tmp1.new_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=new_filename)
        __tmp1.copy_files(old_file_path, new_file_path)

class __typ2(__typ3):
    def __init__(__tmp1) -> None:
        super().__init__()

    @staticmethod
    def mkdirs(path: str) -> None:
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def copy_files(__tmp1, src_path: str, __tmp2) :
        src_path = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', src_path)
        __tmp1.mkdirs(src_path)
        __tmp2 = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', __tmp2)
        __tmp1.mkdirs(__tmp2)
        shutil.copyfile(src_path, __tmp2)

class __typ4(__typ3):
    def __init__(__tmp1) -> None:
        super().__init__()
        conn = S3Connection(settings.S3_KEY, settings.S3_SECRET_KEY)
        __tmp1.bucket_name = settings.S3_AVATAR_BUCKET
        __tmp1.bucket = conn.get_bucket(__tmp1.bucket_name, validate=False)

    def copy_files(__tmp1, src_key: str, dst_key: str) -> None:
        __tmp1.bucket.copy_key(dst_key, __tmp1.bucket_name, src_key)

def __tmp4() :
    if settings.LOCAL_UPLOADS_DIR is None:
        return __typ4()
    return __typ2()

def __tmp3(emoji_file_name: str, new_name: <FILL>) -> str:
    _, image_ext = os.path.splitext(emoji_file_name)
    return ''.join((new_name, image_ext))

def migrate_realm_emoji_image_files(apps: __typ1, schema_editor: __typ5) -> None:
    RealmEmoji = apps.get_model('zerver', 'RealmEmoji')
    uploader = __tmp4()
    for realm_emoji in RealmEmoji.objects.all():
        old_file_name = realm_emoji.file_name
        new_file_name = __tmp3(old_file_name, str(realm_emoji.id))
        uploader.ensure_emoji_images(realm_emoji.realm_id, old_file_name, new_file_name)
        realm_emoji.file_name = new_file_name
        realm_emoji.save(update_fields=['file_name'])

def __tmp5(apps, schema_editor: __typ5) :
    # Ensures that migration can be re-run in case of a failure.
    RealmEmoji = apps.get_model('zerver', 'RealmEmoji')
    for realm_emoji in RealmEmoji.objects.all():
        corrupt_file_name = realm_emoji.file_name
        correct_file_name = __tmp3(corrupt_file_name, realm_emoji.name)
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
            migrate_realm_emoji_image_files,
            reverse_code=__tmp5),
    ]

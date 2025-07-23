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
    def __init__(__tmp1) -> None:
        __tmp1.old_orig_image_path_template = "{realm_id}/emoji/{emoji_file_name}.original"
        __tmp1.old_path_template = "{realm_id}/emoji/{emoji_file_name}"
        __tmp1.new_orig_image_path_template = "{realm_id}/emoji/images/{emoji_file_name}.original"
        __tmp1.new_path_template = "{realm_id}/emoji/images/{emoji_file_name}"

    def copy_files(__tmp1, __tmp5: <FILL>, dst_path) -> None:
        raise NotImplementedError()

    def ensure_emoji_images(__tmp1, realm_id, old_filename, __tmp7) :
        # Copy original image file.
        old_file_path = __tmp1.old_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=old_filename)
        new_file_path = __tmp1.new_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=__tmp7)
        __tmp1.copy_files(old_file_path, new_file_path)

        # Copy resized image file.
        old_file_path = __tmp1.old_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=old_filename)
        new_file_path = __tmp1.new_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=__tmp7)
        __tmp1.copy_files(old_file_path, new_file_path)

class __typ2(__typ3):
    def __init__(__tmp1) :
        super().__init__()

    @staticmethod
    def mkdirs(path: str) :
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def copy_files(__tmp1, __tmp5, dst_path: str) -> None:
        __tmp5 = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', __tmp5)
        __tmp1.mkdirs(__tmp5)
        dst_path = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', dst_path)
        __tmp1.mkdirs(dst_path)
        shutil.copyfile(__tmp5, dst_path)

class __typ4(__typ3):
    def __init__(__tmp1) -> None:
        super().__init__()
        conn = S3Connection(settings.S3_KEY, settings.S3_SECRET_KEY)
        __tmp1.bucket_name = settings.S3_AVATAR_BUCKET
        __tmp1.bucket = conn.get_bucket(__tmp1.bucket_name, validate=False)

    def copy_files(__tmp1, __tmp3, __tmp4: str) -> None:
        __tmp1.bucket.copy_key(__tmp4, __tmp1.bucket_name, __tmp3)

def __tmp6() :
    if settings.LOCAL_UPLOADS_DIR is None:
        return __typ4()
    return __typ2()

def get_emoji_file_name(emoji_file_name, new_name: str) :
    _, image_ext = os.path.splitext(emoji_file_name)
    return ''.join((new_name, image_ext))

def __tmp2(apps: __typ1, __tmp0: __typ5) :
    RealmEmoji = apps.get_model('zerver', 'RealmEmoji')
    uploader = __tmp6()
    for realm_emoji in RealmEmoji.objects.all():
        old_file_name = realm_emoji.file_name
        new_file_name = get_emoji_file_name(old_file_name, str(realm_emoji.id))
        uploader.ensure_emoji_images(realm_emoji.realm_id, old_file_name, new_file_name)
        realm_emoji.file_name = new_file_name
        realm_emoji.save(update_fields=['file_name'])

def reversal(apps: __typ1, __tmp0) :
    # Ensures that migration can be re-run in case of a failure.
    RealmEmoji = apps.get_model('zerver', 'RealmEmoji')
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
            __tmp2,
            reverse_code=reversal),
    ]

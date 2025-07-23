from typing import TypeAlias
__typ0 : TypeAlias = "StateApps"
# -*- coding: utf-8 -*-
import os
import shutil
import tempfile

from boto.s3.connection import S3Connection
from django.conf import settings
from django.db import migrations, models
from django.db.backends.postgresql_psycopg2.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps

class Uploader:
    def __init__(__tmp2) :
        __tmp2.old_orig_image_path_template = "{realm_id}/emoji/{emoji_file_name}.original"
        __tmp2.old_path_template = "{realm_id}/emoji/{emoji_file_name}"
        __tmp2.new_orig_image_path_template = "{realm_id}/emoji/images/{emoji_file_name}.original"
        __tmp2.new_path_template = "{realm_id}/emoji/images/{emoji_file_name}"

    def copy_files(__tmp2, __tmp8, __tmp5) :
        raise NotImplementedError()

    def ensure_emoji_images(__tmp2, realm_id, __tmp1, __tmp9) :
        # Copy original image file.
        old_file_path = __tmp2.old_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=__tmp1)
        new_file_path = __tmp2.new_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=__tmp9)
        __tmp2.copy_files(old_file_path, new_file_path)

        # Copy resized image file.
        old_file_path = __tmp2.old_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=__tmp1)
        new_file_path = __tmp2.new_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=__tmp9)
        __tmp2.copy_files(old_file_path, new_file_path)

class __typ1(Uploader):
    def __init__(__tmp2) :
        super().__init__()

    @staticmethod
    def mkdirs(path) :
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def copy_files(__tmp2, __tmp8, __tmp5) :
        __tmp8 = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', __tmp8)
        __tmp2.mkdirs(__tmp8)
        __tmp5 = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', __tmp5)
        __tmp2.mkdirs(__tmp5)
        shutil.copyfile(__tmp8, __tmp5)

class S3Uploader(Uploader):
    def __init__(__tmp2) :
        super().__init__()
        conn = S3Connection(settings.S3_KEY, settings.S3_SECRET_KEY)
        __tmp2.bucket_name = settings.S3_AVATAR_BUCKET
        __tmp2.bucket = conn.get_bucket(__tmp2.bucket_name, validate=False)

    def copy_files(__tmp2, src_key, __tmp4) :
        __tmp2.bucket.copy_key(__tmp4, __tmp2.bucket_name, src_key)

def get_uploader() :
    if settings.LOCAL_UPLOADS_DIR is None:
        return S3Uploader()
    return __typ1()

def __tmp6(emoji_file_name: <FILL>, __tmp7) :
    _, image_ext = os.path.splitext(emoji_file_name)
    return ''.join((__tmp7, image_ext))

def __tmp3(apps: __typ0, __tmp0) :
    RealmEmoji = apps.get_model('zerver', 'RealmEmoji')
    uploader = get_uploader()
    for realm_emoji in RealmEmoji.objects.all():
        old_file_name = realm_emoji.file_name
        new_file_name = __tmp6(old_file_name, str(realm_emoji.id))
        uploader.ensure_emoji_images(realm_emoji.realm_id, old_file_name, new_file_name)
        realm_emoji.file_name = new_file_name
        realm_emoji.save(update_fields=['file_name'])

def reversal(apps: __typ0, __tmp0) :
    # Ensures that migration can be re-run in case of a failure.
    RealmEmoji = apps.get_model('zerver', 'RealmEmoji')
    for realm_emoji in RealmEmoji.objects.all():
        corrupt_file_name = realm_emoji.file_name
        correct_file_name = __tmp6(corrupt_file_name, realm_emoji.name)
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

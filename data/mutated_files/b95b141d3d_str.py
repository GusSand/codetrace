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
    def __init__(self) :
        self.old_orig_image_path_template = "{realm_id}/emoji/{emoji_file_name}.original"
        self.old_path_template = "{realm_id}/emoji/{emoji_file_name}"
        self.new_orig_image_path_template = "{realm_id}/emoji/images/{emoji_file_name}.original"
        self.new_path_template = "{realm_id}/emoji/images/{emoji_file_name}"

    def copy_files(self, src_path: str, dst_path: str) :
        raise NotImplementedError()

    def ensure_emoji_images(self, realm_id, __tmp0: str, new_filename: <FILL>) :
        # Copy original image file.
        old_file_path = self.old_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=__tmp0)
        new_file_path = self.new_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=new_filename)
        self.copy_files(old_file_path, new_file_path)

        # Copy resized image file.
        old_file_path = self.old_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=__tmp0)
        new_file_path = self.new_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=new_filename)
        self.copy_files(old_file_path, new_file_path)

class LocalUploader(__typ2):
    def __init__(self) :
        super().__init__()

    @staticmethod
    def mkdirs(path) :
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def copy_files(self, src_path: str, dst_path: str) :
        src_path = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', src_path)
        self.mkdirs(src_path)
        dst_path = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', dst_path)
        self.mkdirs(dst_path)
        shutil.copyfile(src_path, dst_path)

class __typ3(__typ2):
    def __init__(self) :
        super().__init__()
        conn = S3Connection(settings.S3_KEY, settings.S3_SECRET_KEY)
        self.bucket_name = settings.S3_AVATAR_BUCKET
        self.bucket = conn.get_bucket(self.bucket_name, validate=False)

    def copy_files(self, src_key, dst_key) :
        self.bucket.copy_key(dst_key, self.bucket_name, src_key)

def get_uploader() -> __typ2:
    if settings.LOCAL_UPLOADS_DIR is None:
        return __typ3()
    return LocalUploader()

def get_emoji_file_name(emoji_file_name, new_name: str) :
    _, image_ext = os.path.splitext(emoji_file_name)
    return ''.join((new_name, image_ext))

def migrate_realm_emoji_image_files(apps, schema_editor) :
    RealmEmoji = apps.get_model('zerver', 'RealmEmoji')
    uploader = get_uploader()
    for realm_emoji in RealmEmoji.objects.all():
        old_file_name = realm_emoji.file_name
        new_file_name = get_emoji_file_name(old_file_name, str(realm_emoji.id))
        uploader.ensure_emoji_images(realm_emoji.realm_id, old_file_name, new_file_name)
        realm_emoji.file_name = new_file_name
        realm_emoji.save(update_fields=['file_name'])

def reversal(apps, schema_editor) :
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
            migrate_realm_emoji_image_files,
            reverse_code=reversal),
    ]

from typing import TypeAlias
__typ0 : TypeAlias = "StateApps"
__typ5 : TypeAlias = "DatabaseSchemaEditor"
__typ1 : TypeAlias = "str"
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
    def __init__(self) -> None:
        self.old_orig_image_path_template = "{realm_id}/emoji/{emoji_file_name}.original"
        self.old_path_template = "{realm_id}/emoji/{emoji_file_name}"
        self.new_orig_image_path_template = "{realm_id}/emoji/images/{emoji_file_name}.original"
        self.new_path_template = "{realm_id}/emoji/images/{emoji_file_name}"

    def copy_files(self, src_path: __typ1, dst_path: __typ1) -> None:
        raise NotImplementedError()

    def ensure_emoji_images(self, realm_id: <FILL>, old_filename: __typ1, new_filename: __typ1) -> None:
        # Copy original image file.
        old_file_path = self.old_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=old_filename)
        new_file_path = self.new_orig_image_path_template.format(realm_id=realm_id,
                                                                 emoji_file_name=new_filename)
        self.copy_files(old_file_path, new_file_path)

        # Copy resized image file.
        old_file_path = self.old_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=old_filename)
        new_file_path = self.new_path_template.format(realm_id=realm_id,
                                                      emoji_file_name=new_filename)
        self.copy_files(old_file_path, new_file_path)

class __typ2(__typ3):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def mkdirs(path: __typ1) -> None:
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def copy_files(self, src_path: __typ1, dst_path: __typ1) -> None:
        src_path = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', src_path)
        self.mkdirs(src_path)
        dst_path = os.path.join(settings.LOCAL_UPLOADS_DIR, 'avatars', dst_path)
        self.mkdirs(dst_path)
        shutil.copyfile(src_path, dst_path)

class __typ4(__typ3):
    def __init__(self) -> None:
        super().__init__()
        conn = S3Connection(settings.S3_KEY, settings.S3_SECRET_KEY)
        self.bucket_name = settings.S3_AVATAR_BUCKET
        self.bucket = conn.get_bucket(self.bucket_name, validate=False)

    def copy_files(self, src_key: __typ1, dst_key) -> None:
        self.bucket.copy_key(dst_key, self.bucket_name, src_key)

def get_uploader() -> __typ3:
    if settings.LOCAL_UPLOADS_DIR is None:
        return __typ4()
    return __typ2()

def get_emoji_file_name(emoji_file_name: __typ1, new_name: __typ1) -> __typ1:
    _, image_ext = os.path.splitext(emoji_file_name)
    return ''.join((new_name, image_ext))

def migrate_realm_emoji_image_files(apps: __typ0, schema_editor: __typ5) -> None:
    RealmEmoji = apps.get_model('zerver', 'RealmEmoji')
    uploader = get_uploader()
    for realm_emoji in RealmEmoji.objects.all():
        old_file_name = realm_emoji.file_name
        new_file_name = get_emoji_file_name(old_file_name, __typ1(realm_emoji.id))
        uploader.ensure_emoji_images(realm_emoji.realm_id, old_file_name, new_file_name)
        realm_emoji.file_name = new_file_name
        realm_emoji.save(update_fields=['file_name'])

def reversal(apps: __typ0, schema_editor) -> None:
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

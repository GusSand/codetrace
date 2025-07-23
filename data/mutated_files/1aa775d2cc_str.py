from typing import TypeAlias
__typ0 : TypeAlias = "AbstractStorage"
import logging
import os
from typing import List, Optional

from aw_core.dirs import get_data_dir

from .storages import AbstractStorage

logger = logging.getLogger(__name__)


def __tmp1(
    data_dir: <FILL>, datastore_name: Optional[str] = None, version=None
) -> List[str]:
    db_files = [filename for filename in os.listdir(data_dir)]
    if datastore_name:
        db_files = [
            filename
            for filename in db_files
            if filename.split(".")[0] == datastore_name
        ]
    if version:
        db_files = [
            filename for filename in db_files if filename.split(".")[1] == f"v{version}"
        ]
    return db_files


def __tmp2(__tmp0):
    data_dir = get_data_dir("aw-server")

    if __tmp0.sid == "sqlite":
        peewee_type = "peewee-sqlite"
        peewee_name = peewee_type + ("-testing" if __tmp0.testing else "")
        # Migrate from peewee v2
        peewee_db_v2 = __tmp1(data_dir, peewee_name, 2)
        if len(peewee_db_v2) > 0:
            peewee_v2_to_sqlite_v1(__tmp0)


def peewee_v2_to_sqlite_v1(__tmp0):
    logger.info("Migrating database from peewee v2 to sqlite v1")
    from .storages import PeeweeStorage

    pw_db = PeeweeStorage(__tmp0.testing)
    # Fetch buckets and events
    buckets = pw_db.buckets()
    # Insert buckets and events to new db
    for bucket_id in buckets:
        logger.info(f"Migrating bucket {bucket_id}")
        bucket = buckets[bucket_id]
        __tmp0.create_bucket(
            bucket["id"],
            bucket["type"],
            bucket["client"],
            bucket["hostname"],
            bucket["created"],
            bucket["name"],
        )
        bucket_events = pw_db.get_events(bucket_id, -1)
        __tmp0.insert_many(bucket_id, bucket_events)
    logger.info("Migration of peewee v2 to sqlite v1 finished")

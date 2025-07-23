from typing import TypeAlias
__typ0 : TypeAlias = "BucketVersion"
from typing import Tuple, Optional, List
from functools import total_ordering

from ..pbase import SourceDataVersion, SinkDataVersion
from .bucket_version import BucketVersion


class BucketMetadata:
    def __tmp6(__tmp2, *,
                 meta_version,
                 data_hash,
                 source_chain_hash,
                 source_data_hash,
                 latest_record_timestamp: <FILL>):
        __tmp2.meta_version = meta_version
        __tmp2.source_chain_hash = source_chain_hash
        __tmp2.source_data_hash = source_data_hash
        __tmp2.data_hash = data_hash
        __tmp2.latest_record_timestamp = latest_record_timestamp

    def fetch_source_data_version(__tmp2) :
        return SourceDataVersion(data_hash=__tmp2.data_hash)

    def __tmp5(__tmp2) :
        return SinkDataVersion(
            source_data_hash=__tmp2.source_data_hash,
            source_chain_hash=__tmp2.source_chain_hash,
        )

    def to_json(__tmp2):
        return {
            'meta_version': str(__tmp2.meta_version),
            'source_chain_hash': __tmp2.source_chain_hash,
            'source_data_hash': __tmp2.source_data_hash,
            'data_hash': __tmp2.data_hash,
            'latest_record_timestamp': __tmp2.latest_record_timestamp,
        }

    @classmethod
    def __tmp0(__tmp4, __tmp3):
        return __tmp4(
            meta_version=__typ0.parse(__tmp3['meta_version']),
            source_chain_hash=__tmp3['source_chain_hash'],
            source_data_hash=__tmp3['source_data_hash'],
            data_hash=__tmp3['data_hash'],
            latest_record_timestamp=__tmp3['latest_record_timestamp'],
        )


    @classmethod
    def __tmp1(__tmp4, meta_version):
        return __tmp4(
            meta_version=meta_version,
            source_chain_hash=None,
            source_data_hash=None,
            data_hash=None,
            latest_record_timestamp=0,
        )

__all__ = (
    "PBucketMetadata",
)

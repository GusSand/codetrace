from typing import TypeAlias
__typ1 : TypeAlias = "BucketMetadata"
__typ0 : TypeAlias = "PRecord"
import json
import numpy as np

from ..bucket_metadata import BucketMetadata
from ..bucket_version import BucketVersion

from ..base_storage import Bucket
from ...pdatastructures import PRecord, PAtom
from typing import Iterator
from contextlib import contextmanager


class __typ2(Bucket):
    META_VERSION = BucketVersion.parse('0.0.1')
    def __init__(__tmp0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        __tmp0._h5file = None

    def load_metadata(__tmp0, __tmp4) -> __typ1:
        with __tmp0._file_context():
            return __tmp0._ensure_metadata()

    def flush_metadata(__tmp0, __tmp4, metadata):
        with __tmp0._file_context():
            __tmp0._h5file.attrs['h5bucket.json'] = json.dumps(metadata.to_json())

    def __tmp3(__tmp0, __tmp4) -> Iterator[str]:
        return __tmp0._h5file.keys()

    def load_precord(__tmp0, __tmp4, id: <FILL>):
        try:
            group = __tmp0._h5file[id]
        except KeyError:
            return None
        active_channel = group.attrs.get('active_channel', 'unknown')
        timestamp = group.attrs.get('timestamp')
        channel_atoms = {}
        for channel_name, dataset in group.items():
            format = dataset.attrs.get('format', 'unknown')
            data = np.array(dataset)
            if data.shape == ():
                data = data.tolist()
            patom = PAtom(value=data, format=format)
            channel_atoms[channel_name] = patom
        return __typ0(
            id=id,
            timestamp=timestamp,
            active_channel=active_channel,
            channel_atoms=channel_atoms,
        )

    def __tmp1(__tmp0, __tmp4, precord: __typ0):
        try:
            group = __tmp0._h5file[precord.id]
        except KeyError:
            group = __tmp0._h5file.create_group(precord.id)
        group.attrs['active_channel'] = precord.active_channel
        group.attrs['timestamp'] = precord.timestamp
        for channel_name, patom in precord.channel_atoms.items():
            try:
                del group[channel_name]
            except KeyError:
                pass
            dataset = group.create_dataset(channel_name, data=patom.value)
            dataset.attrs['format'] = patom.format

    def read_context(__tmp0):
        return __tmp0._file_context()

    def __tmp2(__tmp0):
        return __tmp0._file_context()

    def _ensure_metadata(__tmp0):
        try:
            data_result = __tmp0._h5file.attrs['h5bucket.json']
            return __typ1.from_json(json.loads(data_result))
        except KeyError:
            metadata = __typ1.initial(__tmp0.META_VERSION)
            __tmp0._h5file.attrs['h5bucket.json'] = json.dumps(metadata.to_json())
            return metadata

    @contextmanager
    def _file_context(__tmp0):
        if __tmp0._h5file is None:
            try:
                with __tmp0.storage.with_h5file(__tmp0.scope) as h5file:
                    __tmp0._h5file = h5file
                    __tmp0._ensure_metadata()
                    yield
            finally:
                __tmp0._h5file = None
        else:
            yield

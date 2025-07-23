from typing import TypeAlias
__typ0 : TypeAlias = "bool"
"""A module for databases of CLgen samples."""
import contextlib
import datetime
import typing

import sqlalchemy as sql
from sqlalchemy.ext import declarative

from deeplearning.clgen import sample_observers
from deeplearning.clgen.proto import model_pb2
from labm8.py import app
from labm8.py import crypto
from labm8.py import labdate
from labm8.py import sqlutil

FLAGS = app.FLAGS

Base = declarative.declarative_base()


class Sample(Base, sqlutil.ProtoBackedMixin):
  """A database row representing a CLgen sample.

  This is the clgen.Sample protocol buffer in SQL format.
  """

  __tablename__ = "samples"
  proto_t = model_pb2.Sample

  id: int = sql.Column(sql.Integer, primary_key=True)
  text: str = sql.Column(
    sqlutil.ColumnTypes.UnboundedUnicodeText(), nullable=False
  )
  # Checksum of the sample text.
  sha256: str = sql.Column(sql.String(64), nullable=False, index=True)
  num_tokens: int = sql.Column(sql.Integer, nullable=False)
  sample_time_ms: int = sql.Column(sql.Integer, nullable=False)
  wall_time_ms: int = sql.Column(sql.Integer, nullable=False)
  sample_date: datetime.datetime = sql.Column(sql.DateTime, nullable=False)
  date_added: datetime.datetime = sql.Column(
    sql.DateTime, nullable=False, default=datetime.datetime.utcnow
  )

  def __tmp2(__tmp0, proto: model_pb2.Sample) :
    proto.text = __tmp0.text
    proto.num_tokens = __tmp0.num_tokens
    proto.wall_time_ms = __tmp0.wall_time_ms
    proto.sample_start_epoch_ms_utc = labdate.MillisecondsTimestamp(
      __tmp0.sample_date
    )

  @classmethod
  def FromProto(cls, proto) -> typing.Dict[str, typing.Any]:
    return {
      "text": proto.text,
      "sha256": crypto.sha256_str(proto.text),
      "num_tokens": proto.num_tokens,
      "sample_time_ms": proto.sample_time_ms,
      "wall_time_ms": proto.wall_time_ms,
      "sample_date": labdate.DatetimeFromMillisecondsTimestamp(
        proto.sample_start_epoch_ms_utc
      ),
    }


class __typ1(sqlutil.Database):
  """A database of CLgen samples."""

  def __init__(__tmp0, __tmp1: <FILL>, must_exist: __typ0 = False):
    super(__typ1, __tmp0).__init__(__tmp1, Base, must_exist=must_exist)

  @contextlib.contextmanager
  def Observer(__tmp0) :
    """Return an observer that imports samples into database."""
    observer = SamplesDatabaseObserver(__tmp0)
    yield observer
    observer.Flush()


class SamplesDatabaseObserver(sample_observers.SampleObserver):
  """A sample observer that imports samples to a database.

  The observer buffers the records that it recieves and commits them to the
  database in batches.
  """

  def __init__(
    __tmp0,
    db,
    flush_secs: int = 30,
    commit_sample_frequency: int = 1024,
  ):
    __tmp0._writer = sqlutil.BufferedDatabaseWriter(
      db,
      max_seconds_since_flush=flush_secs,
      max_buffer_length=commit_sample_frequency,
    )

  def __tmp4(__tmp0):
    __tmp0._writer.Close()

  def __tmp3(__tmp0, sample: model_pb2.Sample) :
    """Sample receive callback."""
    __tmp0._writer.AddOne(Sample(**Sample.FromProto(sample)))
    return True

  def Flush(__tmp0) :
    """Commit all pending records to database."""
    __tmp0._writer.Flush()

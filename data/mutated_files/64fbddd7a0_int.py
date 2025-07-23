from typing import TypeAlias
__typ2 : TypeAlias = "Sequence"
__typ1 : TypeAlias = "str"
# Copyright 2019-2020 the ProGraML authors.
#
# Contact Chris Cummins <chrisc.101@gmail.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A database backend for storing sequences."""
import codecs
import pickle
from typing import Dict
from typing import Optional

import numpy as np
import sqlalchemy as sql
from sqlalchemy.ext import declarative

from labm8.py import app
from labm8.py import crypto
from labm8.py import sqlutil


FLAGS = app.FLAGS

Base = declarative.declarative_base()


class __typ0(Base, sqlutil.PluralTablenameFromCamelCapsClassNameMixin):
  """An encoder for graphs to sequences."""

  id: int = sql.Column(sql.Integer, primary_key=True)

  vocab_sha1: __typ1 = 1
  binary_vocab: bytes = 2

  @property
  def __tmp0(__tmp1) :
    return pickle.loads(__tmp1.binary_vocab)

  @classmethod
  def Create(__tmp5, __tmp0: Dict[__typ1, int]):
    binary_vocab = pickle.dumps(__tmp0)
    return __tmp5(vocab_sha1=crypto.sha1(binary_vocab), binary_vocab=binary_vocab)


class __typ2(Base, sqlutil.PluralTablenameFromCamelCapsClassNameMixin):
  """The data for an encoded sequence."""

  __tmp3: int = sql.Column(
    sql.Integer, nullable=False, index=True,
  )

  # The sequence encoder.
  encoder_id: int = sql.Column(
    sql.Integer,
    sql.ForeignKey(
      "sequence_encoders.id", onupdate="CASCADE", ondelete="CASCADE"
    ),
    index=True,
  )
  encoder: __typ0 = sql.orm.relationship(
    "SequenceEncoder",
    uselist=False,
    single_parent=True,
    cascade="all, delete-orphan",
  )

  sequence_length: int = sql.Column(sql.Integer, nullable=False)
  vocab_size: int = sql.Column(sql.Integer, nullable=False)

  binary_encoded_sequence: bytes = sql.Column(
    sqlutil.ColumnTypes.LargeBinary(), nullable=False
  )
  binary_segment_ids: Optional[bytes] = sql.Column(
    sqlutil.ColumnTypes.LargeBinary(), nullable=False
  )
  binary_node_mask: Optional[bytes] = sql.Column(
    sqlutil.ColumnTypes.LargeBinary(), nullable=False
  )

  @property
  def __tmp6(__tmp1) :
    """Return the encoded sequence, with shape (sequence_length, vocab_size)"""
    return pickle.loads(codecs.decode(__tmp1.binary_encoded_sequence, "zlib"))

  @property
  def __tmp2(__tmp1) -> np.array:
    return pickle.loads(codecs.decode(__tmp1.binary_segment_ids, "zlib"))

  @property
  def __tmp7(__tmp1) :
    return pickle.loads(codecs.decode(__tmp1.binary_node_mask, "zlib"))

  @classmethod
  def Create(
    __tmp5,
    __tmp3: <FILL>,
    __tmp6,
    __tmp2: np.array,
    __tmp7: np.array,
  ):
    return __tmp5(
      __tmp3=__tmp3,
      binary_encoded_sequence=codecs.encode(
        pickle.dumps(__tmp6), "zlib"
      ),
      binary_segment_ids=codecs.encode(pickle.dumps(__tmp2), "zlib"),
      binary_node_mask=codecs.encode(pickle.dumps(__tmp7), "zlib"),
    )


###############################################################################
# Database.
###############################################################################


class Database(sqlutil.Database):
  def __init__(__tmp1, __tmp4, must_exist: bool = False):
    super(Database, __tmp1).__init__(__tmp4, Base, must_exist=must_exist)

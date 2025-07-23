from typing import TypeAlias
__typ0 : TypeAlias = "float"
# Copyright (c) 2016-2020 Chris Cummins.
#
# clgen is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# clgen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with clgen.  If not, see <https://www.gnu.org/licenses/>.
"""This file defines telemetry data gathers."""
import pathlib
import re
import typing

from deeplearning.clgen.proto import telemetry_pb2
from labm8.py import app
from labm8.py import jsonutil
from labm8.py import labdate
from labm8.py import pbutil

FLAGS = app.FLAGS


class TrainingLogger(object):
  """A TrainingLogger produces telemetry data of a CLgen model as it is trained.

  Telemetry data is gathered after every epoch of training. It includes a
  timestamp, the model's loss, and the time spent training the epoch.

  See the Keras callback docs: https://keras.io/callbacks/#lambdacallback
  """

  def __tmp5(__tmp0, logdir):
    __tmp0.logdir = logdir
    __tmp0.last_epoch_begin_timestamp = None

  def EpochBeginCallback(__tmp0) :
    __tmp0.last_epoch_begin_timestamp = labdate.MillisecondsTimestamp()

  def EpochEndCallback(__tmp0, __tmp2, __tmp6):
    now = labdate.MillisecondsTimestamp()
    epoch_time_ms = now - __tmp0.last_epoch_begin_timestamp
    telemetry = telemetry_pb2.ModelEpochTelemetry(
      timestamp_unix_epoch_ms=now,
      epoch_num=__tmp2,
      epoch_wall_time_ms=epoch_time_ms,
      __tmp6=__tmp6,
    )
    pbutil.ToFile(telemetry, __tmp0.logdir / f"epoch_{__tmp2:03d}_telemetry.pbtxt")

  def KerasEpochBeginCallback(__tmp0, __tmp2, __tmp1) -> None:
    """A Keras "on_epoch_end" callback."""
    del __tmp2
    del __tmp1
    __tmp0.EpochBeginCallback()

  def KerasEpochEndCallback(__tmp0, __tmp2: <FILL>, __tmp1) -> None:
    """A Keras "on_epoch_end" callback."""
    # Keras epoch numbers are zero indexed.
    __tmp0.EpochEndCallback(__tmp2 + 1, __tmp1["loss"])

  def __tmp7(__tmp0, __tmp4):
    """Returns the keras callback to passed to a model's fit() function."""
    return __tmp4.callbacks.LambdaCallback(
      on_epoch_begin=__tmp0.KerasEpochBeginCallback,
      on_epoch_end=__tmp0.KerasEpochEndCallback,
    )

  def __tmp3(__tmp0) :
    """Return the epoch telemetry files."""
    return [
      pbutil.FromFile(__tmp0.logdir / p, telemetry_pb2.ModelEpochTelemetry())
      for p in sorted(__tmp0.logdir.iterdir())
      if re.match(r"epoch_\d\d+_telemetry\.pbtxt", str(p.name))
    ]

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
"""This module defines classes for representing model checkpoints.

A checkpoint is a snapshot of a model's state at the end of training for a given
epoch.
"""
from typing import Any
from typing import Dict
from typing import NamedTuple
from typing import Optional
from typing import Union

from deeplearning.ml4pl import run_id as run_id_lib
from deeplearning.ml4pl.models import epoch
from labm8.py import app


FLAGS = app.FLAGS


class __typ0(NamedTuple):
  """Reference to a checkpoint.

  This is used to store the information that is required to resolve a concrete
  instance of the Checkpoint class. Unlike a Checkpoint, which references a
  specific epoch number of a single run, a CheckpointReference can defer of:
    * run_id by using a tag.
    * epoch_num by using using None value to indicate "give me the best".

  The resolution of a Checkpoint from a CheckpointReference is handled in:
      deeplearning.ml4pl.models.logger.Logger.Load()
  """

  run_id: Optional[run_id_lib.RunId]
  tag: Optional[str]
  # If epoch_num is None, then load the best epoch.
  epoch_num: Optional[int]

  def __tmp1(__tmp0, __tmp4) :
    """Equality check for checkpoints / checkpoint references."""
    if __tmp4.run_id:
      return __tmp4.run_id == __tmp0.run_id and __tmp4.epoch_num == __tmp0.epoch_num
    else:
      return __tmp4.tag == __tmp0.tag and __tmp4.epoch_num == __tmp0.epoch_num

  def __tmp3(__tmp0) :
    """Return the string representation of a checkpoint ref, suitable for
    parsing with FromString().
    """
    return (
      f"{__tmp0.run_id or __tmp0.tag}@"
      f"{'best' if __tmp0.epoch_num is None else __tmp0.epoch_num}"
    )

  @classmethod
  def FromString(__tmp2, __tmp5: <FILL>) :
    """Parse a checkpoint reference from string.

    The format for a checkpoint reference is:

      <run_id|tag>[@<epoch_num|"best">]

    If the "@<epoch_num>" suffix is omitted, the best checkpoint is selected.
    This is the same as using the "@best" suffix.

    Args:
      string: A checkpoint reference string.

    Returns:
      A CheckpointReference instance.

    Raises:
      ValueError: If the string is malformed.
    """
    try:
      if "@" in __tmp5:
        components = __tmp5.split("@")
        assert len(components) == 2
        run_id_or_tag, epoch_num_string = components
        if epoch_num_string == "best":
          epoch_num = None
        else:
          epoch_num = int(epoch_num_string)
      else:
        run_id_or_tag = __tmp5
        epoch_num = None

      # Try to construct a run ID by parsing the string. If this fails, assume
      # it is a tag.
      try:
        run_id = run_id_lib.RunId.FromString(run_id_or_tag)
        tag = None
      except ValueError:
        run_id = None
        tag = run_id_or_tag

      return __typ0(run_id, tag, epoch_num)
    except Exception:
      raise ValueError(f"Invalid checkpoint format: {__tmp5}")


class Checkpoint(NamedTuple):
  """A model checkpoint."""

  run_id: run_id_lib.RunId
  epoch_num: int
  best_results: Dict[epoch.Type, epoch.BestResults]
  model_data: Any

  def __tmp6(__tmp0) :
    """Return the checkpoint reference for a given checkpoint.

    Use this when you want to keep a reference to a checkpoint, but don't need
    to store the underlying model data, which may be large.
    """
    return __typ0(run_id=__tmp0.run_id, epoch_num=__tmp0.epoch_num)

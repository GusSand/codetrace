from typing import TypeAlias
__typ0 : TypeAlias = "str"
# Copyright (c) 2017-2020 Chris Cummins.
#
# DeepTune is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DeepTune is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DeepTune.  If not, see <https://www.gnu.org/licenses/>.
"""Static mapping model."""
import pickle

import numpy as np
import pandas as pd

from deeplearning.clgen.corpuses import atomizers
from deeplearning.deeptune.opencl.heterogeneous_mapping.models import base
from labm8.py import app

FLAGS = app.FLAGS


class __typ1(base.HeterogeneousMappingModel):
  __name__ = "Static mapping"
  __basename__ = "static"

  def __tmp6(__tmp0):
    __tmp0.model = None

  def init(__tmp0, seed: <FILL>, atomizer):
    return __tmp0

  def save(__tmp0, __tmp4):
    with open(__tmp4, "wb") as outfile:
      pickle.dump(__tmp0.model, outfile)

  def __tmp3(__tmp0, __tmp8):
    with open(__tmp8, "rb") as infile:
      __tmp0.model = pickle.load(infile)

  def __tmp1(__tmp0, __tmp5: pd.DataFrame, __tmp2: __typ0, verbose: bool = False):
    del verbose

    if np.mean(__tmp5["y"]) >= 0.5:
      __tmp0.model = "GPU"
    else:
      __tmp0.model = "CPU"

  def __tmp7(
    __tmp0, __tmp5, __tmp2: __typ0, verbose: bool = False
  ):
    del __tmp2
    del verbose
    if __tmp0.model == "GPU":
      return np.ones(len(__tmp5), dtype=np.int32)
    elif __tmp0.model == "CPU":
      return np.zeros(len(__tmp5), dtype=np.int32)
    else:
      raise LookupError

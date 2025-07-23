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


class __typ0(base.HeterogeneousMappingModel):
  __name__ = "Static mapping"
  __basename__ = "static"

  def __tmp4(__tmp0):
    __tmp0.model = None

  def __tmp1(__tmp0, __tmp6, atomizer):
    return __tmp0

  def save(__tmp0, __tmp3):
    with open(__tmp3, "wb") as outfile:
      pickle.dump(__tmp0.model, outfile)

  def restore(__tmp0, __tmp7):
    with open(__tmp7, "rb") as infile:
      __tmp0.model = pickle.load(infile)

  def train(__tmp0, __tmp5, __tmp2: <FILL>, verbose: bool = False):
    del verbose

    if np.mean(__tmp5["y"]) >= 0.5:
      __tmp0.model = "GPU"
    else:
      __tmp0.model = "CPU"

  def predict(
    __tmp0, __tmp5, __tmp2, verbose: bool = False
  ):
    del __tmp2
    del verbose
    if __tmp0.model == "GPU":
      return np.ones(len(__tmp5), dtype=np.int32)
    elif __tmp0.model == "CPU":
      return np.zeros(len(__tmp5), dtype=np.int32)
    else:
      raise LookupError

from typing import TypeAlias
__typ0 : TypeAlias = "int"
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

  def __init__(__tmp1):
    __tmp1.model = None

  def __tmp2(__tmp1, seed: __typ0, atomizer):
    return __tmp1

  def __tmp0(__tmp1, __tmp4):
    with open(__tmp4, "wb") as outfile:
      pickle.dump(__tmp1.model, outfile)

  def restore(__tmp1, inpath):
    with open(inpath, "rb") as infile:
      __tmp1.model = pickle.load(infile)

  def train(__tmp1, df: pd.DataFrame, __tmp3: str, verbose: bool = False):
    del verbose

    if np.mean(df["y"]) >= 0.5:
      __tmp1.model = "GPU"
    else:
      __tmp1.model = "CPU"

  def predict(
    __tmp1, df, __tmp3: <FILL>, verbose: bool = False
  ):
    del __tmp3
    del verbose
    if __tmp1.model == "GPU":
      return np.ones(len(df), dtype=np.int32)
    elif __tmp1.model == "CPU":
      return np.zeros(len(df), dtype=np.int32)
    else:
      raise LookupError

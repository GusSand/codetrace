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
"""Grewe et. al model."""
import pickle

import pandas as pd
from sklearn import tree as sktree

from datasets.opencl.device_mapping import opencl_device_mapping_dataset
from deeplearning.clgen.corpuses import atomizers
from deeplearning.deeptune.opencl.heterogeneous_mapping.models import base
from labm8.py import app

FLAGS = app.FLAGS


class __typ1(base.HeterogeneousMappingModel):
  """Grewe et al. predictive model for heterogeneous device mapping.

  The Grewe et al. predictive model uses decision trees and hand engineered
  features to predict optimal device mapping, described in publication:

    ﻿Grewe, D., Wang, Z., & O’Boyle, M. (2013). Portable Mapping of Data
    Parallel Programs to OpenCL for Heterogeneous Systems. In CGO. IEEE.
    https://doi.org/10.1109/CGO.2013.6494993
  """

  __name__ = "Grewe et al."
  __basename__ = "grewe"

  def __tmp8(__tmp1):
    __tmp1.model = None

  def __tmp3(__tmp1, __tmp9, atomizer: atomizers.AtomizerBase):
    __tmp1.model = sktree.DecisionTreeClassifier(
      random_state=__tmp9,
      splitter="best",
      criterion="entropy",
      max_depth=5,
      min_samples_leaf=5,
    )
    return __tmp1

  def __tmp0(__tmp1, __tmp6):
    with open(__tmp6, "wb") as outfile:
      pickle.dump(__tmp1.model, outfile)

  def __tmp5(__tmp1, __tmp10):
    with open(__tmp10, "rb") as infile:
      __tmp1.model = pickle.load(infile)

  def __tmp2(__tmp1, __tmp7, __tmp4: str, verbose: bool = False):
    del verbose
    features = opencl_device_mapping_dataset.ComputeGreweFeaturesForGpu(
      __tmp4, __tmp7
    ).values
    __tmp1.model.fit(features, __tmp7["y"])

  def predict(
    __tmp1, __tmp7, __tmp4: <FILL>, verbose: bool = False
  ):
    del verbose
    features = opencl_device_mapping_dataset.ComputeGreweFeaturesForGpu(
      __tmp4, __tmp7
    ).values
    return __tmp1.model.predict(features)

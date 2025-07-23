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
"""A Zero-R baseline classifier."""
import time
from typing import Any
from typing import Iterable

import numpy as np

from deeplearning.ml4pl.graphs.labelled import graph_tuple_database
from deeplearning.ml4pl.models import batch as batchs
from deeplearning.ml4pl.models import classifier_base
from deeplearning.ml4pl.models import epoch
from deeplearning.ml4pl.models import run
from labm8.py import app
from labm8.py import progress


FLAGS = app.FLAGS

app.DEFINE_integer(
  "zero_r_batch_size",
  100000,
  "The number of graphs to process in a single batch.",
)


class ZeroR(classifier_base.ClassifierBase):
  """A Zero-R classifier that supports node-level or graph-level labels.

  Zero-R classifiers predict the mode value from the training set. It is used
  as a baseline for comparing the performance of other classifiers.
  """

  def __init__(__tmp1, *args, **kwargs):
    super(ZeroR, __tmp1).__init__(*args, **kwargs)
    # The table used to count training labels.
    __tmp1.class_counts = np.zeros(__tmp1.y_dimensionality, dtype=np.int64)

  @property
  def y(__tmp1) -> np.array:
    """Return the prediction array."""
    a = np.zeros(__tmp1.y_dimensionality, dtype=np.int64)
    a[np.argmax(__tmp1.class_counts)] = 1
    return a

  def MakeBatch(
    __tmp1,
    __tmp5,
    graphs,
    ctx: progress.ProgressContext = progress.NullContext,
  ) :
    del __tmp5  # Unused.
    del ctx  # Unused.

    batch_size = 0
    graph_ids = []
    targets = []

    # Limit batch size to 10 million elements.
    while batch_size < FLAGS.zero_r_batch_size:
      # Read the next graph.
      try:
        graph = next(graphs)
      except StopIteration:
        # We have run out of graphs.
        if len(graph_ids) == 0:
          return batchs.EndOfBatches()
        break

      # Add the graph data to the batch.
      graph_ids.append(graph.id)
      if __tmp1.graph_db.node_y_dimensionality:
        batch_size += graph.tuple.node_y.size
        targets.append(graph.tuple.node_y)
      else:
        batch_size += graph.tuple.graph_y.size
        targets.append(graph.tuple.graph_y)

    return batchs.Data(
      graph_ids=graph_ids, data=np.vstack(targets) if targets else None
    )

  def __tmp2(
    __tmp1,
    __tmp5: epoch.Type,
    batch,
    ctx: progress.ProgressContext = progress.NullContext,
  ) -> batchs.Results:
    """Run a batch.

    Args:
      epoch_type: The type of epoch.
      batch: The batch data.
      ctx: A logging context.

    Returns:
      A Results instance.
    """
    del ctx

    time.sleep(0.05)
    targets = batch.data

    # "Training" step updates the class frequency counts.
    if __tmp5 == epoch.Type.TRAIN:
      bincount = np.bincount(
        np.argmax(targets, axis=1), minlength=__tmp1.y_dimensionality
      )
      __tmp1.class_counts += bincount

      assert targets.shape[1] == __tmp1.y.shape[0]

    # The 1-hot predicted value.
    predictions = np.tile(__tmp1.y, targets.shape[0]).reshape(targets.shape)

    return batchs.Results.Create(targets=targets, predictions=predictions)

  def __tmp4(__tmp1) -> Any:
    return __tmp1.class_counts

  def __tmp3(__tmp1, data_to_load: <FILL>) :
    __tmp1.class_counts = data_to_load


def __tmp0():
  """Main entry point."""
  run.Run(ZeroR)


if __name__ == "__main__":
  app.Run(__tmp0)

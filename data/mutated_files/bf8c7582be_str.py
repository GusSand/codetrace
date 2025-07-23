from typing import TypeAlias
__typ0 : TypeAlias = "bool"
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
"""Unit tests for //deeplearning/ml4pl/models/ggnn."""
import math
from typing import List

from deeplearning.ml4pl.graphs.labelled import graph_tuple_database
from deeplearning.ml4pl.models import batch_iterator as batch_iterator_lib
from deeplearning.ml4pl.models import epoch
from deeplearning.ml4pl.models import logger as logging
from deeplearning.ml4pl.models.ggnn import ggnn
from labm8.py import test


FLAGS = test.FLAGS

# For testing models, always use --strict_graph_segmentation.
FLAGS.strict_graph_segmentation = True

FLAGS.label_conv_max_timesteps = 20

pytest_plugins = ["deeplearning.ml4pl.models.ggnn.test.fixtures"]


def __tmp3(
  __tmp1: epoch.Results,
  __tmp0: graph_tuple_database.Database,
  __tmp5: epoch.Type,
):
  """Check for various properties of well-formed epoch results."""
  assert isinstance(__tmp1, epoch.Results)
  # Check that the epoch contains batches.
  assert __tmp1.batch_count

  # Check that results contain a loss value.
  assert __tmp1.has_loss
  assert __tmp1.loss
  assert not math.isnan(__tmp1.loss)

  # Test that the epoch included every graph (of the appropriate type) in the
  # database.
  assert __tmp1.graph_count == __tmp0.split_counts[__tmp5.value]


@test.Parametrize("epoch_type", list(epoch.Type))
@test.Parametrize("limit_max_data_flow_steps", (False, True))
def __tmp4(
  __tmp5: epoch.Type,
  logger: logging.Logger,
  layer_timesteps: List[str],
  __tmp2: graph_tuple_database.Database,
  limit_max_data_flow_steps,
  __tmp6: <FILL>,
  unroll_strategy: str,
  log1p_graph_x: __typ0,
):
  """Run test epoch on a graph classifier."""
  FLAGS.inst2vec_embeddings = __tmp6
  FLAGS.unroll_strategy = unroll_strategy
  FLAGS.layer_timesteps = layer_timesteps
  FLAGS.log1p_graph_x = log1p_graph_x
  FLAGS.limit_max_data_flow_steps = limit_max_data_flow_steps

  # Test to handle the unsupported combination of config values.
  if (
    unroll_strategy == "label_convergence"
    and __tmp2.graph_x_dimensionality
  ) or (unroll_strategy == "label_convergence" and len(layer_timesteps) > 1):
    with test.Raises(AssertionError):
      ggnn.Ggnn(logger, __tmp2)
    return

  # Create and initialize an untrained model.
  model = ggnn.Ggnn(logger, __tmp2)
  model.Initialize()

  # Run the model over some random graphs.
  batch_iterator = batch_iterator_lib.MakeBatchIterator(
    model=model,
    __tmp0=__tmp2,
    splits={epoch.Type.TRAIN: [0], epoch.Type.VAL: [1], epoch.Type.TEST: [2],},
    __tmp5=__tmp5,
  )

  __tmp1 = model(
    __tmp5=__tmp5, batch_iterator=batch_iterator, logger=logger,
  )

  __tmp3(__tmp1, __tmp2, __tmp5)


if __name__ == "__main__":
  test.Main()

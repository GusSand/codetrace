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


def __tmp1(
  logger: logging.Logger,
  __tmp0,
  layer_timesteps,
  node_text_embedding_type,
  unroll_strategy: <FILL>,
):
  """Test creating and restoring model from checkpoint."""
  FLAGS.inst2vec_embeddings = node_text_embedding_type
  FLAGS.unroll_strategy = unroll_strategy
  FLAGS.layer_timesteps = layer_timesteps

  # Test to handle the unsupported combination of config values.
  if (
    unroll_strategy == "label_convergence"
    and __tmp0.graph_x_dimensionality
  ) or (unroll_strategy == "label_convergence" and len(layer_timesteps) > 1):
    with test.Raises(AssertionError):
      ggnn.Ggnn(logger, __tmp0)
    return

  # Create and initialize a model.
  model = ggnn.Ggnn(logger, __tmp0)
  model.Initialize()

  # Create a checkpoint from the model.
  checkpoint_ref = model.SaveCheckpoint()

  # Reset the model state to the checkpoint.
  model.RestoreFrom(checkpoint_ref)

  # Run a test epoch to make sure the restored model works.
  batch_iterator = batch_iterator_lib.MakeBatchIterator(
    model=model,
    graph_db=__tmp0,
    splits={epoch.Type.TRAIN: [0], epoch.Type.VAL: [1], epoch.Type.TEST: [2],},
    epoch_type=epoch.Type.TEST,
  )
  model(
    epoch_type=epoch.Type.TEST, batch_iterator=batch_iterator, logger=logger,
  )

  # Create a new model instance and restore its state from the checkpoint.
  new_model = ggnn.Ggnn(logger, __tmp0,)
  new_model.RestoreFrom(checkpoint_ref)

  # Check that the new model works.
  batch_iterator = batch_iterator_lib.MakeBatchIterator(
    model=new_model,
    graph_db=__tmp0,
    splits={epoch.Type.TRAIN: [0], epoch.Type.VAL: [1], epoch.Type.TEST: [2],},
    epoch_type=epoch.Type.TEST,
  )
  new_model(
    epoch_type=epoch.Type.TEST, batch_iterator=batch_iterator, logger=logger,
  )


if __name__ == "__main__":
  test.Main()

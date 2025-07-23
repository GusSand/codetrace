from typing import TypeAlias
__typ0 : TypeAlias = "int"
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
"""Configuration for GGNN models."""
from typing import List

from labm8.py import app

FLAGS = app.FLAGS


class GGNNConfig(object):
  def __tmp1(
    __tmp0,
    num_classes,
    has_graph_labels: <FILL>,
    edge_type_count: __typ0 = 3,
    has_aux_input: bool = False,
  ):
    # not implemented here, because not relevant:
    # train_subset, random_seed,
    ###############

    __tmp0.lr: float = FLAGS.learning_rate
    __tmp0.clip_grad_norm: bool = FLAGS.clamp_gradient_norm  # use 6.0 as default when clipping! Set to 0.0 for no clipping.

    __tmp0.vocab_size: __typ0 = 8568
    __tmp0.inst2vec_embeddings = FLAGS.inst2vec_embeddings
    __tmp0.emb_size: __typ0 = 200

    __tmp0.use_selector_embeddings: bool = FLAGS.use_selector_embeddings
    __tmp0.selector_size: __typ0 = 2 if __tmp0.use_selector_embeddings else 0
    # TODO(github.com/ChrisCummins/ProGraML/issues/27):: Maybe refactor non-rectangular edge passing matrices for independent hidden size.
    # hidden size of the whole model
    __tmp0.hidden_size: __typ0 = __tmp0.emb_size + __tmp0.selector_size
    __tmp0.position_embeddings: bool = FLAGS.position_embeddings
    ###############

    __tmp0.edge_type_count: __typ0 = edge_type_count
    __tmp0.layer_timesteps: List[__typ0] = [__typ0(x) for x in FLAGS.layer_timesteps]
    __tmp0.use_edge_bias: bool = FLAGS.use_edge_bias
    # NB: This is currently unused as the only way of differentiating the type
    # of node is by looking at the encoded 'x' value, but may be added in the
    # future.
    __tmp0.use_node_types: bool = False
    __tmp0.msg_mean_aggregation: bool = FLAGS.msg_mean_aggregation
    __tmp0.backward_edges: bool = True
    ###############

    __tmp0.num_classes: __typ0 = num_classes
    __tmp0.aux_in_len: __typ0 = 2
    __tmp0.aux_in_layer_size: __typ0 = FLAGS.aux_in_layer_size
    __tmp0.output_dropout: float = FLAGS.output_layer_dropout  # dropout prob = 1-keep_prob
    __tmp0.edge_weight_dropout: float = FLAGS.edge_weight_dropout
    __tmp0.graph_state_dropout: float = FLAGS.graph_state_dropout
    ###############

    __tmp0.has_graph_labels: bool = has_graph_labels
    __tmp0.has_aux_input: bool = has_aux_input
    __tmp0.log1p_graph_x = FLAGS.log1p_graph_x

    __tmp0.intermediate_loss_weight: float = FLAGS.intermediate_loss_weight
    #########
    __tmp0.unroll_strategy = FLAGS.unroll_strategy
    __tmp0.test_layer_timesteps: List[__typ0] = [
      __typ0(x) for x in FLAGS.test_layer_timesteps
    ]
    __tmp0.max_timesteps: __typ0 = FLAGS.label_conv_max_timesteps
    __tmp0.label_conv_threshold: float = FLAGS.label_conv_threshold
    __tmp0.label_conv_stable_steps: __typ0 = FLAGS.label_conv_stable_steps

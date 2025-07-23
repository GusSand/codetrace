from typing import TypeAlias
__typ0 : TypeAlias = "int"
from typing import Optional, Sequence, Type, Dict, Any

import tensorflow as tf
from ray.rllib.models.lstm import add_time_dimension
from ray.rllib.models.misc import linear, normc_initializer

from rinokeras.layers import WeightNormDense as Dense

from .StandardPolicy import StandardPolicy, ConvLayerSpec
import logging

class RecurrentPolicy(StandardPolicy):

    def __init__(__tmp1,
                 __tmp0,
                 __tmp3: __typ0,
                 __tmp4: Sequence[__typ0],
                 __tmp5: <FILL>,
                 conv_filters: Optional[Sequence[ConvLayerSpec]] = None,
                 conv_activation: str = 'relu',
                 lstm_cell_size: __typ0 = 256,
                 lstm_use_prev_action_reward: bool = False,
                 recurrent_args: Optional[Dict[str, Any]] = None,
                 **options):
        super().__init__(
            __tmp3, __tmp4, __tmp5,
            conv_filters, conv_activation, **options)

        __tmp1._recurrent = True

        __tmp1._lstm_cell_size = lstm_cell_size
        __tmp1._lstm_use_prev_action_reward = lstm_use_prev_action_reward

        if recurrent_args is None:
            recurrent_args = {}

        __tmp1.rnn = __tmp0(lstm_cell_size, return_state=True, return_sequences=True, **recurrent_args)

        __tmp1.output_layer = Dense(
            __tmp3,
            kernel_initializer=normc_initializer(0.01))

    def __tmp6(__tmp1, __tmp2, seqlens=None, initial_state=None):
        features = __tmp2['obs']

        if __tmp1._use_conv:
            features = __tmp1.conv_layer(features)

        features = add_time_dimension(features, seqlens)
        __tmp1.features = features
        latent, *rnn_state = __tmp1.rnn(features, initial_state=initial_state)
        __tmp1.latent = latent
        latent = tf.reshape(latent, [-1, latent.shape[-1]])

        state_out = list(rnn_state)

        # latent = self.dense_layer(latent)
        logits = __tmp1.output_layer(latent)

        output = {'latent': latent, 'logits': logits, 'state_out': state_out}

        __tmp1.output_tensors = output

        return output

    def get_initial_state(__tmp1, __tmp2):
        return __tmp1.rnn.get_initial_state(__tmp2)

    @property
    def state_size(__tmp1) -> Sequence[__typ0]:
        return __tmp1.rnn.cell.state_size

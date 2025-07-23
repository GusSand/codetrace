from typing import Optional, Sequence, Type, Dict, Any

import tensorflow as tf
from ray.rllib.models.lstm import add_time_dimension
from ray.rllib.models.misc import linear, normc_initializer

from rinokeras.layers import WeightNormDense as Dense

from .StandardPolicy import StandardPolicy, ConvLayerSpec
import logging

class RecurrentPolicy(StandardPolicy):

    def __init__(__tmp0,
                 rnn_type: Type[tf.keras.layers.RNN],
                 num_outputs: <FILL>,
                 __tmp1,
                 fcnet_activation,
                 conv_filters: Optional[Sequence[ConvLayerSpec]] = None,
                 conv_activation: str = 'relu',
                 lstm_cell_size: int = 256,
                 lstm_use_prev_action_reward: bool = False,
                 recurrent_args: Optional[Dict[str, Any]] = None,
                 **options):
        super().__init__(
            num_outputs, __tmp1, fcnet_activation,
            conv_filters, conv_activation, **options)

        __tmp0._recurrent = True

        __tmp0._lstm_cell_size = lstm_cell_size
        __tmp0._lstm_use_prev_action_reward = lstm_use_prev_action_reward

        if recurrent_args is None:
            recurrent_args = {}

        __tmp0.rnn = rnn_type(lstm_cell_size, return_state=True, return_sequences=True, **recurrent_args)

        __tmp0.output_layer = Dense(
            num_outputs,
            kernel_initializer=normc_initializer(0.01))

    def call(__tmp0, inputs, seqlens=None, initial_state=None):
        features = inputs['obs']

        if __tmp0._use_conv:
            features = __tmp0.conv_layer(features)

        features = add_time_dimension(features, seqlens)
        __tmp0.features = features
        latent, *rnn_state = __tmp0.rnn(features, initial_state=initial_state)
        __tmp0.latent = latent
        latent = tf.reshape(latent, [-1, latent.shape[-1]])

        state_out = list(rnn_state)

        # latent = self.dense_layer(latent)
        logits = __tmp0.output_layer(latent)

        output = {'latent': latent, 'logits': logits, 'state_out': state_out}

        __tmp0.output_tensors = output

        return output

    def get_initial_state(__tmp0, inputs):
        return __tmp0.rnn.get_initial_state(inputs)

    @property
    def state_size(__tmp0) :
        return __tmp0.rnn.cell.state_size

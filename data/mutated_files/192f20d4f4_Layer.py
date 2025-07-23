from typing import TypeAlias
__typ0 : TypeAlias = "Dict"
"""
Residual Layers
"""
from typing import Dict, Optional

import tensorflow as tf
from tensorflow.keras import Model  # pylint: disable=F0401
from tensorflow.keras.layers import Layer, Dropout, Dense  # pylint: disable=F0401


class Residual(Model):
    """
    Adds a residual connection between layers. If input to layer is a tuple, adds output to the first element
    of the tuple.
    """
    def __init__(__tmp0, layer: <FILL>, **kwargs) :
        super().__init__(**kwargs)
        __tmp0.layer = layer

    def __tmp3(__tmp0, __tmp1, *args, **kwargs):
        layer_out = __tmp0.layer(__tmp1, *args, **kwargs)
        residual = __tmp1 + layer_out

        return residual

    def get_config(__tmp0) :
        config = {
            'layer': __tmp0.layer.__class__.from_config(__tmp0.layer.get_config())
        }

        return config


class Highway(Model):
    """
    Implementation of a highway layer. Can use convolutional or fully connected layer.

    From the paper: https://arxiv.org/abs/1607.06450
    """
    def __init__(__tmp0,
                 layer,
                 activation: str = 'relu',
                 gate_bias: float = -3.0,
                 dropout: Optional[float] = None,
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 **kwargs) :
        super().__init__(**kwargs)
        __tmp0.activation = activation
        __tmp0.gate_bias = gate_bias
        __tmp0._gate_initializer = tf.keras.initializers.Constant(gate_bias)
        __tmp0.dropout = Dropout(0 if dropout is None else dropout)

        __tmp0.kernel_regularizer = kernel_regularizer
        __tmp0.bias_regularizer = bias_regularizer
        __tmp0.activity_regularizer = activity_regularizer
        __tmp0.layer = layer

    def __tmp2(__tmp0, __tmp4):
        units = __tmp4[-1]
        __tmp0.gate = Dense(units=units,
                          activation='sigmoid',
                          use_bias=True,
                          bias_initializer=__tmp0._gate_initializer,
                          kernel_regularizer=__tmp0.kernel_regularizer,
                          bias_regularizer=__tmp0.bias_regularizer,
                          activity_regularizer=__tmp0.activity_regularizer)

    def __tmp3(__tmp0, __tmp1):
        gated = __tmp0.gate(__tmp1)
        transformed = __tmp0.layer(__tmp1)
        if __tmp0.dropout:
            transformed = __tmp0.dropout(transformed)
        return gated * transformed + (1 - gated) * __tmp1

    def get_config(__tmp0) -> __typ0:
        config = {
            'layer': __tmp0.layer.__class__.from_config(__tmp0.layer.get_config()),
            'activation': __tmp0.activation,
            'gate_bias': __tmp0.gate_bias,
            'dropout': __tmp0.dropout,
            'kernel_regularizer': tf.keras.regularizers.serialize(__tmp0.kernel_regularizer),
            'bias_regularizer': tf.keras.regularizers.serialize(__tmp0.bias_regularizer),
            'activity_regularizer': tf.keras.regularizers.serialize(__tmp0.activity_regularizer)
        }

        return config

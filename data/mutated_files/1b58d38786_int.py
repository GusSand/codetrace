import tensorflow as tf
from typing import Optional
from tensorflow.keras import Model
from tensorflow.keras.layers import Dropout, Dense, Conv1D

from rinokeras.core.v1x.common.layers import Stack, LayerNorm
from rinokeras.core.v1x.common.layers import WeightNormDense


class __typ0(Model):

    def __init__(__tmp0, filter_size: <FILL>,
                 hidden_size,
                 kernel_size: int = 7,
                 dropout: Optional[float] = None,
                 use_conv: bool = False,
                 use_weight_norm: bool = True,
                 use_residual_norm: bool = True,
                 kernel_initializer: Optional[tf.keras.initializers.Initializer] = 'glorot_uniform',
                 kernel_regularizer: Optional[tf.keras.regularizers.Regularizer] = None,
                 bias_regularizer: Optional[tf.keras.regularizers.Regularizer] = None,
                 activity_regularizer:  Optional[tf.keras.regularizers.Regularizer] = None) :
        super().__init__()
        __tmp0.filter_size = filter_size
        __tmp0.hidden_size = hidden_size
        __tmp0.kernel_size = kernel_size
        __tmp0.use_conv = use_conv
        __tmp0.use_residual_norm = use_residual_norm
        __tmp0.norm = LayerNorm()
        layer_args = {
            'kernel_initializer': kernel_initializer,
            'kernel_regularizer': kernel_regularizer,
            'bias_regularizer': bias_regularizer,
            'activity_regularizer': activity_regularizer}

        __tmp0.use_weight_norm = use_weight_norm
        if __tmp0.use_weight_norm:
            layer_type = WeightNormDense if not use_conv else Conv1D
        else:
            layer_type = Dense if not use_conv else Conv1D

        if use_conv:
            conv_args = {
                'kernel_size': kernel_size,
                'padding': 'same',
                'strides': 1}
            layer_args.update(conv_args)
        __tmp0.feed_forward = Stack()
        __tmp0.feed_forward.add(
            layer_type(filter_size, activation='relu', **layer_args))
        __tmp0.feed_forward.add(
            layer_type(hidden_size, activation='linear', **layer_args))
        __tmp0.feed_forward.add(Dropout(0 if dropout is None else dropout))

        __tmp0.kernel_initializer = tf.keras.initializers.get(kernel_initializer)
        __tmp0.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        __tmp0.bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        __tmp0.activity_regularizer = tf.keras.regularizers.get(activity_regularizer)

    def call(__tmp0, __tmp1, padding_mask=None):
        if padding_mask is not None:
            __tmp1 = __tmp1 * tf.cast(padding_mask[..., None], __tmp1.dtype)

        ff_inputs = __tmp0.norm(__tmp1) if __tmp0.use_residual_norm else __tmp1
        dense_out = __tmp0.feed_forward(ff_inputs)

        output = __tmp1 + dense_out
        if not __tmp0.use_residual_norm:
            output = __tmp0.norm(output)
        return output

    def __tmp2(__tmp0):
        config = {
            'filter_size': __tmp0.filter_size,
            'hidden_size': __tmp0.hidden_size,
            'kernel_size': __tmp0.kernel_size,
            'use_conv': __tmp0.use_conv,
            'use_weight_norm': __tmp0.use_weight_norm,
            'use_residual_norm': __tmp0.use_residual_norm,
            'kernel_initializer':
            tf.keras.initializers.serialize(__tmp0.kernel_initializer),
            'kernel_regularizer':
            tf.keras.regularizers.serialize(__tmp0.kernel_regularizer),
            'bias_regularizer':
            tf.keras.regularizers.serialize(__tmp0.bias_regularizer),
            'activity_regularizer':
            tf.keras.regularizers.serialize(__tmp0.activity_regularizer),
        }
        return config


    @classmethod
    def from_config(cls, config):
        return cls(**config)

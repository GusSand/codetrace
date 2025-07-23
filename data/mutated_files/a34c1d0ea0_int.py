from typing import Optional, Tuple

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Activation, Conv1D, Conv2D, Conv3D, Dropout, BatchNormalization, Layer, LeakyReLU

from rinokeras.core.v1x.common.layers.stack import Stack
from rinokeras.core.v1x.common.layers.normalization import LayerNorm
from rinokeras.core.v1x.common.layers.residual import Residual


class NormedConvStack(Stack):

    def __init__(__tmp1,
                 __tmp0,
                 filters,
                 kernel_size,
                 layer_norm: bool = False,
                 activation: str = 'relu') :
        super().__init__()
        assert 1 <= __tmp0 <= 3
        if layer_norm:
            __tmp1.add(LayerNorm())
        __tmp1.add(Activation(activation))

        conv_func = [Conv1D, Conv2D, Conv3D]
        __tmp1.add(conv_func[__tmp0 - 1](
            filters=filters, kernel_size=kernel_size, strides=1, padding='same', use_bias=True))

    def call(__tmp1, __tmp2, mask=None, **kwargs):
        if mask is not None:
            mask = tf.cast(mask, __tmp2.dtype)
            if mask.shape.ndims == 2:
                mask = mask[:, :, None]
            __tmp2 = __tmp2 * mask
        return super().call(__tmp2, **kwargs)


class PaddedConv(Stack):

    def __init__(__tmp1,
                 __tmp0: int,
                 filters: <FILL>,
                 kernel_size: int,
                 dilation_rate: int = 1,
                 activation: str = 'relu',
                 dropout: Optional[float] = None) :
        super().__init__()
        assert 1 <= __tmp0 <= 3
        conv_func = [Conv1D, Conv2D, Conv3D]

        def get_activation():
            if activation == 'glu':
                return GLUActivation()
            elif activation == 'lrelu':
                return LeakyReLU()
            else:
                return Activation(activation)

        __tmp1.add(BatchNormalization())
        __tmp1.add(get_activation())
        __tmp1.add(conv_func[__tmp0 - 1](
            filters=filters, kernel_size=kernel_size, strides=1, padding='same', use_bias=True,
            activation='linear', dilation_rate=dilation_rate, kernel_initializer='he_normal'))
        if dropout is not None:
            __tmp1.add(Dropout(dropout))

    def call(__tmp1, __tmp2, mask=None):
        if mask is not None:
            mask = tf.cast(mask, __tmp2.dtype)
            if mask.shape.ndims == __tmp2.shape.ndims - 1:
                mask = tf.expand_dims(mask, -1)
            __tmp2 = __tmp2 * mask
        return super().call(__tmp2, mask=mask)


class GLUActivation(Layer):

    def call(__tmp1, __tmp2):
        output, gate = tf.split(__tmp2, axis=-1, num_or_size_splits=2)
        return output * tf.nn.sigmoid(gate)


class ResidualBlock(Residual):

    def __init__(__tmp1,
                 __tmp0,
                 filters: int,
                 kernel_size,
                 activation: str = 'relu',
                 dilation_rate: int = 1,
                 layer_norm: bool = False,
                 dropout: Optional[float] = None,
                 add_checkpoint: bool = False,  # used with memory saving gradients
                 **kwargs) -> None:

        __tmp1._add_checkpoint = add_checkpoint
        layer = Stack()
        if layer_norm:
            layer.add(LayerNorm())
        layer.add(PaddedConv(__tmp0, filters, kernel_size, dilation_rate, activation, dropout))
        layer.add(PaddedConv(__tmp0, filters, kernel_size, dilation_rate, activation, dropout))

        super().__init__(layer, **kwargs)

    def call(__tmp1, __tmp2, *args, **kwargs):
        output = super().call(__tmp2, *args, **kwargs)

        if __tmp1._add_checkpoint:
            tf.add_to_collection('checkpoints', output)

        return output


class GroupedConvolution(tf.keras.Model):
    def __init__(__tmp1, cardinality: int = 1, n_filters: int = 64, kernel_size: Tuple[int, int] = (3, 3), stride: Tuple[int, int] = (1,1)) :
        super(GroupedConvolution, __tmp1).__init__()
        __tmp1.cardinality = cardinality

        if __tmp1.cardinality == 1:
            __tmp1.output_layer = tf.keras.layers.Conv2D(filters=n_filters, kernel_size=kernel_size, strides=stride, padding='same')
        else:
            if (n_filters % __tmp1.cardinality != 0):
                raise ValueError('Residual grouped convolution filters must be divisible by the cardinality')

            __tmp1._dim = n_filters // __tmp1.cardinality

            __tmp1._layer_list = tf.contrib.checkpoint.List()
            for idx in range(__tmp1.cardinality):
                group = tf.keras.layers.Lambda(lambda z: z[:,:,:, idx * __tmp1._dim: (idx + 1) * __tmp1._dim])
                group = tf.keras.layers.Conv2D(filters=__tmp1._dim, kernel_size=kernel_size, strides=stride, padding='same')
                __tmp1._layer_list.append(group)

    def call(__tmp1, __tmp2, *args, **kwargs):
        if __tmp1.cardinality == 1:
            return __tmp1.output_layer(__tmp2)
        else:
            layers = [layer(__tmp2) for layer in __tmp1._layer_list]
            return tf.keras.layers.Concatenate()(layers)

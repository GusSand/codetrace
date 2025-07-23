from typing import Optional, Tuple

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Activation, Conv1D, Conv2D, Conv3D, Dropout, BatchNormalization, Layer, LeakyReLU

from rinokeras.core.v1x.common.layers.stack import Stack
from rinokeras.core.v1x.common.layers.normalization import LayerNorm
from rinokeras.core.v1x.common.layers.residual import Residual


class __typ1(Stack):

    def __init__(__tmp2,
                 __tmp1: int,
                 filters: int,
                 __tmp0: int,
                 layer_norm: bool = False,
                 activation: str = 'relu') -> None:
        super().__init__()
        assert 1 <= __tmp1 <= 3
        if layer_norm:
            __tmp2.add(LayerNorm())
        __tmp2.add(Activation(activation))

        conv_func = [Conv1D, Conv2D, Conv3D]
        __tmp2.add(conv_func[__tmp1 - 1](
            filters=filters, __tmp0=__tmp0, strides=1, padding='same', use_bias=True))

    def call(__tmp2, __tmp3, mask=None, **kwargs):
        if mask is not None:
            mask = tf.cast(mask, __tmp3.dtype)
            if mask.shape.ndims == 2:
                mask = mask[:, :, None]
            __tmp3 = __tmp3 * mask
        return super().call(__tmp3, **kwargs)


class __typ0(Stack):

    def __init__(__tmp2,
                 __tmp1: int,
                 filters: int,
                 __tmp0: int,
                 dilation_rate: int = 1,
                 activation: str = 'relu',
                 dropout: Optional[float] = None) -> None:
        super().__init__()
        assert 1 <= __tmp1 <= 3
        conv_func = [Conv1D, Conv2D, Conv3D]

        def get_activation():
            if activation == 'glu':
                return __typ3()
            elif activation == 'lrelu':
                return LeakyReLU()
            else:
                return Activation(activation)

        __tmp2.add(BatchNormalization())
        __tmp2.add(get_activation())
        __tmp2.add(conv_func[__tmp1 - 1](
            filters=filters, __tmp0=__tmp0, strides=1, padding='same', use_bias=True,
            activation='linear', dilation_rate=dilation_rate, kernel_initializer='he_normal'))
        if dropout is not None:
            __tmp2.add(Dropout(dropout))

    def call(__tmp2, __tmp3, mask=None):
        if mask is not None:
            mask = tf.cast(mask, __tmp3.dtype)
            if mask.shape.ndims == __tmp3.shape.ndims - 1:
                mask = tf.expand_dims(mask, -1)
            __tmp3 = __tmp3 * mask
        return super().call(__tmp3, mask=mask)


class __typ3(Layer):

    def call(__tmp2, __tmp3):
        output, gate = tf.split(__tmp3, axis=-1, num_or_size_splits=2)
        return output * tf.nn.sigmoid(gate)


class __typ2(Residual):

    def __init__(__tmp2,
                 __tmp1: <FILL>,
                 filters,
                 __tmp0: int,
                 activation: str = 'relu',
                 dilation_rate: int = 1,
                 layer_norm: bool = False,
                 dropout: Optional[float] = None,
                 add_checkpoint: bool = False,  # used with memory saving gradients
                 **kwargs) -> None:

        __tmp2._add_checkpoint = add_checkpoint
        layer = Stack()
        if layer_norm:
            layer.add(LayerNorm())
        layer.add(__typ0(__tmp1, filters, __tmp0, dilation_rate, activation, dropout))
        layer.add(__typ0(__tmp1, filters, __tmp0, dilation_rate, activation, dropout))

        super().__init__(layer, **kwargs)

    def call(__tmp2, __tmp3, *args, **kwargs):
        output = super().call(__tmp3, *args, **kwargs)

        if __tmp2._add_checkpoint:
            tf.add_to_collection('checkpoints', output)

        return output


class __typ4(tf.keras.Model):
    def __init__(__tmp2, cardinality: int = 1, n_filters: int = 64, __tmp0: Tuple[int, int] = (3, 3), stride: Tuple[int, int] = (1,1)) :
        super(__typ4, __tmp2).__init__()
        __tmp2.cardinality = cardinality

        if __tmp2.cardinality == 1:
            __tmp2.output_layer = tf.keras.layers.Conv2D(filters=n_filters, __tmp0=__tmp0, strides=stride, padding='same')
        else:
            if (n_filters % __tmp2.cardinality != 0):
                raise ValueError('Residual grouped convolution filters must be divisible by the cardinality')

            __tmp2._dim = n_filters // __tmp2.cardinality

            __tmp2._layer_list = tf.contrib.checkpoint.List()
            for idx in range(__tmp2.cardinality):
                group = tf.keras.layers.Lambda(lambda z: z[:,:,:, idx * __tmp2._dim: (idx + 1) * __tmp2._dim])
                group = tf.keras.layers.Conv2D(filters=__tmp2._dim, __tmp0=__tmp0, strides=stride, padding='same')
                __tmp2._layer_list.append(group)

    def call(__tmp2, __tmp3, *args, **kwargs):
        if __tmp2.cardinality == 1:
            return __tmp2.output_layer(__tmp3)
        else:
            layers = [layer(__tmp3) for layer in __tmp2._layer_list]
            return tf.keras.layers.Concatenate()(layers)

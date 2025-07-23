from typing import Optional, Tuple

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Activation, Conv1D, Conv2D, Conv3D, Dropout, BatchNormalization, Layer, LeakyReLU

from rinokeras.core.v1x.common.layers.stack import Stack
from rinokeras.core.v1x.common.layers.normalization import LayerNorm
from rinokeras.core.v1x.common.layers.residual import Residual


class __typ1(Stack):

    def __init__(__tmp0,
                 __tmp3: int,
                 __tmp5: <FILL>,
                 __tmp4,
                 layer_norm: bool = False,
                 activation: str = 'relu') -> None:
        super().__init__()
        assert 1 <= __tmp3 <= 3
        if layer_norm:
            __tmp0.add(LayerNorm())
        __tmp0.add(Activation(activation))

        conv_func = [Conv1D, Conv2D, Conv3D]
        __tmp0.add(conv_func[__tmp3 - 1](
            __tmp5=__tmp5, __tmp4=__tmp4, strides=1, padding='same', use_bias=True))

    def call(__tmp0, __tmp1, mask=None, **kwargs):
        if mask is not None:
            mask = tf.cast(mask, __tmp1.dtype)
            if mask.shape.ndims == 2:
                mask = mask[:, :, None]
            __tmp1 = __tmp1 * mask
        return super().call(__tmp1, **kwargs)


class __typ0(Stack):

    def __init__(__tmp0,
                 __tmp3: int,
                 __tmp5: int,
                 __tmp4,
                 dilation_rate: int = 1,
                 activation: str = 'relu',
                 dropout: Optional[float] = None) -> None:
        super().__init__()
        assert 1 <= __tmp3 <= 3
        conv_func = [Conv1D, Conv2D, Conv3D]

        def __tmp2():
            if activation == 'glu':
                return __typ3()
            elif activation == 'lrelu':
                return LeakyReLU()
            else:
                return Activation(activation)

        __tmp0.add(BatchNormalization())
        __tmp0.add(__tmp2())
        __tmp0.add(conv_func[__tmp3 - 1](
            __tmp5=__tmp5, __tmp4=__tmp4, strides=1, padding='same', use_bias=True,
            activation='linear', dilation_rate=dilation_rate, kernel_initializer='he_normal'))
        if dropout is not None:
            __tmp0.add(Dropout(dropout))

    def call(__tmp0, __tmp1, mask=None):
        if mask is not None:
            mask = tf.cast(mask, __tmp1.dtype)
            if mask.shape.ndims == __tmp1.shape.ndims - 1:
                mask = tf.expand_dims(mask, -1)
            __tmp1 = __tmp1 * mask
        return super().call(__tmp1, mask=mask)


class __typ3(Layer):

    def call(__tmp0, __tmp1):
        output, gate = tf.split(__tmp1, axis=-1, num_or_size_splits=2)
        return output * tf.nn.sigmoid(gate)


class __typ2(Residual):

    def __init__(__tmp0,
                 __tmp3: int,
                 __tmp5,
                 __tmp4: int,
                 activation: str = 'relu',
                 dilation_rate: int = 1,
                 layer_norm: bool = False,
                 dropout: Optional[float] = None,
                 add_checkpoint: bool = False,  # used with memory saving gradients
                 **kwargs) -> None:

        __tmp0._add_checkpoint = add_checkpoint
        layer = Stack()
        if layer_norm:
            layer.add(LayerNorm())
        layer.add(__typ0(__tmp3, __tmp5, __tmp4, dilation_rate, activation, dropout))
        layer.add(__typ0(__tmp3, __tmp5, __tmp4, dilation_rate, activation, dropout))

        super().__init__(layer, **kwargs)

    def call(__tmp0, __tmp1, *args, **kwargs):
        output = super().call(__tmp1, *args, **kwargs)

        if __tmp0._add_checkpoint:
            tf.add_to_collection('checkpoints', output)

        return output


class __typ4(tf.keras.Model):
    def __init__(__tmp0, cardinality: int = 1, n_filters: int = 64, __tmp4: Tuple[int, int] = (3, 3), stride: Tuple[int, int] = (1,1)) -> None:
        super(__typ4, __tmp0).__init__()
        __tmp0.cardinality = cardinality

        if __tmp0.cardinality == 1:
            __tmp0.output_layer = tf.keras.layers.Conv2D(__tmp5=n_filters, __tmp4=__tmp4, strides=stride, padding='same')
        else:
            if (n_filters % __tmp0.cardinality != 0):
                raise ValueError('Residual grouped convolution filters must be divisible by the cardinality')

            __tmp0._dim = n_filters // __tmp0.cardinality

            __tmp0._layer_list = tf.contrib.checkpoint.List()
            for idx in range(__tmp0.cardinality):
                group = tf.keras.layers.Lambda(lambda z: z[:,:,:, idx * __tmp0._dim: (idx + 1) * __tmp0._dim])
                group = tf.keras.layers.Conv2D(__tmp5=__tmp0._dim, __tmp4=__tmp4, strides=stride, padding='same')
                __tmp0._layer_list.append(group)

    def call(__tmp0, __tmp1, *args, **kwargs):
        if __tmp0.cardinality == 1:
            return __tmp0.output_layer(__tmp1)
        else:
            layers = [layer(__tmp1) for layer in __tmp0._layer_list]
            return tf.keras.layers.Concatenate()(layers)

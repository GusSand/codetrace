"""
Feed forward/Conv layers for QANet
"""

from typing import Optional
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dropout, SeparableConv1D

from rinokeras.core.v1x.common import DenseStack, LayerNorm

class __typ0(Model):
    """QANet Feed Forward Block

    :param filter_size: The size of the input filter
    :type filter_size: int
    :param hidden_size: The size of the hidden layer
    :type hidden_size: int
    :param dropout: Dropout Weight
    :type dropout: Optional[float]

    """
    def __init__(__tmp0,
                 filter_size: int,
                 hidden_size: <FILL>,
                 dropout: Optional[float] = None,
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        
        __tmp0.filter_size = filter_size
        __tmp0.hidden_size = hidden_size
        
        __tmp0.norm = LayerNorm()
        __tmp0.feed_forward = DenseStack(
            [filter_size, hidden_size], output_activation=None,
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer,
            activity_regularizer=activity_regularizer)
        __tmp0.dropout_rate = dropout
        __tmp0.dropout = Dropout(0 if dropout is None else dropout)

        __tmp0.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        __tmp0.bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        __tmp0.activity_regularizer = tf.keras.regularizers.get(activity_regularizer)

    def __tmp3(__tmp0, inputs):
        """Compute a feed-forward pass on the inputs

        :param inputs: Input tensor
        :type inputs: tf.Tensor
        :return: Feed-Forward Output
        :rtype: tf.Tensor
        """
        norm_input = __tmp0.norm(inputs)
        dense_out = __tmp0.feed_forward(norm_input)
        dense_out = __tmp0.dropout(dense_out)
        return dense_out + inputs

    def get_config(__tmp0):
        __tmp1 = {
            'filter_size': __tmp0.filter_size,
            'hidden_size': __tmp0.hidden_size,
            'dropout': __tmp0.dropout_rate,
            'kernel_regularizer':
            tf.keras.regularizers.serialize(__tmp0.kernel_regularizer),
            'bias_regularizer':
            tf.keras.regularizers.serialize(__tmp0.bias_regularizer),
            'activity_regularizer':
            tf.keras.regularizers.serialize(__tmp0.activity_regularizer),
        }
        return __tmp1

    @classmethod
    def from_config(__tmp2, __tmp1):
        return __tmp2(**__tmp1)


class QANetConvBlock(Model):
    """QANet Convolutional Block

    Layered depth-wise separable convolutions. Based on https://arxiv.org/pdf/1804.09541.pdf.

    :param filters: The number of filters in the convolution
    :type filters: int
    :param kernel_size: The size of the convolutional kernel
    :type kernel_size: int
    :param dropout: Dropout weight
    :type dropout: Optional[float]

    """

    def __init__(__tmp0,
                 filters: int,
                 kernel_size,
                 dropout: Optional[float] = None,
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        __tmp0.filters = filters
        __tmp0.kernel_size = kernel_size
        __tmp0.norm = LayerNorm()
        __tmp0.conv_layer = SeparableConv1D(filters, kernel_size, padding='same',
                                          depthwise_regularizer=kernel_regularizer,
                                          pointwise_regularizer=kernel_regularizer)
        
        __tmp0.dropout_rate = dropout
        __tmp0.dropout = Dropout(0 if dropout is None else dropout)

        __tmp0.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        __tmp0.bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        __tmp0.activity_regularizer = tf.keras.regularizers.get(activity_regularizer)

    def __tmp3(__tmp0, inputs, mask=None):
        """
        :param inputs: a float32 Tensor with shape [batch_size, seqlen, d_model]
        :type inputs: tf.Tensor
        :param mask: a float32 Tensor with shape [batch_size, seqlen, seqlen]
        :type mask: tf.Tensor
        :return: a float32 Tensor with shape  [TODO (roshan_rao@berkeley.edu)]
        :rtype: tf.Tensor
        """
        norm_input = __tmp0.norm(inputs)
        if mask is not None:
            mask = tf.cast(mask[:, 0, :], norm_input.dtype)
            norm_input = norm_input * mask[:, :, None]

        conv_out = __tmp0.conv_layer(norm_input)
        conv_out = __tmp0.dropout(conv_out)

        return conv_out + inputs

    def get_config(__tmp0):
        __tmp1 = {
            'filters': __tmp0.filters,
            'kernel_size': __tmp0.kernel_size,
            'dropout': __tmp0.dropout_rate,
            'kernel_regularizer':
            tf.keras.regularizers.serialize(__tmp0.kernel_regularizer),
            'bias_regularizer':
            tf.keras.regularizers.serialize(__tmp0.bias_regularizer),
            'activity_regularizer':
            tf.keras.regularizers.serialize(__tmp0.activity_regularizer),
        }
        return __tmp1

    @classmethod
    def from_config(__tmp2, __tmp1):
        return __tmp2(**__tmp1)

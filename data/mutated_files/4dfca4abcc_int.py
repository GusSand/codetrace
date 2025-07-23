"""
QANet Attention Blocks
"""
import tensorflow as tf
from typing import Optional
from tensorflow.keras import Model
from rinokeras.core.v1x.common import SelfAttention, LayerNorm


class __typ0(Model):
    """QANet Self Attention Block

    :param n_heads: The number of heads in the self attention block
    :type n_heads: int
    :param dropout: Dropout weight
    :type dropout: Optional[float]

    """

    def __init__(__tmp0,
                 n_heads: <FILL>,
                 dropout: Optional[float] = None,
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)
        __tmp0.n_heads = n_heads
        __tmp0.dropout = dropout
        __tmp0.self_attention = SelfAttention('scaled_dot', n_heads, dropout,
                                            kernel_regularizer=kernel_regularizer,
                                            bias_regularizer=bias_regularizer,
                                            activity_regularizer=activity_regularizer)
        __tmp0.norm = LayerNorm()

        __tmp0.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        __tmp0.bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        __tmp0.activity_regularizer = tf.keras.regularizers.get(activity_regularizer)

    def __tmp5(__tmp0, __tmp1, mask=None):
        """Calls the Self-Attention module on the provided inputs

            :param inputs: The inputs to the self-attention module
            :type inputs: tf.Tensor
            :param mask: The self-attention mask
            :type mask: tf.Tensor
            :return: The self-attended inputs
            :rtype: tf.Tensor
        """
        norm_input = __tmp0.norm(__tmp1)
        attention = __tmp0.self_attention(norm_input, mask=mask)
        return attention + __tmp1  # Just do the residual connection manually

    def __tmp2(__tmp0):
        __tmp4 = {
            'n_heads': __tmp0.n_heads,
            'dropout': __tmp0.dropout,
            'kernel_regularizer':
            tf.keras.regularizers.serialize(__tmp0.kernel_regularizer),
            'bias_regularizer':
            tf.keras.regularizers.serialize(__tmp0.bias_regularizer),
            'activity_regularizer':
            tf.keras.regularizers.serialize(__tmp0.activity_regularizer),
        }
        return __tmp4

    @classmethod
    def __tmp6(__tmp3, __tmp4):
        return __tmp3(**__tmp4)

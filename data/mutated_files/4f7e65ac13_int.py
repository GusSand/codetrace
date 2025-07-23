
from typing import Optional
import tensorflow as tf
from tensorflow.keras import Model

from rinokeras.core.v1x.common import LayerDropoutStack, LayerDropout
from rinokeras.core.v1x.models.qanet import QANetConvBlock, QANetFeedForward, QANetSelfAttention


class __typ0(Model):
    """QANet Encoder Block
    """

    def __init__(__tmp0,
                 n_conv: int,
                 n_heads: int,
                 filter_size: int,
                 hidden_size: <FILL>,
                 kernel_size: int = 7,
                 dropout: Optional[float] = None,
                 layer_dropout: Optional[float] = None,
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 **kwargs) :
        super().__init__(**kwargs)

        __tmp0.n_conv = n_conv
        __tmp0.n_heads = n_heads
        __tmp0.filter_size = filter_size
        __tmp0.hidden_size = hidden_size
        __tmp0.kernel_size = kernel_size
        __tmp0.dropout = dropout
        __tmp0.layer_dropout = layer_dropout

        __tmp0.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        __tmp0.bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        __tmp0.activity_regularizer = tf.keras.regularizers.get(
            activity_regularizer)

        __tmp0.conv_stack = LayerDropoutStack([QANetConvBlock(hidden_size, kernel_size, dropout, kernel_regularizer=kernel_regularizer,
                                bias_regularizer=bias_regularizer,
                                activity_regularizer=activity_regularizer) for _ in range(n_conv)], layer_dropout=0 if layer_dropout is None else layer_dropout)
        __tmp0.self_attention = QANetSelfAttention(n_heads, dropout,
                                                 kernel_regularizer=kernel_regularizer,
                                                 bias_regularizer=bias_regularizer,
                                                 activity_regularizer=activity_regularizer)
        __tmp0.layer_drop_2 = LayerDropout(
            0 if layer_dropout is None else layer_dropout)
        __tmp0.feed_forward = QANetFeedForward(filter_size, hidden_size, dropout,
                                             kernel_regularizer=kernel_regularizer,
                                             bias_regularizer=bias_regularizer,
                                             activity_regularizer=activity_regularizer)
        __tmp0.layer_drop_3 = LayerDropout(
            0 if layer_dropout is None else layer_dropout)

    def __tmp5(__tmp0, __tmp1, mask=None):
        """Computes the encoding on the context

        :param inputs: The inputs to compute over
        :type inputs: tf.Tensor
        :param self_attention_mask: Self Attention Mask, defaults to None
        :param self_attention_mask: tf.Tensor, optional
        :param padding_mask: Padding Mask, defaults to None
        :param padding_mask: tf.Tensor, optional
        :return: The convolutional stack + the self-attention
        :rtype: tf.Tensor
        """

        if mask is not None:
            self_attention_mask, padding_mask = mask
        else:
            self_attention_mask, padding_mask = (None, None)

        conv_out = __tmp0.conv_stack(__tmp1, mask=padding_mask) 
        res_attn = __tmp0.layer_drop_2( __tmp0.self_attention(conv_out), conv_out, mask=self_attention_mask)
        output = __tmp0.layer_drop_3(__tmp0.feed_forward(res_attn),res_attn)
        # def subcall(inputs):
        # conv_out = self.conv_stack(inputs, mask=padding_mask)
        # res_attn = self.self_attention(conv_out, mask=self_attention_mask)
        # output = self.feed_forward(res_attn)
        # return output
        # output = self.layer_drop(subcall, inputs)
        return output

    def __tmp2(__tmp0):
        __tmp4 = {
            'n_conv': __tmp0.n_conv,
            'n_heads': __tmp0.n_heads,
            'filter_size': __tmp0.filter_size,
            'hidden_size': __tmp0.hidden_size,
            'kernel_size': __tmp0.kernel_size,
            'dropout': __tmp0.dropout,
            'layer_dropout': __tmp0.layer_dropout,
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

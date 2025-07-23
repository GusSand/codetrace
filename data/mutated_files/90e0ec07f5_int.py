
from typing import Optional
import tensorflow as tf
from tensorflow.keras import Model

from rinokeras.core.v1x.common import LayerDropoutStack, LayerDropout
from rinokeras.core.v1x.models.qanet import QANetConvBlock, QANetFeedForward, QANetSelfAttention


class QANetEncoderBlock(Model):
    """QANet Encoder Block
    """

    def __init__(__tmp1,
                 n_conv: int,
                 n_heads: <FILL>,
                 filter_size,
                 hidden_size,
                 kernel_size: int = 7,
                 dropout: Optional[float] = None,
                 layer_dropout: Optional[float] = None,
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 **kwargs) :
        super().__init__(**kwargs)

        __tmp1.n_conv = n_conv
        __tmp1.n_heads = n_heads
        __tmp1.filter_size = filter_size
        __tmp1.hidden_size = hidden_size
        __tmp1.kernel_size = kernel_size
        __tmp1.dropout = dropout
        __tmp1.layer_dropout = layer_dropout

        __tmp1.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        __tmp1.bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        __tmp1.activity_regularizer = tf.keras.regularizers.get(
            activity_regularizer)

        __tmp1.conv_stack = LayerDropoutStack([QANetConvBlock(hidden_size, kernel_size, dropout, kernel_regularizer=kernel_regularizer,
                                bias_regularizer=bias_regularizer,
                                activity_regularizer=activity_regularizer) for _ in range(n_conv)], layer_dropout=0 if layer_dropout is None else layer_dropout)
        __tmp1.self_attention = QANetSelfAttention(n_heads, dropout,
                                                 kernel_regularizer=kernel_regularizer,
                                                 bias_regularizer=bias_regularizer,
                                                 activity_regularizer=activity_regularizer)
        __tmp1.layer_drop_2 = LayerDropout(
            0 if layer_dropout is None else layer_dropout)
        __tmp1.feed_forward = QANetFeedForward(filter_size, hidden_size, dropout,
                                             kernel_regularizer=kernel_regularizer,
                                             bias_regularizer=bias_regularizer,
                                             activity_regularizer=activity_regularizer)
        __tmp1.layer_drop_3 = LayerDropout(
            0 if layer_dropout is None else layer_dropout)

    def __tmp3(__tmp1, __tmp2, mask=None):
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

        conv_out = __tmp1.conv_stack(__tmp2, mask=padding_mask) 
        res_attn = __tmp1.layer_drop_2( __tmp1.self_attention(conv_out), conv_out, mask=self_attention_mask)
        output = __tmp1.layer_drop_3(__tmp1.feed_forward(res_attn),res_attn)
        # def subcall(inputs):
        # conv_out = self.conv_stack(inputs, mask=padding_mask)
        # res_attn = self.self_attention(conv_out, mask=self_attention_mask)
        # output = self.feed_forward(res_attn)
        # return output
        # output = self.layer_drop(subcall, inputs)
        return output

    def get_config(__tmp1):
        config = {
            'n_conv': __tmp1.n_conv,
            'n_heads': __tmp1.n_heads,
            'filter_size': __tmp1.filter_size,
            'hidden_size': __tmp1.hidden_size,
            'kernel_size': __tmp1.kernel_size,
            'dropout': __tmp1.dropout,
            'layer_dropout': __tmp1.layer_dropout,
            'kernel_regularizer':
            tf.keras.regularizers.serialize(__tmp1.kernel_regularizer),
            'bias_regularizer':
            tf.keras.regularizers.serialize(__tmp1.bias_regularizer),
            'activity_regularizer':
            tf.keras.regularizers.serialize(__tmp1.activity_regularizer),
        }
        return config

    @classmethod
    def __tmp0(cls, config):
        return cls(**config)

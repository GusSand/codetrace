"""
Attention layers for the transformer model
"""

from typing import Optional

import tensorflow as tf
from tensorflow.python.keras.utils.generic_utils import serialize_keras_object

from rinokeras.core.v1x.common.attention import SelfAttention, MultiHeadAttention
from rinokeras.core.v1x.common.layers import LayerNorm


class __typ1(tf.keras.Model):

    def __init__(__tmp0,
                 n_heads,
                 dropout: Optional[float] = None,
                 key_size: Optional[int] = None,
                 use_residual_norm: bool = True,
                 kernel_initializer: Optional[tf.keras.initializers.Initializer] = 'glorot_uniform',
                 kernel_regularizer: Optional[tf.keras.regularizers.Regularizer] = None,
                 bias_regularizer : Optional[tf.keras.regularizers.Regularizer] = None,
                 activity_regularizer : Optional[tf.keras.regularizers.Regularizer] = None) :
        super().__init__()
        __tmp0.n_heads = n_heads
        __tmp0.dropout = dropout
        __tmp0.key_size = key_size
        __tmp0.norm = LayerNorm()
        __tmp0.use_residual_norm = use_residual_norm
        __tmp0.self_attention = SelfAttention(
            'scaled_dot', n_heads, dropout,
            key_size=key_size,
            kernel_initializer=kernel_initializer,
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer,
            activity_regularizer=activity_regularizer)

        __tmp0.kernel_initializer = tf.keras.initializers.get(kernel_initializer)
        __tmp0.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        __tmp0.bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        __tmp0.activity_regularizer = tf.keras.regularizers.get(activity_regularizer)

    def __tmp5(__tmp0, __tmp1, mask=None, return_attention_weights=False):
        attn_inputs = __tmp0.norm(__tmp1) if __tmp0.use_residual_norm else __tmp1
        attention, attention_weights = __tmp0.self_attention(
            attn_inputs, mask=mask, return_attention_weights=True)
        
        # Residual connection on the attention block
        output = __tmp1 + attention
        if not __tmp0.use_residual_norm:
            output = __tmp0.norm(output)

        if return_attention_weights:
            return output, attention_weights
        return output

    def __tmp2(__tmp0):
        __tmp4 = {
            'n_heads': __tmp0.n_heads,
            'dropout': __tmp0.dropout,
            'key_size': __tmp0.key_size,
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
        return __tmp4

    @classmethod
    def from_config(__tmp3, __tmp4):
        return __tmp3(**__tmp4)


class __typ0(tf.keras.Model):

    def __init__(__tmp0,
                 n_heads: <FILL>,
                 dropout: Optional[float] = None,
                 key_size: Optional[int] = None,
                 use_residual_norm: bool = True,
                 kernel_initializer: Optional[tf.keras.initializers.Initializer] = 'glorot_uniform',
                 kernel_regularizer: Optional[tf.keras.regularizers.Regularizer] = None,
                 bias_regularizer: Optional[tf.keras.regularizers.Regularizer] = None,
                 activity_regularizer:  Optional[tf.keras.regularizers.Regularizer] = None) :
        super().__init__()
        __tmp0.n_heads = n_heads
        __tmp0.dropout = dropout
        __tmp0.key_size = key_size
        __tmp0.multi_attention = MultiHeadAttention(
            'scaled_dot', n_heads, dropout,
            key_size=key_size,
            project_value=True,
            kernel_initializer=kernel_initializer,
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer,
            activity_regularizer=activity_regularizer
        )
        __tmp0.norm = LayerNorm()
        __tmp0.use_residual_norm = use_residual_norm

        __tmp0.kernel_initializer = tf.keras.initializers.get(kernel_initializer)
        __tmp0.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        __tmp0.bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        __tmp0.activity_regularizer = tf.keras.regularizers.get(activity_regularizer)

    def __tmp5(__tmp0, __tmp1, mask=None, return_attention_weights=False):
        source, target = __tmp1
        attn_inputs = __tmp0.norm(target) if __tmp0.use_residual_norm else target
        attention, attention_weights = __tmp0.multi_attention(
            (attn_inputs, source, source), mask=mask, return_attention_weights=True)

        # Residual connection on the target
        output = target + attention
        if not __tmp0.use_residual_norm:
            output = __tmp0.norm(output)

        if return_attention_weights:
            return output, attention_weights
        return output

    def __tmp2(__tmp0):
        __tmp4 = {
            'n_heads': __tmp0.n_heads,
            'dropout': __tmp0.dropout,
            'key_size': __tmp0.key_size,
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
        return __tmp4

    @classmethod
    def from_config(__tmp3, __tmp4):
        return __tmp3(**__tmp4)

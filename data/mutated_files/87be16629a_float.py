"""
Layers for handling masked inputs
"""

from typing import Optional, Dict

import tensorflow as tf
from tensorflow.keras.layers import Layer  # pylint: disable=F0401
import tensorflow.keras.backend as K  # pylint: disable=F0401


class __typ0(Layer):
    """
    Replaces some percentage of the input with a mask token. Used for
    mplementing BERT style models. This is actually slightly more complex - it 
    does one of three things

    Based on https://arxiv.org/abs/1810.04805.

    Args:
        percentage (float): Percentage of input tokens to mask
        mask_token (int): Token to replace masked input with
    """

    def __init__(__tmp0,
                 percentage: <FILL>,
                 mask_token,
                 n_symbols: Optional[int] = None,
                 *args, **kwargs) :
        super().__init__(*args, **kwargs)
        if not 0 <= percentage < 1:
            raise ValueError("Masking percentage must be in [0, 1).\
                Received {}".format(percentage))
        __tmp0.percentage = percentage
        __tmp0.mask_token = mask_token
        __tmp0.n_symbols = n_symbols

    def __tmp2(__tmp0,
             __tmp1: tf.Tensor,
             mask: Optional[tf.Tensor] = None,
             n_symbols: Optional[int] = None):
        """
        Args:
            inputs (tf.Tensor[ndims=2, int]): Tensor of values to mask
            mask (Optional[tf.Tensor[bool]]): Locations in the inputs to that are valid
                                                     (i.e. not padding, start tokens, etc.)
        Returns:
            masked_inputs (tf.Tensor[ndims=2, int]): Tensor of masked values
            bert_mask: Locations in the input that were masked
        """

        discrete = __tmp1.dtype not in [tf.float16, tf.float32, tf.float64]
        mask_shape = K.shape(__tmp1) if discrete else K.shape(__tmp1)[:-1]

        if n_symbols is None:
            n_symbols = __tmp0.n_symbols

        bert_mask = K.random_uniform(mask_shape) < __tmp0.percentage

        if mask is not None:
            bert_mask &= mask

        if not discrete:
            bert_mask = tf.expand_dims(bert_mask, -1)

        masked_inputs = __tmp1 * \
            tf.cast(~bert_mask, __tmp1.dtype)  # type: ignore

        token_bert_mask = K.random_uniform(K.shape(bert_mask)) < 0.8
        random_bert_mask = (K.random_uniform(
            K.shape(bert_mask)) < 0.1) & ~token_bert_mask
        true_bert_mask = ~token_bert_mask & ~random_bert_mask

        token_bert_mask = tf.cast(token_bert_mask & bert_mask, __tmp1.dtype)
        random_bert_mask = tf.cast(random_bert_mask & bert_mask, __tmp1.dtype)
        true_bert_mask = tf.cast(true_bert_mask & bert_mask, __tmp1.dtype)

        masked_inputs += __tmp0.mask_token * token_bert_mask  # type: ignore

        if discrete:
            assert n_symbols is not None
            masked_inputs += K.random_uniform(
                K.shape(bert_mask), 0, n_symbols, dtype=__tmp1.dtype) * random_bert_mask
        else:
            masked_inputs += (K.random_normal(K.shape(masked_inputs)
                                              ) + __tmp1) * random_bert_mask

        masked_inputs += __tmp1 * true_bert_mask

        return masked_inputs, bert_mask

    def __tmp3(__tmp0) -> Dict:
        config = {
            'percentage': __tmp0.percentage,
            'mask_token': __tmp0.mask_token
        }

        return config

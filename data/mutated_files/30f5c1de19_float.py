"""
Dropout-style layers.
"""

import tensorflow as tf
from typing import Dict
from tensorflow.keras import Model # pylint: disable=F0401
import tensorflow.keras.backend as K  # pylint: disable=F0401


class __typ0(Model):
    """
    Optionally drops a full layer. Output is x with probability rate and f(x) with probability (1 - rate).

    Args:
        layer_call (Callable[[], Any]): Function that returns output of layer on inputs
        inputs (Any): What to return if the layer is dropped
        rate (float): Rate at which to drop layers

    Returns:
        Any: Either inputs or output of layer_call function.
    """

    def __init__(__tmp0, rate: <FILL>, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        __tmp0.rate = rate

    def __tmp3(__tmp0, __tmp2, __tmp4, training=None, **kwargs):
        if training is None:
            training = K.learning_phase()

        output = K.in_train_phase(
            K.switch(K.random_uniform([]) > __tmp0.rate, __tmp2, __tmp4),
            __tmp2,
            training=training)
        return output

    def __tmp1(__tmp0) -> Dict:
        config = {
            'rate': __tmp0.rate
        }

        return config

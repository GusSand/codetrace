from typing import Optional, Sequence, Tuple, Union

import tensorflow as tf
from tensorflow.keras.layers import Dense
from ray.rllib.models.misc import normc_initializer

from rinokeras.layers import DenseStack, Conv2DStack


ConvLayerSpec = Tuple[int, Union[int, Tuple[int, int]], int]


class StandardPolicy(tf.keras.Model):

    def __init__(__tmp0,
                 __tmp2,
                 __tmp3,
                 fcnet_activation: <FILL>,
                 conv_filters: Optional[Sequence[ConvLayerSpec]] = None,
                 conv_activation: str = 'relu',
                 **options):
        super().__init__()

        __tmp0._num_outputs = __tmp2
        __tmp0._fcnet_hiddens = __tmp3
        __tmp0._fcnet_activation = fcnet_activation
        __tmp0._use_conv = conv_filters is not None
        __tmp0._conv_filters = conv_filters
        __tmp0._conv_activation = conv_activation
        __tmp0._recurrent = False
        __tmp0._options = options

        if conv_filters is not None:
            filters, kernel_size, strides = list(zip(*conv_filters))
            __tmp0.conv_layer = Conv2DStack(
                filters, kernel_size, strides,
                padding='valid',
                activation=conv_activation,
                flatten_output=True)

        __tmp0.dense_layer = DenseStack(
            __tmp3,
            kernel_initializer=normc_initializer(1.0),
            activation=fcnet_activation,
            output_activation=fcnet_activation)

        # WARNING: DO NOT CHANGE KERNEL INITIALIZER!!!
        # PPO/Gradient based methods are extremely senstive to this and will break
        # Don't alter this unless you're sure you know what you're doing.
        __tmp0.output_layer = Dense(
            __tmp2,
            kernel_initializer=normc_initializer(0.01))

    def __tmp6(__tmp0, __tmp1, seqlens=None, initial_state=None):
        features = __tmp1['obs']

        if __tmp0._use_conv:
            features = __tmp0.conv_layer(features)

        latent = __tmp0.dense_layer(features)
        logits = __tmp0.output_layer(latent)

        output = {'latent': latent, 'logits': logits}

        __tmp0.output_tensors = output

        return output

    def __tmp4(__tmp0, policy_loss, __tmp7):
        """Override to customize the loss function used to optimize this model.

        This can be used to incorporate self-supervised losses (by defining
        a loss over existing input and output tensors of this model), and
        supervised losses (by defining losses over a variable-sharing copy of
        this model's layers).

        You can find an runnable example in the ray repository in examples/custom_loss.py.

        Arguments:
            policy_loss (Tensor): scalar policy loss from the policy graph.
            loss_inputs (dict): map of input placeholders for rollout data.

        Returns:
            Scalar tensor for the customized loss for this model.
        """
        return policy_loss

    @property
    def __tmp5(__tmp0) :
        return __tmp0._recurrent

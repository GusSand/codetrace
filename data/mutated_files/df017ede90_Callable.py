from typing import Union, Callable, Tuple, Sequence, Optional

import tensorflow as tf
import tensorflow.keras.backend as K

from .RinokerasGraph import RinokerasGraph


class __typ0(RinokerasGraph):

    def __init__(__tmp1,
                 optimizer: tf.train.Optimizer,
                 loss_function: Callable,
                 grads_function: <FILL>,
                 *args,
                 **kwargs) :
        assert tf.executing_eagerly(), "Cannot use EagerGraph when not in tf eager mode."
        super(__typ0, __tmp1).__init__(*args, **kwargs)
        __tmp1.optimizer = optimizer
        __tmp1.loss_function = loss_function
        __tmp1.grads_function = grads_function
        __tmp1._default_operation: Optional[str] = None

    def __tmp2(__tmp1, ops, *args, **kwargs) :
        if ops == 'default':
            if __tmp1._default_operation is None:
                raise ValueError("No default operation in set.")
            ops = __tmp1._default_operation

        if ops == 'update':
            return __tmp1.update(*args, **kwargs)
        elif ops == 'loss':
            return __tmp1.loss(*args, **kwargs)
        else:
            raise ValueError("Unknown argument for ops: {}. \
                In eager mode, can only automatically run the update and loss ops.".format(ops))

    def update(__tmp1, *args, **kwargs) :
        """Updates the model in eager mode.

        Args:
            *args: Positional arguments to the loss function
            **kwargs: Keyword arguments to the loss function

        Returns:
            loss (Union[float, tf.Tensor]): Model loss on input batch
        """
        K.set_learning_phase(1)
        grads, loss = __tmp1.grads_function(*args, **kwargs)
        __tmp1.optimizer.apply_gradients(grads)
        return loss

    def loss(__tmp1, *args, **kwargs) :
        """Gets the loss of the model in eager mode.

        Args:
            *args: Positional arguments to the loss function
            **kwargs: Keyword arguments to the loss function

        Returns:
            loss (Union[tf.Tensor, Tuple]): Model loss on input batch
        """
        K.set_learning_phase(0)
        loss = __tmp1.loss_function(*args, **kwargs)
        return loss

    @property
    def __tmp0(__tmp1) -> Optional[str]:
        return __tmp1._default_operation

    @__tmp0.setter
    def __tmp0(__tmp1, value) -> None:
        if value not in ['update', 'loss', None]:
            raise ValueError(f"Must be one of <update, loss, None>. Received {value}")
        __tmp1._default_operation = value

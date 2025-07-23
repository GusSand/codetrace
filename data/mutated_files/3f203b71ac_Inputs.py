from typing import TypeAlias
__typ0 : TypeAlias = "Model"
__typ1 : TypeAlias = "Outputs"
from abc import ABC, abstractmethod
from typing import Optional, Tuple, Union, Callable, Sequence, List

from tensorflow.keras import Model
from tensorflow.contrib.distribute import DistributionStrategy, OneDeviceStrategy

from .train_utils import Inputs, Outputs, Losses


class __typ2(ABC):

    def __init__(__tmp1,
                 model: __typ0,
                 optimizer: str = 'adam',
                 learning_rate: Union[float, Callable[[int], float]] = 1e-3,
                 gradient_clipping: str = 'none',
                 gradient_clipping_bounds: Union[float, Tuple[float, float]] = (-1, 1),
                 return_loss_summaries: bool = False,
                 return_variable_summaries: bool = False,
                 return_grad_summaries: bool = False,
                 distribution_strategy: DistributionStrategy = OneDeviceStrategy('/gpu:0'),
                 use_memory_saving_gradients: bool = False) :
        super().__init__()
        __tmp1.model = model
        __tmp1.optimizer = optimizer
        __tmp1.learning_rate = learning_rate
        __tmp1.gradient_clipping = gradient_clipping
        __tmp1.gradient_clipping_bounds = gradient_clipping_bounds
        __tmp1.return_loss_summaries = return_loss_summaries
        __tmp1.return_variable_summaries = return_variable_summaries
        __tmp1.return_grad_summaries = return_grad_summaries
        __tmp1.distribution_strategy = distribution_strategy
        __tmp1.use_memory_saving_gradients = use_memory_saving_gradients

    @abstractmethod
    def build_model(__tmp1, __tmp2: Inputs) -> __typ1:
        return NotImplemented

    @abstractmethod
    def loss_function(__tmp1, __tmp2: <FILL>, __tmp0: __typ1) -> Losses:
        return NotImplemented

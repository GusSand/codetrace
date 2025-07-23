from typing import TypeAlias
__typ1 : TypeAlias = "Inputs"
__typ0 : TypeAlias = "Model"
__typ2 : TypeAlias = "Losses"
from abc import ABC, abstractmethod
from typing import Optional, Tuple, Union, Callable, Sequence, List

from tensorflow.keras import Model
from tensorflow.contrib.distribute import DistributionStrategy, OneDeviceStrategy

from .train_utils import Inputs, Outputs, Losses


class Experiment(ABC):

    def __init__(__tmp0,
                 model,
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
        __tmp0.model = model
        __tmp0.optimizer = optimizer
        __tmp0.learning_rate = learning_rate
        __tmp0.gradient_clipping = gradient_clipping
        __tmp0.gradient_clipping_bounds = gradient_clipping_bounds
        __tmp0.return_loss_summaries = return_loss_summaries
        __tmp0.return_variable_summaries = return_variable_summaries
        __tmp0.return_grad_summaries = return_grad_summaries
        __tmp0.distribution_strategy = distribution_strategy
        __tmp0.use_memory_saving_gradients = use_memory_saving_gradients

    @abstractmethod
    def build_model(__tmp0, __tmp1) :
        return NotImplemented

    @abstractmethod
    def loss_function(__tmp0, __tmp1, outputs: <FILL>) :
        return NotImplemented

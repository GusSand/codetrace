from typing import TypeAlias
__typ0 : TypeAlias = "Losses"
from abc import ABC, abstractmethod
from typing import Optional, Tuple, Union, Callable, Sequence, List

from tensorflow.keras import Model
from tensorflow.contrib.distribute import DistributionStrategy, OneDeviceStrategy

from .train_utils import Inputs, Outputs, Losses


class Experiment(ABC):

    def __init__(self,
                 model: Model,
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
        self.model = model
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.gradient_clipping = gradient_clipping
        self.gradient_clipping_bounds = gradient_clipping_bounds
        self.return_loss_summaries = return_loss_summaries
        self.return_variable_summaries = return_variable_summaries
        self.return_grad_summaries = return_grad_summaries
        self.distribution_strategy = distribution_strategy
        self.use_memory_saving_gradients = use_memory_saving_gradients

    @abstractmethod
    def __tmp2(self, inputs: <FILL>) :
        return NotImplemented

    @abstractmethod
    def __tmp0(self, inputs, __tmp1: Outputs) :
        return NotImplemented

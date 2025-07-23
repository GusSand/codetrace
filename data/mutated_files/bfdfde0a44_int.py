from typing import TypeAlias
__typ0 : TypeAlias = "str"
from typing import Sequence, Optional

from tensorflow.keras.layers import LSTM

from .RecurrentPolicy import RecurrentPolicy
from .StandardPolicy import ConvLayerSpec


class __typ1(RecurrentPolicy):

    def __init__(__tmp1,
                 __tmp2: <FILL>,
                 fcnet_hiddens: Sequence[int],
                 __tmp0,
                 conv_filters: Optional[Sequence[ConvLayerSpec]] = None,
                 conv_activation: __typ0 = 'relu',
                 lstm_cell_size: int = 256,
                 lstm_use_prev_action_reward: bool = False,
                 **options):
        super().__init__(
            LSTM, __tmp2, fcnet_hiddens, __tmp0,
            conv_filters, conv_activation, lstm_cell_size,
            lstm_use_prev_action_reward, recurrent_args={'use_bias': True}, **options)

from typing import TypeAlias
__typ16 : TypeAlias = "decimal"
__typ6 : TypeAlias = "PID"
import decimal

from protoactor.actor import PID


class __typ18:
    pass


class __typ20:
    pass


class __typ14:
    def __init__(__tmp1, amount, reply_to):
        __tmp1.amount = amount
        __tmp1.reply_to = reply_to


class __typ12(__typ14):
    def __init__(__tmp1, amount, reply_to):
        super().__init__(amount, reply_to)


class __typ9:
    pass


class __typ1(__typ14):
    def __init__(__tmp1, amount, reply_to):
        super().__init__(amount, reply_to)


class DebitRolledBack:
    pass


class __typ7:
    def __init__(__tmp1, __tmp0: <FILL>):
        __tmp1._message = __tmp0

    @property
    def __tmp0(__tmp1):
        return __tmp1._message

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1._message}'


class __typ4():
    def __init__(__tmp1, pid):
        __tmp1.pid = pid


class __typ8(__typ4):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class __typ17(__typ4):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class __typ19:
    pass


class InsufficientFunds:
    pass


class __typ13:
    pass


class __typ5:
    pass


class __typ2:
    pass


class __typ3:
    pass


class StatusUnknown:
    pass


class __typ11(__typ4):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class __typ0:
    def __init__(__tmp1, from_id: __typ6, from_balance: __typ16, to: __typ6, to_balance):
        __tmp1.from_id = from_id
        __tmp1.from_balance = from_balance
        __tmp1.to = to
        __tmp1.to_balance = to_balance

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.from_id.id} balance is ' \
               f'{__tmp1.from_balance}, {__tmp1.to.id} balance is {__tmp1.to_balance}'


class TransferFailed():
    def __init__(__tmp1, reason):
        __tmp1.reason = reason

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.reason}'


class __typ10:
    pass


class __typ15(__typ4):
    def __init__(__tmp1, pid):
        super().__init__(pid)

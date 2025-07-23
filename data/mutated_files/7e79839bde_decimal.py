from typing import TypeAlias
__typ8 : TypeAlias = "PID"
__typ0 : TypeAlias = "str"
import decimal

from protoactor.actor import PID


class __typ16:
    pass


class AccountDebited:
    pass


class __typ12:
    def __init__(__tmp0, amount, reply_to):
        __tmp0.amount = amount
        __tmp0.reply_to = reply_to


class __typ10(__typ12):
    def __init__(__tmp0, amount, reply_to):
        super().__init__(amount, reply_to)


class __typ18:
    pass


class Debit(__typ12):
    def __init__(__tmp0, amount: decimal, reply_to):
        super().__init__(amount, reply_to)


class DebitRolledBack:
    pass


class EscalateTransfer:
    def __init__(__tmp0, message):
        __tmp0._message = message

    @property
    def message(__tmp0):
        return __tmp0._message

    def __tmp1(__tmp0):
        return f'{__tmp0.__class__.__module__}.{__tmp0.__class__.__name__}: {__tmp0._message}'


class __typ6():
    def __init__(__tmp0, pid: __typ8):
        __tmp0.pid = pid


class FailedAndInconsistent(__typ6):
    def __init__(__tmp0, pid):
        super().__init__(pid)


class __typ15(__typ6):
    def __init__(__tmp0, pid):
        super().__init__(pid)


class __typ17:
    pass


class __typ5:
    pass


class __typ11:
    pass


class __typ7:
    pass


class __typ3:
    pass


class __typ4:
    pass


class __typ13:
    pass


class __typ9(__typ6):
    def __init__(__tmp0, pid: __typ8):
        super().__init__(pid)


class __typ1:
    def __init__(__tmp0, from_id: __typ8, from_balance, to: __typ8, to_balance: <FILL>):
        __tmp0.from_id = from_id
        __tmp0.from_balance = from_balance
        __tmp0.to = to
        __tmp0.to_balance = to_balance

    def __tmp1(__tmp0):
        return f'{__tmp0.__class__.__module__}.{__tmp0.__class__.__name__}: {__tmp0.from_id.id} balance is ' \
               f'{__tmp0.from_balance}, {__tmp0.to.id} balance is {__tmp0.to_balance}'


class __typ2():
    def __init__(__tmp0, reason: __typ0):
        __tmp0.reason = reason

    def __tmp1(__tmp0):
        return f'{__tmp0.__class__.__module__}.{__tmp0.__class__.__name__}: {__tmp0.reason}'


class TransferStarted:
    pass


class __typ14(__typ6):
    def __init__(__tmp0, pid):
        super().__init__(pid)

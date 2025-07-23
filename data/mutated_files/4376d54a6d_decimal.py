from typing import TypeAlias
__typ1 : TypeAlias = "PID"
import decimal

from protoactor.actor import PID


class AccountCredited:
    pass


class __typ13:
    pass


class __typ2:
    def __init__(__tmp1, amount, reply_to: __typ1):
        __tmp1.amount = amount
        __tmp1.reply_to = reply_to


class __typ11(__typ2):
    def __init__(__tmp1, amount: <FILL>, reply_to):
        super().__init__(amount, reply_to)


class __typ0:
    pass


class __typ4(__typ2):
    def __init__(__tmp1, amount: decimal, reply_to: __typ1):
        super().__init__(amount, reply_to)


class __typ7:
    pass


class EscalateTransfer:
    def __init__(__tmp1, __tmp0: str):
        __tmp1._message = __tmp0

    @property
    def __tmp0(__tmp1):
        return __tmp1._message

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1._message}'


class Result():
    def __init__(__tmp1, pid: __typ1):
        __tmp1.pid = pid


class __typ12(Result):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class __typ6(Result):
    def __init__(__tmp1, pid: __typ1):
        super().__init__(pid)


class __typ3:
    pass


class InsufficientFunds:
    pass


class InternalServerError:
    pass


class OK:
    pass


class __typ9:
    pass


class __typ10:
    pass


class StatusUnknown:
    pass


class SuccessResult(Result):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class TransferCompleted:
    def __init__(__tmp1, from_id: __typ1, from_balance: decimal, to: __typ1, to_balance: decimal):
        __tmp1.from_id = from_id
        __tmp1.from_balance = from_balance
        __tmp1.to = to
        __tmp1.to_balance = to_balance

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.from_id.id} balance is ' \
               f'{__tmp1.from_balance}, {__tmp1.to.id} balance is {__tmp1.to_balance}'


class __typ8():
    def __init__(__tmp1, reason: str):
        __tmp1.reason = reason

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.reason}'


class __typ5:
    pass


class UnknownResult(Result):
    def __init__(__tmp1, pid: __typ1):
        super().__init__(pid)

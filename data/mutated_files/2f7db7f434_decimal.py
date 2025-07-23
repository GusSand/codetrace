from typing import TypeAlias
__typ0 : TypeAlias = "PID"
__typ1 : TypeAlias = "str"
import decimal

from protoactor.actor import PID


class AccountCredited:
    pass


class AccountDebited:
    pass


class ChangeBalance:
    def __init__(__tmp1, amount, reply_to):
        __tmp1.amount = amount
        __tmp1.reply_to = reply_to


class Credit(ChangeBalance):
    def __init__(__tmp1, amount, reply_to):
        super().__init__(amount, reply_to)


class CreditRefused:
    pass


class Debit(ChangeBalance):
    def __init__(__tmp1, amount, reply_to):
        super().__init__(amount, reply_to)


class DebitRolledBack:
    pass


class EscalateTransfer:
    def __init__(__tmp1, __tmp0):
        __tmp1._message = __tmp0

    @property
    def __tmp0(__tmp1):
        return __tmp1._message

    def __str__(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1._message}'


class __typ5():
    def __init__(__tmp1, pid):
        __tmp1.pid = pid


class FailedAndInconsistent(__typ5):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class __typ4(__typ5):
    def __init__(__tmp1, pid: __typ0):
        super().__init__(pid)


class GetBalance:
    pass


class InsufficientFunds:
    pass


class __typ6:
    pass


class OK:
    pass


class Refused:
    pass


class ServiceUnavailable:
    pass


class StatusUnknown:
    pass


class SuccessResult(__typ5):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class __typ2:
    def __init__(__tmp1, from_id, from_balance: <FILL>, to, to_balance):
        __tmp1.from_id = from_id
        __tmp1.from_balance = from_balance
        __tmp1.to = to
        __tmp1.to_balance = to_balance

    def __str__(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.from_id.id} balance is ' \
               f'{__tmp1.from_balance}, {__tmp1.to.id} balance is {__tmp1.to_balance}'


class TransferFailed():
    def __init__(__tmp1, reason):
        __tmp1.reason = reason

    def __str__(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.reason}'


class __typ3:
    pass


class UnknownResult(__typ5):
    def __init__(__tmp1, pid):
        super().__init__(pid)

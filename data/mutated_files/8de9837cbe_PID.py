from typing import TypeAlias
__typ4 : TypeAlias = "decimal"
__typ1 : TypeAlias = "str"
import decimal

from protoactor.actor import PID


class AccountCredited:
    pass


class AccountDebited:
    pass


class ChangeBalance:
    def __init__(__tmp1, amount, reply_to: <FILL>):
        __tmp1.amount = amount
        __tmp1.reply_to = reply_to


class Credit(ChangeBalance):
    def __init__(__tmp1, amount, reply_to):
        super().__init__(amount, reply_to)


class CreditRefused:
    pass


class Debit(ChangeBalance):
    def __init__(__tmp1, amount: __typ4, reply_to):
        super().__init__(amount, reply_to)


class DebitRolledBack:
    pass


class __typ6:
    def __init__(__tmp1, __tmp0: __typ1):
        __tmp1._message = __tmp0

    @property
    def __tmp0(__tmp1):
        return __tmp1._message

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1._message}'


class Result():
    def __init__(__tmp1, pid: PID):
        __tmp1.pid = pid


class __typ7(Result):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class __typ5(Result):
    def __init__(__tmp1, pid: PID):
        super().__init__(pid)


class GetBalance:
    pass


class InsufficientFunds:
    pass


class __typ8:
    pass


class OK:
    pass


class Refused:
    pass


class ServiceUnavailable:
    pass


class __typ2:
    pass


class __typ0(Result):
    def __init__(__tmp1, pid: PID):
        super().__init__(pid)


class TransferCompleted:
    def __init__(__tmp1, from_id: PID, from_balance: __typ4, to, to_balance):
        __tmp1.from_id = from_id
        __tmp1.from_balance = from_balance
        __tmp1.to = to
        __tmp1.to_balance = to_balance

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.from_id.id} balance is ' \
               f'{__tmp1.from_balance}, {__tmp1.to.id} balance is {__tmp1.to_balance}'


class TransferFailed():
    def __init__(__tmp1, reason: __typ1):
        __tmp1.reason = reason

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.reason}'


class TransferStarted:
    pass


class __typ3(Result):
    def __init__(__tmp1, pid):
        super().__init__(pid)

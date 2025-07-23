from typing import TypeAlias
__typ8 : TypeAlias = "decimal"
__typ4 : TypeAlias = "str"
import decimal

from protoactor.actor import PID


class __typ3:
    pass


class __typ13:
    pass


class ChangeBalance:
    def __init__(__tmp1, amount, reply_to):
        __tmp1.amount = amount
        __tmp1.reply_to = reply_to


class Credit(ChangeBalance):
    def __init__(__tmp1, amount: __typ8, reply_to: PID):
        super().__init__(amount, reply_to)


class CreditRefused:
    pass


class __typ5(ChangeBalance):
    def __init__(__tmp1, amount, reply_to):
        super().__init__(amount, reply_to)


class DebitRolledBack:
    pass


class __typ10:
    def __init__(__tmp1, __tmp0):
        __tmp1._message = __tmp0

    @property
    def __tmp0(__tmp1):
        return __tmp1._message

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1._message}'


class Result():
    def __init__(__tmp1, pid: PID):
        __tmp1.pid = pid


class FailedAndInconsistent(Result):
    def __init__(__tmp1, pid: PID):
        super().__init__(pid)


class __typ9(Result):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class __typ12:
    pass


class __typ11:
    pass


class __typ14:
    pass


class __typ1:
    pass


class Refused:
    pass


class __typ2:
    pass


class StatusUnknown:
    pass


class __typ0(Result):
    def __init__(__tmp1, pid: <FILL>):
        super().__init__(pid)


class TransferCompleted:
    def __init__(__tmp1, from_id, from_balance, to, to_balance):
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


class __typ6:
    pass


class __typ7(Result):
    def __init__(__tmp1, pid):
        super().__init__(pid)

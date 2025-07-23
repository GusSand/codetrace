from typing import TypeAlias
__typ9 : TypeAlias = "decimal"
__typ3 : TypeAlias = "str"
import decimal

from protoactor.actor import PID


class __typ2:
    pass


class AccountDebited:
    pass


class __typ4:
    def __init__(__tmp1, amount, reply_to: PID):
        __tmp1.amount = amount
        __tmp1.reply_to = reply_to


class __typ12(__typ4):
    def __init__(__tmp1, amount, reply_to):
        super().__init__(amount, reply_to)


class CreditRefused:
    pass


class __typ5(__typ4):
    def __init__(__tmp1, amount: __typ9, reply_to):
        super().__init__(amount, reply_to)


class DebitRolledBack:
    pass


class EscalateTransfer:
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
    def __init__(__tmp1, pid):
        super().__init__(pid)


class FailedButConsistentResult(Result):
    def __init__(__tmp1, pid: PID):
        super().__init__(pid)


class GetBalance:
    pass


class __typ13:
    pass


class __typ14:
    pass


class __typ1:
    pass


class Refused:
    pass


class __typ11:
    pass


class StatusUnknown:
    pass


class __typ0(Result):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class __typ6:
    def __init__(__tmp1, from_id: PID, from_balance, to: <FILL>, to_balance):
        __tmp1.from_id = from_id
        __tmp1.from_balance = from_balance
        __tmp1.to = to
        __tmp1.to_balance = to_balance

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.from_id.id} balance is ' \
               f'{__tmp1.from_balance}, {__tmp1.to.id} balance is {__tmp1.to_balance}'


class __typ10():
    def __init__(__tmp1, reason: __typ3):
        __tmp1.reason = reason

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.reason}'


class __typ7:
    pass


class __typ8(Result):
    def __init__(__tmp1, pid):
        super().__init__(pid)

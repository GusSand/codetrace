from typing import TypeAlias
__typ9 : TypeAlias = "decimal"
__typ4 : TypeAlias = "str"
import decimal

from protoactor.actor import PID


class AccountCredited:
    pass


class AccountDebited:
    pass


class __typ3:
    def __init__(__tmp1, amount, reply_to):
        __tmp1.amount = amount
        __tmp1.reply_to = reply_to


class __typ14(__typ3):
    def __init__(__tmp1, amount, reply_to: PID):
        super().__init__(amount, reply_to)


class __typ13:
    pass


class __typ6(__typ3):
    def __init__(__tmp1, amount: __typ9, reply_to):
        super().__init__(amount, reply_to)


class __typ11:
    pass


class __typ2:
    def __init__(__tmp1, __tmp0):
        __tmp1._message = __tmp0

    @property
    def __tmp0(__tmp1):
        return __tmp1._message

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1._message}'


class __typ16():
    def __init__(__tmp1, pid):
        __tmp1.pid = pid


class __typ1(__typ16):
    def __init__(__tmp1, pid: <FILL>):
        super().__init__(pid)


class __typ10(__typ16):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class __typ5:
    pass


class __typ15:
    pass


class __typ17:
    pass


class OK:
    pass


class Refused:
    pass


class ServiceUnavailable:
    pass


class StatusUnknown:
    pass


class __typ0(__typ16):
    def __init__(__tmp1, pid: PID):
        super().__init__(pid)


class __typ7:
    def __init__(__tmp1, from_id: PID, from_balance, to: PID, to_balance):
        __tmp1.from_id = from_id
        __tmp1.from_balance = from_balance
        __tmp1.to = to
        __tmp1.to_balance = to_balance

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.from_id.id} balance is ' \
               f'{__tmp1.from_balance}, {__tmp1.to.id} balance is {__tmp1.to_balance}'


class __typ12():
    def __init__(__tmp1, reason):
        __tmp1.reason = reason

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.reason}'


class TransferStarted:
    pass


class __typ8(__typ16):
    def __init__(__tmp1, pid):
        super().__init__(pid)

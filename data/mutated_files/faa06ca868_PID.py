from typing import TypeAlias
__typ17 : TypeAlias = "decimal"
__typ0 : TypeAlias = "str"
import decimal

from protoactor.actor import PID


class __typ19:
    pass


class __typ10:
    pass


class __typ14:
    def __init__(__tmp1, amount, reply_to: PID):
        __tmp1.amount = amount
        __tmp1.reply_to = reply_to


class Credit(__typ14):
    def __init__(__tmp1, amount: __typ17, reply_to: PID):
        super().__init__(amount, reply_to)


class __typ21:
    pass


class __typ2(__typ14):
    def __init__(__tmp1, amount: __typ17, reply_to: <FILL>):
        super().__init__(amount, reply_to)


class DebitRolledBack:
    pass


class __typ8:
    def __init__(__tmp1, __tmp0: __typ0):
        __tmp1._message = __tmp0

    @property
    def __tmp0(__tmp1):
        return __tmp1._message

    def __str__(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1._message}'


class __typ6():
    def __init__(__tmp1, pid: PID):
        __tmp1.pid = pid


class __typ9(__typ6):
    def __init__(__tmp1, pid: PID):
        super().__init__(pid)


class __typ18(__typ6):
    def __init__(__tmp1, pid: PID):
        super().__init__(pid)


class __typ20:
    pass


class InsufficientFunds:
    pass


class __typ13:
    pass


class __typ7:
    pass


class __typ4:
    pass


class __typ5:
    pass


class __typ15:
    pass


class __typ12(__typ6):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class __typ1:
    def __init__(__tmp1, from_id: PID, from_balance: __typ17, to: PID, to_balance: __typ17):
        __tmp1.from_id = from_id
        __tmp1.from_balance = from_balance
        __tmp1.to = to
        __tmp1.to_balance = to_balance

    def __str__(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.from_id.id} balance is ' \
               f'{__tmp1.from_balance}, {__tmp1.to.id} balance is {__tmp1.to_balance}'


class __typ3():
    def __init__(__tmp1, reason: __typ0):
        __tmp1.reason = reason

    def __str__(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.reason}'


class __typ11:
    pass


class __typ16(__typ6):
    def __init__(__tmp1, pid: PID):
        super().__init__(pid)

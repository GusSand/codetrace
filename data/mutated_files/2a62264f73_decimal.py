from typing import TypeAlias
__typ9 : TypeAlias = "PID"
__typ0 : TypeAlias = "str"
import decimal

from protoactor.actor import PID


class __typ18:
    pass


class __typ12:
    pass


class __typ16:
    def __init__(__tmp0, amount, reply_to):
        __tmp0.amount = amount
        __tmp0.reply_to = reply_to


class Credit(__typ16):
    def __init__(__tmp0, amount, reply_to: __typ9):
        super().__init__(amount, reply_to)


class __typ20:
    pass


class __typ2(__typ16):
    def __init__(__tmp0, amount: <FILL>, reply_to: __typ9):
        super().__init__(amount, reply_to)


class __typ14:
    pass


class __typ10:
    def __init__(__tmp0, message):
        __tmp0._message = message

    @property
    def message(__tmp0):
        return __tmp0._message

    def __tmp1(__tmp0):
        return f'{__tmp0.__class__.__module__}.{__tmp0.__class__.__name__}: {__tmp0._message}'


class __typ7():
    def __init__(__tmp0, pid):
        __tmp0.pid = pid


class __typ11(__typ7):
    def __init__(__tmp0, pid):
        super().__init__(pid)


class FailedButConsistentResult(__typ7):
    def __init__(__tmp0, pid):
        super().__init__(pid)


class __typ19:
    pass


class __typ6:
    pass


class InternalServerError:
    pass


class __typ8:
    pass


class __typ4:
    pass


class __typ5:
    pass


class StatusUnknown:
    pass


class __typ15(__typ7):
    def __init__(__tmp0, pid: __typ9):
        super().__init__(pid)


class __typ1:
    def __init__(__tmp0, from_id, from_balance: decimal, to, to_balance):
        __tmp0.from_id = from_id
        __tmp0.from_balance = from_balance
        __tmp0.to = to
        __tmp0.to_balance = to_balance

    def __tmp1(__tmp0):
        return f'{__tmp0.__class__.__module__}.{__tmp0.__class__.__name__}: {__tmp0.from_id.id} balance is ' \
               f'{__tmp0.from_balance}, {__tmp0.to.id} balance is {__tmp0.to_balance}'


class __typ3():
    def __init__(__tmp0, reason):
        __tmp0.reason = reason

    def __tmp1(__tmp0):
        return f'{__tmp0.__class__.__module__}.{__tmp0.__class__.__name__}: {__tmp0.reason}'


class __typ13:
    pass


class __typ17(__typ7):
    def __init__(__tmp0, pid):
        super().__init__(pid)

from typing import TypeAlias
__typ9 : TypeAlias = "PID"
__typ0 : TypeAlias = "str"
import decimal

from protoactor.actor import PID


class __typ5:
    pass


class AccountDebited:
    pass


class __typ16:
    def __init__(self, amount: <FILL>, reply_to: __typ9):
        self.amount = amount
        self.reply_to = reply_to


class __typ14(__typ16):
    def __init__(self, amount: decimal, reply_to: __typ9):
        super().__init__(amount, reply_to)


class __typ19:
    pass


class __typ1(__typ16):
    def __init__(self, amount, reply_to):
        super().__init__(amount, reply_to)


class DebitRolledBack:
    pass


class __typ10:
    def __init__(self, __tmp0):
        self._message = __tmp0

    @property
    def __tmp0(self):
        return self._message

    def __str__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}: {self._message}'


class __typ7():
    def __init__(self, pid: __typ9):
        self.pid = pid


class __typ11(__typ7):
    def __init__(self, pid):
        super().__init__(pid)


class __typ18(__typ7):
    def __init__(self, pid: __typ9):
        super().__init__(pid)


class GetBalance:
    pass


class __typ6:
    pass


class __typ15:
    pass


class __typ8:
    pass


class __typ3:
    pass


class __typ4:
    pass


class __typ20:
    pass


class __typ13(__typ7):
    def __init__(self, pid: __typ9):
        super().__init__(pid)


class TransferCompleted:
    def __init__(self, from_id, from_balance, to, to_balance):
        self.from_id = from_id
        self.from_balance = from_balance
        self.to = to
        self.to_balance = to_balance

    def __str__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}: {self.from_id.id} balance is ' \
               f'{self.from_balance}, {self.to.id} balance is {self.to_balance}'


class __typ2():
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}: {self.reason}'


class __typ12:
    pass


class __typ17(__typ7):
    def __init__(self, pid: __typ9):
        super().__init__(pid)

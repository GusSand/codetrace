from typing import TypeAlias
__typ1 : TypeAlias = "str"
import decimal

from protoactor.actor import PID


class AccountCredited:
    pass


class AccountDebited:
    pass


class ChangeBalance:
    def __init__(self, amount, reply_to):
        self.amount = amount
        self.reply_to = reply_to


class Credit(ChangeBalance):
    def __init__(self, amount, reply_to):
        super().__init__(amount, reply_to)


class CreditRefused:
    pass


class Debit(ChangeBalance):
    def __init__(self, amount, reply_to):
        super().__init__(amount, reply_to)


class DebitRolledBack:
    pass


class EscalateTransfer:
    def __init__(self, message):
        self._message = message

    @property
    def message(self):
        return self._message

    def __str__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}: {self._message}'


class __typ2():
    def __init__(self, pid):
        self.pid = pid


class FailedAndInconsistent(__typ2):
    def __init__(self, pid):
        super().__init__(pid)


class FailedButConsistentResult(__typ2):
    def __init__(self, pid):
        super().__init__(pid)


class GetBalance:
    pass


class InsufficientFunds:
    pass


class InternalServerError:
    pass


class OK:
    pass


class __typ0:
    pass


class ServiceUnavailable:
    pass


class StatusUnknown:
    pass


class SuccessResult(__typ2):
    def __init__(self, pid):
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


class TransferFailed():
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}: {self.reason}'


class TransferStarted:
    pass


class UnknownResult(__typ2):
    def __init__(self, pid: <FILL>):
        super().__init__(pid)

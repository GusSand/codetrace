import decimal

from protoactor.actor import PID


class AccountCredited:
    pass


class AccountDebited:
    pass


class ChangeBalance:
    def __init__(__tmp1, amount: decimal, reply_to: PID):
        __tmp1.amount = amount
        __tmp1.reply_to = reply_to


class Credit(ChangeBalance):
    def __init__(__tmp1, amount: decimal, reply_to: PID):
        super().__init__(amount, reply_to)


class CreditRefused:
    pass


class Debit(ChangeBalance):
    def __init__(__tmp1, amount: decimal, reply_to: PID):
        super().__init__(amount, reply_to)


class DebitRolledBack:
    pass


class __typ0:
    def __init__(__tmp1, __tmp0: str):
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


class FailedButConsistentResult(Result):
    def __init__(__tmp1, pid: PID):
        super().__init__(pid)


class __typ1:
    pass


class InsufficientFunds:
    pass


class InternalServerError:
    pass


class OK:
    pass


class Refused:
    pass


class ServiceUnavailable:
    pass


class StatusUnknown:
    pass


class SuccessResult(Result):
    def __init__(__tmp1, pid):
        super().__init__(pid)


class TransferCompleted:
    def __init__(__tmp1, from_id: <FILL>, from_balance: decimal, to: PID, to_balance: decimal):
        __tmp1.from_id = from_id
        __tmp1.from_balance = from_balance
        __tmp1.to = to
        __tmp1.to_balance = to_balance

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.from_id.id} balance is ' \
               f'{__tmp1.from_balance}, {__tmp1.to.id} balance is {__tmp1.to_balance}'


class TransferFailed():
    def __init__(__tmp1, reason: str):
        __tmp1.reason = reason

    def __tmp2(__tmp1):
        return f'{__tmp1.__class__.__module__}.{__tmp1.__class__.__name__}: {__tmp1.reason}'


class TransferStarted:
    pass


class UnknownResult(Result):
    def __init__(__tmp1, pid: PID):
        super().__init__(pid)

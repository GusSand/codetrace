import decimal

from protoactor.actor import PID


class AccountCredited:
    pass


class __typ2:
    pass


class __typ1:
    def __init__(__tmp0, amount, reply_to):
        __tmp0.amount = amount
        __tmp0.reply_to = reply_to


class Credit(__typ1):
    def __init__(__tmp0, amount: decimal, reply_to: <FILL>):
        super().__init__(amount, reply_to)


class CreditRefused:
    pass


class Debit(__typ1):
    def __init__(__tmp0, amount, reply_to):
        super().__init__(amount, reply_to)


class DebitRolledBack:
    pass


class EscalateTransfer:
    def __init__(__tmp0, message):
        __tmp0._message = message

    @property
    def message(__tmp0):
        return __tmp0._message

    def __tmp1(__tmp0):
        return f'{__tmp0.__class__.__module__}.{__tmp0.__class__.__name__}: {__tmp0._message}'


class Result():
    def __init__(__tmp0, pid):
        __tmp0.pid = pid


class FailedAndInconsistent(Result):
    def __init__(__tmp0, pid):
        super().__init__(pid)


class FailedButConsistentResult(Result):
    def __init__(__tmp0, pid):
        super().__init__(pid)


class GetBalance:
    pass


class InsufficientFunds:
    pass


class InternalServerError:
    pass


class OK:
    pass


class Refused:
    pass


class __typ0:
    pass


class StatusUnknown:
    pass


class SuccessResult(Result):
    def __init__(__tmp0, pid: PID):
        super().__init__(pid)


class TransferCompleted:
    def __init__(__tmp0, from_id, from_balance, to, to_balance: decimal):
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


class TransferStarted:
    pass


class UnknownResult(Result):
    def __init__(__tmp0, pid):
        super().__init__(pid)

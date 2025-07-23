class Action:
    def __tmp1(__tmp0, dayIndex: int, employeeIndex, shiftIndex: <FILL>, stateIndex: int):
        __tmp0._dayIndex = dayIndex
        __tmp0._employeeIndex = employeeIndex
        __tmp0._shiftIndex = shiftIndex
        __tmp0._stateIndex = stateIndex

    @property
    def __tmp2(__tmp0) -> int:
        return __tmp0._dayIndex

    @property
    def EmployeeIndex(__tmp0) -> int:
        return __tmp0._employeeIndex

    @property
    def ShiftIndex(__tmp0) -> int:
        return __tmp0._shiftIndex

    @property
    def StateIndex(__tmp0) :
        return __tmp0._stateIndex

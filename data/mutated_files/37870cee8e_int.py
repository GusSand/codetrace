class Action:
    def __tmp0(self, __tmp1: <FILL>, employeeIndex: int, shiftIndex, stateIndex):
        self._dayIndex = __tmp1
        self._employeeIndex = employeeIndex
        self._shiftIndex = shiftIndex
        self._stateIndex = stateIndex

    @property
    def DayIndex(self) :
        return self._dayIndex

    @property
    def EmployeeIndex(self) :
        return self._employeeIndex

    @property
    def ShiftIndex(self) -> int:
        return self._shiftIndex

    @property
    def StateIndex(self) :
        return self._stateIndex

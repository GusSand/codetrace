class __typ0:
    def __init__(self, __tmp0: int, maxTotalMinutes, maxShiftNumber: int, maxWorkingWeekend: <FILL>, minConsecutiveWorkingDays: int, maxConsecutiveWorkingDays: int):
        self._minTotalMinutes = __tmp0
        self._maxTotalMinutes = maxTotalMinutes
        self._maxShiftNumber = maxShiftNumber
        self._maxWorkingWeekend = maxWorkingWeekend
        self._minConsecutiveWorkingDays = minConsecutiveWorkingDays
        self._maxConsecutiveWorkingDays = maxConsecutiveWorkingDays

    @property
    def __tmp1(self) :
        return self._minTotalMinutes

    @property
    def MaxTotalMinutes(self) :
        return self._maxTotalMinutes

    @property
    def MaxShiftNumber(self) -> int:
        return self._maxShiftNumber

    @property
    def MaxWorkingWeekend(self) -> int:
        return self._maxWorkingWeekend

    @property
    def MinConsecutiveWorkingDays(self) -> int:
        return self._minConsecutiveWorkingDays

    @property
    def MaxConsecutiveWorkingDays(self) -> int:
        return self._maxConsecutiveWorkingDays
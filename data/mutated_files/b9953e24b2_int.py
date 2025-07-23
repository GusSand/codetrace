from person import Person
from workSchedule import WorkSchedule
from typing import List

class __typ0:
    def __tmp4(__tmp0, __tmp2: <FILL>, __tmp5: int):
        __tmp0._dayCount = __tmp2
        __tmp0._employees = __tmp0._createEmployees(__tmp5)
        __tmp0._demandCounts = __tmp0._createDemandCounts(2)

    def reset(__tmp0):
        for employee in __tmp0._employees:
            employee.reset()

    def _createEmployees(__tmp0, __tmp3: int) :
        workSchedule = WorkSchedule(3360, 4320, 14, 1, 2, 5)

        persons = []

        for i in range(0, __tmp3):
            persons.append(Person(i, workSchedule, [3]))
        
        return persons

    def _createDemandCounts(__tmp0, __tmp6: int) :
        demandCountsOnDays = []

        for i in range(__tmp0._dayCount):
            demandCountsOnDays.append(__tmp6)

        return demandCountsOnDays

    def calculateDemandPenalty(__tmp0) :
        penalty = 0

        for dayIndex in range(0, __tmp0._dayCount):
            assignmentsOnDay = sum(e.hasAssignmentOnDay(dayIndex) for e in __tmp0._employees)
            demandsOnDay = __tmp0._demandCounts[dayIndex]
            diff = demandsOnDay - assignmentsOnDay
            penalty += diff * 100 if diff > 0 else -1 * diff * 100

        return penalty

    @property
    def __tmp2(__tmp0) -> int:
        return __tmp0._dayCount

    @property
    def __tmp1(__tmp0) :
        return __tmp0._employees

    @property
    def __tmp7(__tmp0) -> List[int]:
        return __tmp0._demandCounts
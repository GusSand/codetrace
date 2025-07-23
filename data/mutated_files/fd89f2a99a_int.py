from person import Person
from workSchedule import WorkSchedule
from typing import List

class __typ0:
    def __tmp3(__tmp1, __tmp2: int, __tmp4):
        __tmp1._dayCount = __tmp2
        __tmp1._employees = __tmp1._createEmployees(__tmp4)
        __tmp1._demandCounts = __tmp1._createDemandCounts(2)

    def reset(__tmp1):
        for employee in __tmp1._employees:
            employee.reset()

    def _createEmployees(__tmp1, count) :
        workSchedule = WorkSchedule(3360, 4320, 14, 1, 2, 5)

        persons = []

        for i in range(0, count):
            persons.append(Person(i, workSchedule, [3]))
        
        return persons

    def _createDemandCounts(__tmp1, __tmp5: <FILL>) :
        demandCountsOnDays = []

        for i in range(__tmp1._dayCount):
            demandCountsOnDays.append(__tmp5)

        return demandCountsOnDays

    def __tmp0(__tmp1) :
        penalty = 0

        for dayIndex in range(0, __tmp1._dayCount):
            assignmentsOnDay = sum(e.hasAssignmentOnDay(dayIndex) for e in __tmp1._employees)
            demandsOnDay = __tmp1._demandCounts[dayIndex]
            diff = demandsOnDay - assignmentsOnDay
            penalty += diff * 100 if diff > 0 else -1 * diff * 100

        return penalty

    @property
    def __tmp2(__tmp1) -> int:
        return __tmp1._dayCount

    @property
    def employees(__tmp1) -> List[Person]:
        return __tmp1._employees

    @property
    def __tmp6(__tmp1) -> List[int]:
        return __tmp1._demandCounts
from person import Person
from workSchedule import WorkSchedule
from typing import List

class __typ0:
    def __init__(__tmp1, __tmp2, employeeCount: <FILL>):
        __tmp1._dayCount = __tmp2
        __tmp1._employees = __tmp1._createEmployees(employeeCount)
        __tmp1._demandCounts = __tmp1._createDemandCounts(2)

    def reset(__tmp1):
        for employee in __tmp1._employees:
            employee.reset()

    def _createEmployees(__tmp1, __tmp3: int) :
        workSchedule = WorkSchedule(3360, 4320, 14, 1, 2, 5)

        persons = []

        for i in range(0, __tmp3):
            persons.append(Person(i, workSchedule, [3]))
        
        return persons

    def _createDemandCounts(__tmp1, __tmp4) :
        demandCountsOnDays = []

        for i in range(__tmp1._dayCount):
            demandCountsOnDays.append(__tmp4)

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
    def employees(__tmp1) :
        return __tmp1._employees

    @property
    def demandCounts(__tmp1) :
        return __tmp1._demandCounts
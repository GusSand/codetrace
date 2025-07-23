from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
from typing import List
import numpy as np
from action import Action
from schedulingModel import SchedulingModel
from person import Person

class AddOnlyEnvironment:
    def __init__(__tmp1):
        __tmp1._model = SchedulingModel(3, 3)
        
        __tmp1._state = __tmp1._createState()
        __tmp1._actions = __tmp1._createActions()
        __tmp1._dayStartIndexes = __tmp1._calculateDayStartIndexes()

    def _createState(__tmp1) -> np.ndarray:
        return np.negative(np.ones(sum(__tmp1._model.demandCounts)))

    def _createActions(__tmp1) -> List[Action]:
        actions = []
        demandCountsSoFar = 0

        for dayIndex in range(0, __tmp1._model.dayCount):
            for employeeIndex in range(0, len(__tmp1._model.employees)):
                for demandIndex in range(0, __tmp1._model.demandCounts[dayIndex]):
                    actions.append(Action(dayIndex, employeeIndex, 0, demandCountsSoFar + demandIndex))
            
            demandCountsSoFar += __tmp1._model.demandCounts[dayIndex]

        return actions

    def _calculateDayStartIndexes(__tmp1) -> List[__typ1]:
        employeeCount = len(__tmp1._model.employees)
        dayStartIndexes = [0]

        for day in range(1, __tmp1._model.dayCount):
            previousDayStartIndex = dayStartIndexes[day - 1]
            demandCountOnPreviousDay = __tmp1._model.demandCounts[day - 1]
            dayStartIndexes.append(previousDayStartIndex + demandCountOnPreviousDay * employeeCount)

        return dayStartIndexes

    def reset(__tmp1) -> List[__typ1]:
        __tmp1._state = __tmp1._createState()
        __tmp1._model.reset()
        return __tmp1._state

    def __tmp0(__tmp1, __tmp2: __typ1) -> (list, __typ1, bool, dict):
        __tmp5 = __tmp1._calculateReward(__tmp2)
        __tmp1._setState(__tmp2)
        next_state = __tmp1._state
        done = __tmp1._isDone(__tmp5)

        return (next_state, __tmp5, done, {})

    def _calculateReward(__tmp1, __tmp2: __typ1) :
        action = __tmp1._actions[__tmp2]

        if __tmp1._state[action.StateIndex] != -1:
            previousEmployee = __tmp1._model.employees[__typ1(__tmp1._state[action.StateIndex])]
            previousEmployee.removeShift(action)

        __tmp6 = __tmp1._model.employees[action.EmployeeIndex]
        hasAssignmentOnDay = __tmp6.hasAssignmentOnDay(action.DayIndex)
        __tmp6.applyAction(action)
        
        __tmp5 = 0

        if hasAssignmentOnDay:
            __tmp5 -= 10000

        # if employee.TotalWorkedMinutes < employee.WorkSchedule.MinTotalMinutes:
        #     return -1000

        # if employee.TotalWorkedMinutes > employee.WorkSchedule.MaxTotalMinutes:
        #     return -1000

        # if employee.ShiftCount > employee.WorkSchedule.MaxShiftNumber:
        #     return -1000

        # if add and employee.isDayOff(action.DayIndex):
        #     return -1000

        # if employee.WorkingWeekendCount > employee.WorkSchedule.MaxWorkingWeekend:
        #     return -1000

        # if employee.ConsecutiveWorkingDays < employee.WorkSchedule.MinConsecutiveWorkingDays:
        #     return -1000

        # if employee.ConsecutiveWorkingDays > employee.WorkSchedule.MaxConsecutiveWorkingDays:
        #     return -1000

        __tmp5 -= __tmp1._model.calculateDemandPenalty()

        return __tmp5

    def _isDone(__tmp1, __tmp5):
        # if self._assignmentCount == len(self._state):
        #     return True

        # for dayIndex in range(0, self._model.dayCount):
        #     assignmentCountOnDay = self._countAssignmentsOnDay(dayIndex)

        #     if assignmentCountOnDay < self._model.demandCounts[dayIndex]:
        #         return False

        #     if assignmentCountOnDay > self._model.demandCounts[dayIndex]:
        #         return False

        # return True
        return __tmp5 == 0

    def _setState(__tmp1, __tmp2: __typ1):
        action = __tmp1._actions[__tmp2]
        
        __tmp1._state[action.StateIndex] = action.EmployeeIndex

    def __tmp4(__tmp1) -> __typ0:
        return ''.join('{}\r\n'.format(__tmp1._employeeShiftsToRosterString(e)) for e in __tmp1._model.employees)

    def _employeeShiftsToRosterString(__tmp1, __tmp6: <FILL>) -> __typ0:
        return ''.join(('{}\t'.format('D') if dayIndex in __tmp6.Shifts else '\t') for dayIndex in range(0, __tmp1._model.dayCount))

    @property
    def __tmp3(__tmp1) -> __typ1:
        return len(__tmp1._state)

    @property
    def __tmp7(__tmp1) -> __typ1:
        return len(__tmp1._actions)

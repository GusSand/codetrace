from typing import TypeAlias
__typ2 : TypeAlias = "Person"
__typ1 : TypeAlias = "str"
from typing import List
import numpy as np
from action import Action
from schedulingModel import SchedulingModel
from person import Person

class __typ0:
    def __init__(__tmp2):
        __tmp2._model = SchedulingModel(3, 3)
        
        __tmp2._state = __tmp2._createState()
        __tmp2._actions = __tmp2._createActions()
        __tmp2._dayStartIndexes = __tmp2._calculateDayStartIndexes()

    def _createState(__tmp2) :
        return np.negative(np.ones(sum(__tmp2._model.demandCounts)))

    def _createActions(__tmp2) :
        actions = []
        demandCountsSoFar = 0

        for dayIndex in range(0, __tmp2._model.dayCount):
            for employeeIndex in range(0, len(__tmp2._model.employees)):
                for demandIndex in range(0, __tmp2._model.demandCounts[dayIndex]):
                    actions.append(Action(dayIndex, employeeIndex, 0, demandCountsSoFar + demandIndex))
            
            demandCountsSoFar += __tmp2._model.demandCounts[dayIndex]

        return actions

    def _calculateDayStartIndexes(__tmp2) :
        employeeCount = len(__tmp2._model.employees)
        dayStartIndexes = [0]

        for day in range(1, __tmp2._model.dayCount):
            previousDayStartIndex = dayStartIndexes[day - 1]
            demandCountOnPreviousDay = __tmp2._model.demandCounts[day - 1]
            dayStartIndexes.append(previousDayStartIndex + demandCountOnPreviousDay * employeeCount)

        return dayStartIndexes

    def reset(__tmp2) :
        __tmp2._state = __tmp2._createState()
        __tmp2._model.reset()
        return __tmp2._state

    def step(__tmp2, __tmp0) :
        __tmp1 = __tmp2._calculateReward(__tmp0)
        __tmp2._setState(__tmp0)
        next_state = __tmp2._state
        done = __tmp2._isDone(__tmp1)

        return (next_state, __tmp1, done, {})

    def _calculateReward(__tmp2, __tmp0) -> int:
        action = __tmp2._actions[__tmp0]

        if __tmp2._state[action.StateIndex] != -1:
            previousEmployee = __tmp2._model.employees[int(__tmp2._state[action.StateIndex])]
            previousEmployee.removeShift(action)

        employee = __tmp2._model.employees[action.EmployeeIndex]
        hasAssignmentOnDay = employee.hasAssignmentOnDay(action.DayIndex)
        employee.applyAction(action)
        
        __tmp1 = 0

        if hasAssignmentOnDay:
            __tmp1 -= 10000

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

        __tmp1 -= __tmp2._model.calculateDemandPenalty()

        return __tmp1

    def _isDone(__tmp2, __tmp1):
        # if self._assignmentCount == len(self._state):
        #     return True

        # for dayIndex in range(0, self._model.dayCount):
        #     assignmentCountOnDay = self._countAssignmentsOnDay(dayIndex)

        #     if assignmentCountOnDay < self._model.demandCounts[dayIndex]:
        #         return False

        #     if assignmentCountOnDay > self._model.demandCounts[dayIndex]:
        #         return False

        # return True
        return __tmp1 == 0

    def _setState(__tmp2, __tmp0: <FILL>):
        action = __tmp2._actions[__tmp0]
        
        __tmp2._state[action.StateIndex] = action.EmployeeIndex

    def toRosterViewerFormat(__tmp2) -> __typ1:
        return ''.join('{}\r\n'.format(__tmp2._employeeShiftsToRosterString(e)) for e in __tmp2._model.employees)

    def _employeeShiftsToRosterString(__tmp2, employee) :
        return ''.join(('{}\t'.format('D') if dayIndex in employee.Shifts else '\t') for dayIndex in range(0, __tmp2._model.dayCount))

    @property
    def num_states(__tmp2) :
        return len(__tmp2._state)

    @property
    def num_actions(__tmp2) :
        return len(__tmp2._actions)

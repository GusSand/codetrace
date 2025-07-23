from typing import TypeAlias
__typ1 : TypeAlias = "Person"
__typ0 : TypeAlias = "str"
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

    def _calculateDayStartIndexes(__tmp1) -> List[int]:
        employeeCount = len(__tmp1._model.employees)
        dayStartIndexes = [0]

        for day in range(1, __tmp1._model.dayCount):
            previousDayStartIndex = dayStartIndexes[day - 1]
            demandCountOnPreviousDay = __tmp1._model.demandCounts[day - 1]
            dayStartIndexes.append(previousDayStartIndex + demandCountOnPreviousDay * employeeCount)

        return dayStartIndexes

    def reset(__tmp1) -> List[int]:
        __tmp1._state = __tmp1._createState()
        __tmp1._model.reset()
        return __tmp1._state

    def step(__tmp1, __tmp0: <FILL>) -> (list, int, bool, dict):
        reward = __tmp1._calculateReward(__tmp0)
        __tmp1._setState(__tmp0)
        next_state = __tmp1._state
        done = __tmp1._isDone(reward)

        return (next_state, reward, done, {})

    def _calculateReward(__tmp1, __tmp0: int) -> int:
        action = __tmp1._actions[__tmp0]

        if __tmp1._state[action.StateIndex] != -1:
            previousEmployee = __tmp1._model.employees[int(__tmp1._state[action.StateIndex])]
            previousEmployee.removeShift(action)

        employee = __tmp1._model.employees[action.EmployeeIndex]
        hasAssignmentOnDay = employee.hasAssignmentOnDay(action.DayIndex)
        employee.applyAction(action)
        
        reward = 0

        if hasAssignmentOnDay:
            reward -= 10000

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

        reward -= __tmp1._model.calculateDemandPenalty()

        return reward

    def _isDone(__tmp1, reward):
        # if self._assignmentCount == len(self._state):
        #     return True

        # for dayIndex in range(0, self._model.dayCount):
        #     assignmentCountOnDay = self._countAssignmentsOnDay(dayIndex)

        #     if assignmentCountOnDay < self._model.demandCounts[dayIndex]:
        #         return False

        #     if assignmentCountOnDay > self._model.demandCounts[dayIndex]:
        #         return False

        # return True
        return reward == 0

    def _setState(__tmp1, __tmp0: int):
        action = __tmp1._actions[__tmp0]
        
        __tmp1._state[action.StateIndex] = action.EmployeeIndex

    def toRosterViewerFormat(__tmp1) -> __typ0:
        return ''.join('{}\r\n'.format(__tmp1._employeeShiftsToRosterString(e)) for e in __tmp1._model.employees)

    def _employeeShiftsToRosterString(__tmp1, employee) -> __typ0:
        return ''.join(('{}\t'.format('D') if dayIndex in employee.Shifts else '\t') for dayIndex in range(0, __tmp1._model.dayCount))

    @property
    def num_states(__tmp1) -> int:
        return len(__tmp1._state)

    @property
    def num_actions(__tmp1) -> int:
        return len(__tmp1._actions)

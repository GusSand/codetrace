from typing import TypeAlias
__typ0 : TypeAlias = "VmState"
__typ1 : TypeAlias = "bool"
"""Module with jump-related operations implementation."""

import typing

from interpreter.src.virtual_machine.vm.vm_def import (
    VmState,
    VM_OPERATION_TO_BYTECODE
)
from interpreter.src.virtual_machine.vm.helpers import vm_operation


def generate_jump(jmp_name: <FILL>, __tmp4: typing.Callable):
    """Generate function for conditional jumps.

    Every jump work as explained above:

        Example:
            LABEL abc
            CMP 3, 7
            JMP_NE abc

        Jump will work only if compare operation before set NE register to True

    :param str jump_name: Name of jump operation for checks and exceptions

    :param cond: Function around VmState wich checks NE, EQ, GT, LT registers
    :type cond: Callable[[VmState], bool]

    :return: Generated function for jumps
    :rtype: Callable
    """
    @vm_operation
    def __tmp1(__tmp3, *args, op_bytecode=None, **kwargs) -> __typ0:
        op_code, _, arg1, _, _ = op_bytecode

        assert VM_OPERATION_TO_BYTECODE[op_code] == jmp_name

        label_index = arg1

        if label_index not in __tmp3.vm_labels:
            raise Exception(f"Bad label {label_index}")

        if __tmp4(__tmp3):
            __tmp3.vm_code_pointer = __tmp3.vm_labels[label_index]

        return __tmp3

    # Need for easy debugging
    __tmp1.__name__ = f"vm_{jmp_name.lower()}"

    return __tmp1


# Jumps
vm_jmp = generate_jump("JMP", lambda _: True)
vm_jump_eq = generate_jump("JMP_EQ", lambda __tmp2: __tmp2.vm_registers[5].value)
vm_jump_lt = generate_jump("JMP_LT", lambda __tmp2: __tmp2.vm_registers[6].value)
vm_jump_gt = generate_jump("JMP_GT", lambda __tmp2: __tmp2.vm_registers[7].value)
vm_jump_ne = generate_jump("JMP_NE", lambda __tmp2: __tmp2.vm_registers[8].value)


def set_called_subroutine(__tmp2: __typ0) -> __typ1:
    """Set subroutine call."""
    __tmp2.vm_call_stack.append(__tmp2.vm_code_pointer)

    return True


vm_call = generate_jump("CALL", set_called_subroutine)


@vm_operation
def __tmp5(__tmp3: __typ0, *args, op_bytecode=None, **kwargs) -> __typ0:
    op_code, _, _, _, _ = op_bytecode

    assert VM_OPERATION_TO_BYTECODE[op_code] == "RET"

    try:
        previuous_routine = __tmp3.vm_call_stack.pop()
    except IndexError:
        raise Exception("Bad RET before CALL.")

    __tmp3.vm_code_pointer = previuous_routine

    return __tmp3


@vm_operation
def vm_label(__tmp3: __typ0, *args, op_bytecode=None, **kwargs) -> __typ0:
    """LABEL operation for virtual machine."""
    op_code, _, arg1, _, _ = op_bytecode

    assert VM_OPERATION_TO_BYTECODE[op_code] == "LABEL"

    label_index = arg1
    label_position = __tmp3.vm_code_pointer

    if label_index not in __tmp3.vm_labels:
        __tmp3.vm_labels[label_index] = label_position

    return __tmp3


@vm_operation
def vm_cmp(__tmp3: __typ0, *args, op_bytecode=None, **kwargs) -> __typ0:
    """CMP operation for virtual machine."""
    op_code, arg1_type, arg1, arg2_type, arg2 = op_bytecode

    assert VM_OPERATION_TO_BYTECODE[op_code] == "CMP"

    if arg2_type == 2:  # Register
        right_value = __tmp3.vm_registers[arg2].value

    elif arg2_type == 3:  # Register pointer
        input_value_addr = __tmp3.vm_registers[arg2].value
        right_value = __tmp3.vm_memory[input_value_addr]

    elif arg2_type == 4:  # In-place value
        right_value = arg2

    else:
        raise Exception(f"Bad argument for CMP")

    if arg1_type == 2:  # Register
        left_value = __tmp3.vm_registers[arg1].value

    elif arg1_type == 3:  # RegisterPointer
        mem_index = __tmp3.vm_registers[arg1].value
        left_value = __tmp3.vm_memory[mem_index]

    elif arg1_type == 4:  # In-place value
        left_value = arg1

    else:
        raise Exception(f"Bad argument on CMP")

    if left_value > right_value:
        __tmp3.vm_registers[7].value = True
        __tmp3.vm_registers[8].value = True
    elif left_value < right_value:
        __tmp3.vm_registers[6].value = True
        __tmp3.vm_registers[8].value = True
    elif left_value == right_value:
        __tmp3.vm_registers[5].value = True
        __tmp3.vm_registers[6].value = False
        __tmp3.vm_registers[7].value = False
        __tmp3.vm_registers[8].value = False

    return __tmp3


@vm_operation
def vm_nop(__tmp3: __typ0, *args, op_bytecode=None, **kwargs) -> __typ0:
    """NOP operation for virtual machine."""
    op_code, _, _, _, _ = op_bytecode

    # assert VM_OPERATION_TO_BYTECODE[op_code] == "NOP"

    return __tmp3


@vm_operation
def __tmp0(__tmp3: __typ0, *args, op_bytecode=None, **kwargs) -> __typ0:
    """END operation for virtual machine."""
    op_code, _, _, _, _ = op_bytecode

    assert VM_OPERATION_TO_BYTECODE[op_code] == "END"

    last_code_addr = __tmp3.vm_code_pointer

    end_pointer = len(__tmp3.vm_code_buffer.read1())

    __tmp3.vm_code_pointer = last_code_addr + end_pointer

    return __tmp3

from typing import TypeAlias
__typ0 : TypeAlias = "Visitor"
__typ1 : TypeAlias = "str"
from typing import cast
from parser.VMParser import VMParser
from parser.VMVisitor import VMVisitor
from .Generator import Generator


class __typ0(VMVisitor):
    def __tmp6(__tmp0, generator: <FILL>):
        __tmp0.generator = generator

    # Visit a parse tree produced by VMParser#program.
    def __tmp7(__tmp0, __tmp11) -> __typ1:
        return __tmp0.visitStatements(__tmp11.statements())

    # Visit a parse tree produced by VMParser#statements.
    def visitStatements(__tmp0, __tmp11: VMParser.StatementsContext) -> __typ1:
        instructions = [__tmp0.visit(child) for child in __tmp11.getChildren()]
        return "\n".join(instructions) + "\n"

    # Visit a parse tree produced by VMParser#statement.
    def __tmp8(__tmp0, __tmp11) :
        return cast(__typ1, __tmp0.visitChildren(__tmp11))

    # Visit a parse tree produced by VMParser#push.
    def visitPush(__tmp0, __tmp11) -> __typ1:
        segment = __tmp11.segment().getText()
        i = __tmp11.INT().getText()
        comment = f"// push {segment} {i}\n"

        if segment == "constant":
            return comment + __tmp0.generator.push_constant(i)
        elif segment == "static":
            return comment + __tmp0.generator.push_static(i)
        elif segment == "pointer":
            return comment + __tmp0.generator.push_pointer(i)
        elif segment == "temp":
            return comment + __tmp0.generator.push_temp(i)
        elif segment in __tmp0.generator.hack_segment_labels:
            return comment + __tmp0.generator.push_segment(segment, i)
        else:
            raise ValueError(f'unexpected segment value: "{segment}"')

    # Visit a parse tree produced by VMParser#pop.
    def __tmp9(__tmp0, __tmp11: VMParser.PopContext) -> __typ1:
        segment = __tmp11.segment().getText()
        i = __tmp11.INT().getText()
        comment = f"// pop {segment} {i}\n"

        if segment == "temp":
            return comment + __tmp0.generator.pop_temp(i)
        elif segment == "pointer":
            return comment + __tmp0.generator.pop_pointer(i)
        elif segment == "static":
            return comment + __tmp0.generator.pop_static(i)
        elif segment in __tmp0.generator.hack_segment_labels:
            return comment + __tmp0.generator.pop_segment(segment, i)
        else:
            raise ValueError(f'unexpected segment value: "{segment}"')

    # Visit a parse tree produced by VMParser#arithmetic.
    def visitArithmetic(__tmp0, __tmp11: VMParser.ArithmeticContext) :
        operation = __tmp11.getText()
        comment = f"// {operation}\n"

        if operation == "add":
            return comment + __tmp0.generator.add()
        elif operation == "sub":
            return comment + __tmp0.generator.sub()
        elif operation == "neg":
            return comment + __tmp0.generator.neg()
        else:
            raise ValueError(f'unexpected arithmetic value: "{operation}"')

    # Visit a parse tree produced by VMParser#logical.
    def __tmp3(__tmp0, __tmp11: VMParser.LogicalContext) -> __typ1:
        operator = __tmp11.getText()
        comment = f"// {operator}\n"

        if operator == "not":
            return comment + __tmp0.generator.logical_not()
        elif operator in __tmp0.generator.comparison_operators:
            return comment + __tmp0.generator.comparison_operator(operator)
        elif operator == "and":
            return comment + __tmp0.generator.logical_and()
        elif operator == "or":
            return comment + __tmp0.generator.logical_or()
        else:
            raise ValueError(f'Unexpected logical operation "{operator}"')

    # Visit a parse tree produced by VMParser#label.
    def __tmp1(__tmp0, __tmp11: VMParser.LabelContext) -> __typ1:
        label = __tmp11.labelIdentifier().getText()
        comment = f"// label {label}\n"

        return comment + __tmp0.generator.label(label)

    # Visit a parse tree produced by VMParser#goto.
    def __tmp5(__tmp0, __tmp11) :
        label = __tmp11.labelIdentifier().getText()
        comment = f"// goto {label}\n"

        return comment + __tmp0.generator.goto(label)

    # Visit a parse tree produced by VMParser#ifGoto.
    def __tmp10(__tmp0, __tmp11) -> __typ1:
        label = __tmp11.labelIdentifier().getText()
        comment = f"// if-goto {label}\n"

        return comment + __tmp0.generator.if_goto(label)

    # Visit a parse tree produced by VMParser#call.
    def visitCall(__tmp0, __tmp11) :
        name = __tmp11.functionName().getText()
        argument_count = int(__tmp11.argumentCount().getText())
        comment = f"// call {name} {argument_count}\n"

        return comment + __tmp0.generator.call(name, argument_count)

    # Visit a parse tree produced by VMParser#function.
    def __tmp4(__tmp0, __tmp11: VMParser.FunctionContext) -> __typ1:
        name = __tmp11.functionName().getText()
        local_variable_count = int(__tmp11.localVariableCount().getText())
        comment = f"// function {name} {local_variable_count}\n"

        return comment + __tmp0.generator.function(name, local_variable_count)

    # Visit a parse tree produced by VMParser#returnStatement.
    def __tmp2(__tmp0, __tmp11) :
        comment = "// return\n"

        return comment + __tmp0.generator.return_statement()

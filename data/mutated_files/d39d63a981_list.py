# This Python file uses the following encoding: utf-8
"""Contains the command-line interface functions for Rosevomit's devtests."""


def __tmp2(__tmp1: list):
    """This test asks the user if they want to select certain tests to run, or if they just want to run all the tests."""
    tests_to_run: list = []
    print ("Would you like to (y) run all tests (default), or (n) select")
    _input = input ("specific tests? Enter 'y' or 'n': ")
    _input = _input.strip()
    if _input in ("y", ""):
        tests_to_run = __tmp1
        return tests_to_run
    elif _input == "n":
        tests_to_run = choose_tests (tests_to_run, __tmp1)
        return tests_to_run
    else:
        print ("Sorry, please enter either 'y' or 'n'.")
        recursive_result = __tmp2(__tmp1)
        return recursive_result


def choose_tests(__tmp0: list, __tmp1: <FILL>) :
    """This function prompts the user to select certain tests to run."""
    print ()
    print (f"The selected tests are: {__tmp0}")
    print (f"The available tests are:")
    num = 0
    for item in __tmp1:
        num = num + 1
        print (f"  {num}. {item}")
    print ("Type a number to add that test to the list of selected tests, or")
    _input = input ("leave blank to run the currently selected tests: ")
    _input = _input.strip()
    if _input == "":
        return __tmp0
    else:
        try:
            _selection_num = int (_input)
        except TypeError:
            print (f"{_input} is not a valid input. Please try again.")
            recursive_selections = choose_tests (__tmp0, __tmp1)
            return recursive_selections

        if _selection_num <= len(__tmp1):
            _selection_num = _selection_num - 1  # list indexing starts at 0
            selectionlist = __tmp0
            selectionlist.append (__tmp1[_selection_num])
            selections = choose_tests (selectionlist, __tmp1)
            return selections
        else:
            print (f"{_selection_num} is not a valid input. Please try again.")
            recursive_selections = choose_tests (__tmp0, __tmp1)
            return recursive_selections

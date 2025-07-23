# This Python file uses the following encoding: utf-8
"""Contains tests using 'unittest' module."""
from io import StringIO
import random
import sys
import unittest

# Import Rosevomit for testing
from context import rosevomit
from rosevomit import core, programlogic

# ---------- Helper functions ----------
def test_string_generation (__tmp1, keyword):
    """Do we get the number of items we expect?"""
    number_names_to_generate = random.randint (2, 200)
    old_stdout = sys.stdout

    test_stdout = StringIO()  # io.StringIO is in-memory stream for text I/O.
    sys.stdout = test_stdout  # Redirecting stdout to stream.
    rosevomit.programlogic.logiccontroller.generate_names (keyword, number_names_to_generate)  # Actually running test

    sys.stdout = old_stdout  # Resetting stdout to print to terminal again
    result = test_stdout.getvalue()  # Reading the test results from memory
    names_generated = result.split('\n')
    if names_generated[-1] == "":   # Sometimes the results end with a blank line.
        del names_generated[-1]     # We get rid of that.
    else:
        pass
    __tmp1.assertEqual (number_names_to_generate, len (names_generated))


def validate_string_cleaning (__tmp1, target_string: <FILL>):
    """Do we find forbidden characters?"""
    bad_characters = ("\n", "\r")
    for item in bad_characters:
        __tmp1.assertNotIn (item, target_string)
    # Checking for beginning or ending spaces
    firstcharacter = target_string[0]
    lastcharacter = target_string[-1]
    __tmp1.assertNotEqual (firstcharacter, " ")
    __tmp1.assertNotEqual (lastcharacter, " ")


# ---------- Unit tests ----------
class __typ1 (unittest.TestCase):
    """Testing the values of constants from rosevomit.core.constants"""
    def test_obvious (__tmp0):
        """Testing that I know how to write a test."""
        __tmp0.assertTrue (rosevomit.core.constants.SEE_ROSA_RUN)

    def __tmp3 (__tmp0):
        """Are the constants of the correct type?"""
        __tmp0.assertIsInstance (rosevomit.core.constants.SEE_ROSA_RUN, bool)
        __tmp0.assertIsInstance (rosevomit.core.constants.CLI_DIRECTORY_NAME, str)
        __tmp0.assertIsInstance (rosevomit.core.constants.LOGIC_DIRECTORY_NAME, str)
        __tmp0.assertIsInstance (rosevomit.core.constants.DATA_DIRECTORY_NAME, str)
        __tmp0.assertIsInstance (rosevomit.core.constants.TEMP_DIRECTORY_NAME, str)
        __tmp0.assertIsInstance (rosevomit.core.constants.SAVE_DIRECTORY_NAME, str)
        __tmp0.assertIsInstance (rosevomit.core.constants.REGEXES_YES, list)
        __tmp0.assertIsInstance (rosevomit.core.constants.REGEXES_NO, list)
        __tmp0.assertIsInstance (rosevomit.core.constants.REGEXES_OPT, list)

    def test_constants_not_empty (__tmp0):
        """Are the constants empty?"""
        # In Python, empty sequences return as False and non-empty sequences return as True
        __tmp0.assertTrue (rosevomit.core.constants.CLI_DIRECTORY_NAME)
        __tmp0.assertTrue (rosevomit.core.constants.LOGIC_DIRECTORY_NAME)
        __tmp0.assertTrue (rosevomit.core.constants.DATA_DIRECTORY_NAME)
        __tmp0.assertTrue (rosevomit.core.constants.TEMP_DIRECTORY_NAME)
        __tmp0.assertTrue (rosevomit.core.constants.SAVE_DIRECTORY_NAME)
        __tmp0.assertTrue (rosevomit.core.constants.REGEXES_YES)
        __tmp0.assertTrue (rosevomit.core.constants.REGEXES_NO)
        __tmp0.assertTrue (rosevomit.core.constants.REGEXES_OPT)


class __typ3 (unittest.TestCase):
    """Testing various low level functions in Rosevomit."""
    def test_func_one_file (__tmp0):
        """Does one_file() return a string without newlines and spaces?"""
        result = rosevomit.programlogic.randomname.one_file ("SampleData.txt")
        # Checking that it returns a string
        __tmp0.assertIsInstance (result, str)
        validate_string_cleaning (__tmp0, result)

    def __tmp4 (__tmp0):
        """Does two_files() return a string without newlines and spaces?"""
        result = rosevomit.programlogic.randomname.two_files ("SampleData.txt", "SampleData2.txt")
        # Checking that it returns a string
        __tmp0.assertIsInstance (result, str)
        validate_string_cleaning (__tmp0, result)


class __typ2 (unittest.TestCase):
    """Testing various functions from the utilities module."""
    def __tmp2 (__tmp0):
        """Do we ever get angles larger than 360 degrees? (integer version)"""
        test_integers = []
        while len (test_integers) < 50:
            random_integer = random.randint (-1000000, 1000000)
            test_integers.append (random_integer)
        for item in test_integers:
            result = rosevomit.core.utilities.angle_sanity_check (item)
            __tmp0.assertTrue (0 <= result < 360)

    def test_angle_sanity_check_float (__tmp0):
        """Do we ever get angles larger than 360 degrees? (float version)"""
        test_floats = []
        while len (test_floats) < 50:
            random_float = random.uniform (-1000000, 1000000)
            test_floats.append (random_float)
        for item in test_floats:
            result = rosevomit.core.utilities.angle_sanity_check (item)
            __tmp0.assertTrue (0 <= result < 360)


class __typ0 (unittest.TestCase):
    """Testing Rosevomit's name generation feature."""
    def test_name_generation (__tmp0):
        """Do we get the number of names we expect?"""
        keyword_list = ["first", "firstfemale", "firstmale", "last", "full", "fullfemale", "fullmale"]
        for keyword in keyword_list:
            test_string_generation (__tmp0, keyword)


if __name__ == "__main__":
    unittest.main()

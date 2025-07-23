from typing import TypeAlias
__typ0 : TypeAlias = "bool"
__typ1 : TypeAlias = "Test"
__typ2 : TypeAlias = "RegressionTest"
"""Contain function for updating the outputs of regression test with latest CCExtractor version."""


import os
import subprocess
from time import gmtime, strftime
from typing import List

from database import create_session
from mod_regression.models import RegressionTest
from run import config

INPUT_VIDEO_FOLDER = os.path.join(config.get('SAMPLE_REPOSITORY', ''), 'TestFiles')
OUTPUT_RESULTS_FOLDER = os.path.join(config.get('SAMPLE_REPOSITORY', ''), 'TestResults')
LOG_DIR = os.path.join(os.path.expanduser('~'), 'sampleplatform_sample_update_logs')


class __typ1:
    """Object to hold all test details and get methods."""

    def __tmp6(__tmp1, __tmp4: str, args: str, output: str) -> None:
        __tmp1.input = __tmp4
        __tmp1.args = args
        __tmp1.output = output

    @staticmethod
    def get_inputfilepath(__tmp2) -> str:
        """
        Get absolute input video path from RegressionTest entry.

        :param reg_test: regression test
        :type reg_test: RegressionTest
        :return: absolute file path of the input file
        :rtype: str
        """
        file_name = __tmp2.sample.filename
        file_path = os.path.join(INPUT_VIDEO_FOLDER, file_name)
        abs_file_path = os.path.abspath(file_path)

        return abs_file_path

    @staticmethod
    def get_outputfilepath(__tmp2) -> str:
        """
        Get absolute output captions path from RegressionTest entry.

        :param reg_test: regression test
        :type reg_test: RegressionTest
        :return: absolute file path of the output file
        :rtype: str
        """
        output = __tmp2.output_files[0]
        file_name = output.filename_correct
        file_path = os.path.join(OUTPUT_RESULTS_FOLDER, file_name)
        abs_file_path = os.path.abspath(file_path)

        return abs_file_path

    @staticmethod
    def run_ccex(__tmp5, __tmp7: str, __tmp4, args: str, __tmp3) -> __typ0:
        """
        Run ccextractor in a subprocess in a synchronous manner.

        :param path_to_ccex: path to the latest ccextractor executable
        :type path_to_ccex: str
        :param log_file: absolute path to the log file where ccextractor output is saved
        :type log_file: str
        :param input_file: absolute path to the input file
        :type input_file: str
        :param args: arguments for ccextractor
        :type args: str
        :param output_file: absolute path to the output file
        :type output_file: str
        :return: True if successful, False otherwise
        :rtype: bool
        """
        proc_args = [__tmp5]
        proc_args.extend(list(args.split(' ')))
        proc_args.append(__tmp4)
        proc_args.extend(['-o', __tmp3])

        try:
            proc = subprocess.run(proc_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            with open(__tmp7, 'w+') as logf:
                logf.write(proc.stdout.decode('utf-8'))
            if proc.returncode != 0:
                print(f'ERROR: ccextractor encountered error for {__tmp4}, please see {__tmp7}')
                print(f'ccextractor was run as {" ".join(proc_args)}')
                return False
            return True
        except subprocess.CalledProcessError as err:
            print(f'ERROR: subprocess failed for {__tmp4}')
            print(f'ERROR: The run for subprocess was "{" ".join(proc_args)}"')
            return False


def __tmp0(__tmp5: <FILL>) :
    """
    Update expected result in the regression.

    :param path_to_ccex: path to the ccextractor executable
    :type path_to_ccex: str
    """
    DBSession = create_session(config['DATABASE_URI'])

    if not os.path.isfile(__tmp5):
        return False

    all_regression_tests = DBSession.query(__typ2).all()

    tests_to_update = []

    if len(all_regression_tests) == 0:
        print('INFO: No regression tests found!')
        return True

    for test in all_regression_tests:
        __tmp4 = __typ1.get_inputfilepath(test)
        __tmp3 = __typ1.get_outputfilepath(test)
        args = test.command

        tests_to_update.append(__typ1(
            __tmp4,
            args,
            __tmp3
        ))

    log_folder_name = strftime("%Y_%m_%dT%H_%M_%SZ", gmtime())
    log_folder_path = os.path.join(LOG_DIR, log_folder_name)
    os.makedirs(log_folder_path, exist_ok=True)
    print(f'INFO: ccextractor logs can be found at {log_folder_path} for each sample after update')

    for test in tests_to_update:
        __tmp7 = os.path.join(log_folder_path, os.path.basename(test.input) + '.log')
        success = __typ1.run_ccex(__tmp5, __tmp7, test.input, test.args, test.output)
        if success:
            print(f'SUCCESS: output {__tmp3} updated for sample {__tmp4}')
    return True

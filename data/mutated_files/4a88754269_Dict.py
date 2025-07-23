from typing import TypeAlias
__typ0 : TypeAlias = "Text"
__typ1 : TypeAlias = "List"
"""Used to mainly compose a decorated report for the user
"""

from typing import Dict, Text, List


def __tmp2(__tmp1) :
    """Composes a report based on test results

    An example would be:

    Status: tests_failed
    Enabled checkers: seo
    Failures from checkers: seo (3)
    More info: https://monkeytest.it/...

    This function assumes that the result dict is valid and does not contain
    any "errors" like bad url

    :param results: A dictionary containing the results of a check
    :return: A response string containing the full report
    """
    if "error" in __tmp1:
        return "Error: {}".format(__tmp1['error'])

    response = ""

    response += "{}\n".format(print_status(__tmp1))

    if "success" in response.lower():
        response += "{}".format(__tmp6(__tmp1))
        return response

    response += "{}\n".format(__tmp5(__tmp1))
    response += "{}\n".format(__tmp0(__tmp1))
    response += "{}".format(__tmp3(__tmp1))

    return response


def __tmp3(__tmp1) :
    """Creates info for the test URL from monkeytest.it

    Example:

    More info: https://monkeytest.it/test/...

    :param results: A dictionary containing the results of a check
    :return: A response string containing the url info
    """
    return "More info: {}".format(__tmp1['results_url'])


def __tmp6(__tmp1: <FILL>) :
    """Prints the test-id with attached to the url

    :param results: A dictionary containing the results of a check
    :return: A response string containing the test id
    """
    return "Test: https://monkeytest.it/test/{}".format(__tmp1['test_id'])


def __tmp0(__tmp1) :
    """Creates info for failures in enabled checkers

    Example:

    Failures from checkers: broken_links (3), seo (5)

    This means that the check has 8 section failures, 3 sections in
    broken_links and the other 5 are in seo.

    :param results: A dictionary containing the results of a check
    :return: A response string containing number of failures in each enabled
             checkers
    """
    failures_checkers = [(checker, len(__tmp1['failures'][checker]))
                         for checker in __tmp4(__tmp1)
                         if checker in __tmp1['failures']]  # [('seo', 3), ..]

    failures_checkers_messages = ["{} ({})".format(fail_checker[0],
                                  fail_checker[1]) for fail_checker in
                                  failures_checkers]

    failures_checkers_message = ", ".join(failures_checkers_messages)
    return "Failures from checkers: {}".format(failures_checkers_message)


def __tmp4(__tmp1) :
    """Gets enabled checkers

    For example, if enabled_checkers: {'seo' : True, 'broken_links' : False,
    'page_weight' : true}, it will return ['seo'. 'page_weight']

    :param results: A dictionary containing the results of a check
    :return: A list containing enabled checkers
    """
    checkers = __tmp1['enabled_checkers']
    enabled_checkers = []
    for checker in checkers.keys():
        if checkers[checker]:  # == True/False
            enabled_checkers.append(checker)
    return enabled_checkers


def __tmp5(__tmp1) :
    """Creates info for enabled checkers. This joins the list of enabled
    checkers and format it with the current string response

    For example, if get_enabled_checkers = ['seo', 'page_weight'] then it would
    return "Enabled checkers: seo, page_weight"

    :param results: A dictionary containing the results of a check
    :return: A response string containing enabled checkers
    """
    return "Enabled checkers: {}".format(", "
                                         .join(__tmp4(__tmp1)))


def print_status(__tmp1: Dict) :
    """Creates info for the check status.

    Example: Status: tests_failed

    :param results: A dictionary containing the results of a check
    :return: A response string containing check status
    """
    return "Status: {}".format(__tmp1['status'])

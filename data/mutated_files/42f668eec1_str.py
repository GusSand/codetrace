import re
from typing import Dict

# Warning: If you change this parsing, please test using
#   zerver/tests/test_decorators.py
# And extend zerver/tests/fixtures/user_agents_unique with any new test cases
def __tmp0(user_agent: <FILL>) -> Dict[str, str]:
    match = re.match("^(?P<name>[^/ ]*[^0-9/(]*)(/(?P<version>[^/ ]*))?([ /].*)?$", user_agent)
    assert match is not None
    return match.groupdict()

from typing import TypeAlias
__typ0 : TypeAlias = "type"
# Set of helper functions to manipulate the OpenAPI files that define our REST
# API's specification.
import os
from typing import Any, Dict, List, Optional

OPENAPI_SPEC_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    '../openapi/zulip.yaml'))

# A list of exceptions we allow when running validate_against_openapi_schema.
# The validator will ignore these keys when they appear in the "content"
# passed.
EXCLUDE_PROPERTIES = {
    '/register': {
        'post': {
            '200': ['max_message_id', 'realm_emoji']
        }
    }
}

class __typ1():
    def __tmp7(__tmp1, path: str) :
        __tmp1.path = path
        __tmp1.last_update = None  # type: Optional[float]
        __tmp1.data = None

    def reload(__tmp1) -> None:
        # Because importing yamole (and in turn, yaml) takes
        # significant time, and we only use python-yaml for our API
        # docs, importing it lazily here is a significant optimization
        # to `manage.py` startup.
        #
        # There is a bit of a race here...we may have two processes
        # accessing this module level object and both trying to
        # populate self.data at the same time.  Hopefully this will
        # only cause some extra processing at startup and not data
        # corruption.
        from yamole import YamoleParser
        with open(__tmp1.path) as f:
            yaml_parser = YamoleParser(f)

        __tmp1.data = yaml_parser.data
        __tmp1.last_update = os.path.getmtime(__tmp1.path)

    def spec(__tmp1) -> Dict[str, Any]:
        """Reload the OpenAPI file if it has been modified after the last time
        it was read, and then return the parsed data.
        """
        last_modified = os.path.getmtime(__tmp1.path)
        # Using != rather than < to cover the corner case of users placing an
        # earlier version than the current one
        if __tmp1.last_update != last_modified:
            __tmp1.reload()
        assert(__tmp1.data)
        return __tmp1.data

class __typ2(Exception):
    pass

openapi_spec = __typ1(OPENAPI_SPEC_PATH)

def __tmp5(__tmp10: str, __tmp2: <FILL>,
                        __tmp4: Optional[str]='200') :
    """Fetch a fixture from the full spec object.
    """
    return (openapi_spec.spec()['paths'][__tmp10][__tmp2.lower()]['responses']
            [__tmp4]['content']['application/json']['schema']
            ['example'])

def __tmp0(__tmp10,
                           __tmp2: str) -> List[Dict[str, Any]]:
    return (openapi_spec.spec()['paths'][__tmp10][__tmp2.lower()]['parameters'])

def __tmp9(__tmp6: Dict[str, Any], __tmp10: str,
                                    __tmp2: str, __tmp4: str) -> None:
    """Compare a "content" dict with the defined schema for a specific method
    in an endpoint.
    """
    schema = (openapi_spec.spec()['paths'][__tmp10][__tmp2.lower()]['responses']
              [__tmp4]['content']['application/json']['schema'])

    exclusion_list = (EXCLUDE_PROPERTIES.get(__tmp10, {}).get(__tmp2, {})
                                        .get(__tmp4, []))

    for key, value in __tmp6.items():
        # Ignore in the validation the keys in EXCLUDE_PROPERTIES
        if key in exclusion_list:
            continue

        # Check that the key is defined in the schema
        if key not in schema['properties']:
            raise __typ2('Extraneous key "{}" in the response\'s '
                              'content'.format(key))

        # Check that the types match
        expected_type = __tmp8(schema['properties'][key]['type'])
        actual_type = __typ0(value)
        if expected_type is not actual_type:
            raise __typ2('Expected type {} for key "{}", but actually '
                              'got {}'.format(expected_type, key, actual_type))

    # Check that at least all the required keys are present
    for req_key in schema['required']:
        if req_key not in __tmp6.keys():
            raise __typ2('Expected to find the "{}" required key')

def __tmp8(__tmp3: str) :
    """Transform an OpenAPI-like type to a Pyton one.
    https://swagger.io/docs/specification/data-models/data-types
    """
    TYPES = {
        'string': str,
        'number': float,
        'integer': int,
        'boolean': bool,
        'array': list,
        'object': dict
    }

    return TYPES[__tmp3]

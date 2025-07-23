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

class OpenAPISpec():
    def __tmp4(__tmp0, path) :
        __tmp0.path = path
        __tmp0.last_update = None  # type: Optional[float]
        __tmp0.data = None

    def reload(__tmp0) :
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
        with open(__tmp0.path) as f:
            yaml_parser = YamoleParser(f)

        __tmp0.data = yaml_parser.data
        __tmp0.last_update = os.path.getmtime(__tmp0.path)

    def spec(__tmp0) -> Dict[str, Any]:
        """Reload the OpenAPI file if it has been modified after the last time
        it was read, and then return the parsed data.
        """
        last_modified = os.path.getmtime(__tmp0.path)
        # Using != rather than < to cover the corner case of users placing an
        # earlier version than the current one
        if __tmp0.last_update != last_modified:
            __tmp0.reload()
        assert(__tmp0.data)
        return __tmp0.data

class SchemaError(Exception):
    pass

openapi_spec = OpenAPISpec(OPENAPI_SPEC_PATH)

def __tmp2(__tmp6, __tmp1,
                        response: Optional[str]='200') :
    """Fetch a fixture from the full spec object.
    """
    return (openapi_spec.spec()['paths'][__tmp6][__tmp1.lower()]['responses']
            [response]['content']['application/json']['schema']
            ['example'])

def get_openapi_parameters(__tmp6,
                           __tmp1) :
    return (openapi_spec.spec()['paths'][__tmp6][__tmp1.lower()]['parameters'])

def __tmp5(content, __tmp6,
                                    __tmp1: str, response: str) :
    """Compare a "content" dict with the defined schema for a specific method
    in an endpoint.
    """
    schema = (openapi_spec.spec()['paths'][__tmp6][__tmp1.lower()]['responses']
              [response]['content']['application/json']['schema'])

    exclusion_list = (EXCLUDE_PROPERTIES.get(__tmp6, {}).get(__tmp1, {})
                                        .get(response, []))

    for key, value in content.items():
        # Ignore in the validation the keys in EXCLUDE_PROPERTIES
        if key in exclusion_list:
            continue

        # Check that the key is defined in the schema
        if key not in schema['properties']:
            raise SchemaError('Extraneous key "{}" in the response\'s '
                              'content'.format(key))

        # Check that the types match
        expected_type = __tmp3(schema['properties'][key]['type'])
        actual_type = __typ0(value)
        if expected_type is not actual_type:
            raise SchemaError('Expected type {} for key "{}", but actually '
                              'got {}'.format(expected_type, key, actual_type))

    # Check that at least all the required keys are present
    for req_key in schema['required']:
        if req_key not in content.keys():
            raise SchemaError('Expected to find the "{}" required key')

def __tmp3(py_type: <FILL>) -> __typ0:
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

    return TYPES[py_type]

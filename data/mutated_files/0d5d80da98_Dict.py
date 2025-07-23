from typing import TypeAlias
__typ8 : TypeAlias = "Any"
__typ2 : TypeAlias = "str"
__typ4 : TypeAlias = "Hashable"
__typ6 : TypeAlias = "Callable"
__typ7 : TypeAlias = "HomeAssistant"
"""Classes to help gather user submissions."""
import logging
from typing import Dict, Any, Callable, Hashable, List, Optional  # noqa pylint: disable=unused-import
import uuid
import voluptuous as vol
from .core import callback, HomeAssistant
from .exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)

RESULT_TYPE_FORM = 'form'
RESULT_TYPE_CREATE_ENTRY = 'create_entry'
RESULT_TYPE_ABORT = 'abort'


class __typ9(HomeAssistantError):
    """Error while configuring an account."""


class __typ10(__typ9):
    """Unknown handler specified."""


class __typ0(__typ9):
    """Uknown flow specified."""


class __typ3(__typ9):
    """Unknown step specified."""


class __typ1:
    """Manage all the flows that are in progress."""

    def __init__(__tmp0, hass, __tmp2,
                 async_finish_flow: __typ6) :
        """Initialize the flow manager."""
        __tmp0.hass = hass
        __tmp0._progress = {}  # type: Dict[str, Any]
        __tmp0._async_create_flow = __tmp2
        __tmp0._async_finish_flow = async_finish_flow

    @callback
    def async_progress(__tmp0) :
        """Return the flows in progress."""
        return [{
            'flow_id': __tmp7.flow_id,
            'handler': __tmp7.handler,
            'context': __tmp7.context,
        } for __tmp7 in __tmp0._progress.values()]

    async def async_init(__tmp0, handler: __typ4, *,
                         context: Optional[Dict] = None,
                         __tmp3: __typ8 = None) :
        """Start a configuration flow."""
        __tmp7 = await __tmp0._async_create_flow(
            handler, context=context, __tmp3=__tmp3)
        __tmp7.hass = __tmp0.hass
        __tmp7.handler = handler
        __tmp7.flow_id = uuid.uuid4().hex
        __tmp7.context = context
        __tmp0._progress[__tmp7.flow_id] = __tmp7

        return await __tmp0._async_handle_step(__tmp7, __tmp7.init_step, __tmp3)

    async def __tmp5(
            __tmp0, flow_id, __tmp10: Optional[Dict] = None) :
        """Continue a configuration flow."""
        __tmp7 = __tmp0._progress.get(flow_id)

        if __tmp7 is None:
            raise __typ0

        __tmp9, data_schema = __tmp7.cur_step

        if data_schema is not None and __tmp10 is not None:
            __tmp10 = data_schema(__tmp10)

        return await __tmp0._async_handle_step(
            __tmp7, __tmp9, __tmp10)

    @callback
    def __tmp8(__tmp0, flow_id: __typ2) :
        """Abort a flow."""
        if __tmp0._progress.pop(flow_id, None) is None:
            raise __typ0

    async def _async_handle_step(__tmp0, __tmp7, __tmp9,
                                 __tmp10: Optional[Dict]) :
        """Handle a step of a flow."""
        method = "async_step_{}".format(__tmp9)

        if not hasattr(__tmp7, method):
            __tmp0._progress.pop(__tmp7.flow_id)
            raise __typ3("Handler {} doesn't support step {}".format(
                __tmp7.__class__.__name__, __tmp9))

        result = await getattr(__tmp7, method)(__tmp10)  # type: Dict

        if result['type'] not in (RESULT_TYPE_FORM, RESULT_TYPE_CREATE_ENTRY,
                                  RESULT_TYPE_ABORT):
            raise ValueError(
                'Handler returned incorrect type: {}'.format(result['type']))

        if result['type'] == RESULT_TYPE_FORM:
            __tmp7.cur_step = (result['step_id'], result['data_schema'])
            return result

        # We pass a copy of the result because we're mutating our version
        result = await __tmp0._async_finish_flow(__tmp7, dict(result))

        # _async_finish_flow may change result type, check it again
        if result['type'] == RESULT_TYPE_FORM:
            __tmp7.cur_step = (result['step_id'], result['data_schema'])
            return result

        # Abort and Success results both finish the flow
        __tmp0._progress.pop(__tmp7.flow_id)

        return result


class __typ5:
    """Handle the configuration flow of a component."""

    # Set by flow manager
    flow_id = None
    hass = None
    handler = None
    cur_step = None
    context = None

    # Set by _async_create_flow callback
    init_step = 'init'

    # Set by developer
    VERSION = 1

    @callback
    def __tmp4(__tmp0, *, __tmp9, data_schema: vol.Schema = None,
                        errors: Optional[Dict] = None,
                        description_placeholders: Optional[Dict] = None) \
            -> Dict:
        """Return the definition of a form to gather user input."""
        return {
            'type': RESULT_TYPE_FORM,
            'flow_id': __tmp0.flow_id,
            'handler': __tmp0.handler,
            'step_id': __tmp9,
            'data_schema': data_schema,
            'errors': errors,
            'description_placeholders': description_placeholders,
        }

    @callback
    def __tmp1(__tmp0, *, title: __typ2, __tmp3: <FILL>,
                           description: Optional[__typ2] = None,
                           description_placeholders: Optional[Dict] = None) \
            :
        """Finish config flow and create a config entry."""
        return {
            'version': __tmp0.VERSION,
            'type': RESULT_TYPE_CREATE_ENTRY,
            'flow_id': __tmp0.flow_id,
            'handler': __tmp0.handler,
            'title': title,
            'data': __tmp3,
            'description': description,
            'description_placeholders': description_placeholders,
        }

    @callback
    def __tmp8(__tmp0, *, __tmp6: __typ2) :
        """Abort the config flow."""
        return {
            'type': RESULT_TYPE_ABORT,
            'flow_id': __tmp0.flow_id,
            'handler': __tmp0.handler,
            'reason': __tmp6
        }

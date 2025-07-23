from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ4 : TypeAlias = "Hashable"
__typ7 : TypeAlias = "Any"
__typ8 : TypeAlias = "Dict"
__typ6 : TypeAlias = "HomeAssistant"
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

    def __init__(__tmp2, hass: __typ6, async_create_flow: <FILL>,
                 __tmp1) -> None:
        """Initialize the flow manager."""
        __tmp2.hass = hass
        __tmp2._progress = {}  # type: Dict[str, Any]
        __tmp2._async_create_flow = async_create_flow
        __tmp2._async_finish_flow = __tmp1

    @callback
    def async_progress(__tmp2) :
        """Return the flows in progress."""
        return [{
            'flow_id': flow.flow_id,
            'handler': flow.handler,
            'context': flow.context,
        } for flow in __tmp2._progress.values()]

    async def async_init(__tmp2, handler: __typ4, *,
                         context: Optional[__typ8] = None,
                         data: __typ7 = None) -> __typ7:
        """Start a configuration flow."""
        flow = await __tmp2._async_create_flow(
            handler, context=context, data=data)
        flow.hass = __tmp2.hass
        flow.handler = handler
        flow.flow_id = uuid.uuid4().hex
        flow.context = context
        __tmp2._progress[flow.flow_id] = flow

        return await __tmp2._async_handle_step(flow, flow.init_step, data)

    async def async_configure(
            __tmp2, flow_id: __typ2, user_input: Optional[__typ8] = None) :
        """Continue a configuration flow."""
        flow = __tmp2._progress.get(flow_id)

        if flow is None:
            raise __typ0

        step_id, data_schema = flow.cur_step

        if data_schema is not None and user_input is not None:
            user_input = data_schema(user_input)

        return await __tmp2._async_handle_step(
            flow, step_id, user_input)

    @callback
    def async_abort(__tmp2, flow_id) -> None:
        """Abort a flow."""
        if __tmp2._progress.pop(flow_id, None) is None:
            raise __typ0

    async def _async_handle_step(__tmp2, flow, step_id: __typ2,
                                 user_input: Optional[__typ8]) -> __typ8:
        """Handle a step of a flow."""
        method = "async_step_{}".format(step_id)

        if not hasattr(flow, method):
            __tmp2._progress.pop(flow.flow_id)
            raise __typ3("Handler {} doesn't support step {}".format(
                flow.__class__.__name__, step_id))

        result = await getattr(flow, method)(user_input)  # type: Dict

        if result['type'] not in (RESULT_TYPE_FORM, RESULT_TYPE_CREATE_ENTRY,
                                  RESULT_TYPE_ABORT):
            raise ValueError(
                'Handler returned incorrect type: {}'.format(result['type']))

        if result['type'] == RESULT_TYPE_FORM:
            flow.cur_step = (result['step_id'], result['data_schema'])
            return result

        # We pass a copy of the result because we're mutating our version
        result = await __tmp2._async_finish_flow(flow, dict(result))

        # _async_finish_flow may change result type, check it again
        if result['type'] == RESULT_TYPE_FORM:
            flow.cur_step = (result['step_id'], result['data_schema'])
            return result

        # Abort and Success results both finish the flow
        __tmp2._progress.pop(flow.flow_id)

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
    def __tmp0(__tmp2, *, step_id: __typ2, data_schema: vol.Schema = None,
                        errors: Optional[__typ8] = None,
                        description_placeholders: Optional[__typ8] = None) \
            -> __typ8:
        """Return the definition of a form to gather user input."""
        return {
            'type': RESULT_TYPE_FORM,
            'flow_id': __tmp2.flow_id,
            'handler': __tmp2.handler,
            'step_id': step_id,
            'data_schema': data_schema,
            'errors': errors,
            'description_placeholders': description_placeholders,
        }

    @callback
    def __tmp3(__tmp2, *, title: __typ2, data,
                           description: Optional[__typ2] = None,
                           description_placeholders: Optional[__typ8] = None) \
            -> __typ8:
        """Finish config flow and create a config entry."""
        return {
            'version': __tmp2.VERSION,
            'type': RESULT_TYPE_CREATE_ENTRY,
            'flow_id': __tmp2.flow_id,
            'handler': __tmp2.handler,
            'title': title,
            'data': data,
            'description': description,
            'description_placeholders': description_placeholders,
        }

    @callback
    def async_abort(__tmp2, *, reason: __typ2) -> __typ8:
        """Abort the config flow."""
        return {
            'type': RESULT_TYPE_ABORT,
            'flow_id': __tmp2.flow_id,
            'handler': __tmp2.handler,
            'reason': reason
        }

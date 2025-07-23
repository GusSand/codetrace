from typing import TypeAlias
__typ0 : TypeAlias = "str"
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


class FlowError(HomeAssistantError):
    """Error while configuring an account."""


class UnknownHandler(FlowError):
    """Unknown handler specified."""


class UnknownFlow(FlowError):
    """Uknown flow specified."""


class UnknownStep(FlowError):
    """Unknown step specified."""


class FlowManager:
    """Manage all the flows that are in progress."""

    def __init__(__tmp0, hass, async_create_flow: Callable,
                 __tmp1: <FILL>) -> None:
        """Initialize the flow manager."""
        __tmp0.hass = hass
        __tmp0._progress = {}  # type: Dict[str, Any]
        __tmp0._async_create_flow = async_create_flow
        __tmp0._async_finish_flow = __tmp1

    @callback
    def async_progress(__tmp0) -> List[Dict]:
        """Return the flows in progress."""
        return [{
            'flow_id': flow.flow_id,
            'handler': flow.handler,
            'context': flow.context,
        } for flow in __tmp0._progress.values()]

    async def async_init(__tmp0, handler, *,
                         context: Optional[Dict] = None,
                         __tmp3: Any = None) -> Any:
        """Start a configuration flow."""
        flow = await __tmp0._async_create_flow(
            handler, context=context, __tmp3=__tmp3)
        flow.hass = __tmp0.hass
        flow.handler = handler
        flow.flow_id = uuid.uuid4().hex
        flow.context = context
        __tmp0._progress[flow.flow_id] = flow

        return await __tmp0._async_handle_step(flow, flow.init_step, __tmp3)

    async def async_configure(
            __tmp0, flow_id, user_input: Optional[Dict] = None) -> Any:
        """Continue a configuration flow."""
        flow = __tmp0._progress.get(flow_id)

        if flow is None:
            raise UnknownFlow

        step_id, data_schema = flow.cur_step

        if data_schema is not None and user_input is not None:
            user_input = data_schema(user_input)

        return await __tmp0._async_handle_step(
            flow, step_id, user_input)

    @callback
    def __tmp2(__tmp0, flow_id: __typ0) :
        """Abort a flow."""
        if __tmp0._progress.pop(flow_id, None) is None:
            raise UnknownFlow

    async def _async_handle_step(__tmp0, flow, step_id,
                                 user_input) :
        """Handle a step of a flow."""
        method = "async_step_{}".format(step_id)

        if not hasattr(flow, method):
            __tmp0._progress.pop(flow.flow_id)
            raise UnknownStep("Handler {} doesn't support step {}".format(
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
        result = await __tmp0._async_finish_flow(flow, dict(result))

        # _async_finish_flow may change result type, check it again
        if result['type'] == RESULT_TYPE_FORM:
            flow.cur_step = (result['step_id'], result['data_schema'])
            return result

        # Abort and Success results both finish the flow
        __tmp0._progress.pop(flow.flow_id)

        return result


class FlowHandler:
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
    def async_show_form(__tmp0, *, step_id: __typ0, data_schema: vol.Schema = None,
                        errors: Optional[Dict] = None,
                        description_placeholders: Optional[Dict] = None) \
            :
        """Return the definition of a form to gather user input."""
        return {
            'type': RESULT_TYPE_FORM,
            'flow_id': __tmp0.flow_id,
            'handler': __tmp0.handler,
            'step_id': step_id,
            'data_schema': data_schema,
            'errors': errors,
            'description_placeholders': description_placeholders,
        }

    @callback
    def async_create_entry(__tmp0, *, title: __typ0, __tmp3,
                           description: Optional[__typ0] = None,
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
    def __tmp2(__tmp0, *, reason: __typ0) -> Dict:
        """Abort the config flow."""
        return {
            'type': RESULT_TYPE_ABORT,
            'flow_id': __tmp0.flow_id,
            'handler': __tmp0.handler,
            'reason': reason
        }

from typing import TypeAlias
__typ7 : TypeAlias = "Dict"
__typ5 : TypeAlias = "HomeAssistant"
__typ6 : TypeAlias = "Any"
__typ2 : TypeAlias = "Hashable"
__typ4 : TypeAlias = "Callable"
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


class __typ8(HomeAssistantError):
    """Error while configuring an account."""


class __typ9(__typ8):
    """Unknown handler specified."""


class __typ0(__typ8):
    """Uknown flow specified."""


class __typ3(__typ8):
    """Unknown step specified."""


class __typ1:
    """Manage all the flows that are in progress."""

    def __tmp4(__tmp1, hass: __typ5, async_create_flow: __typ4,
                 __tmp8) -> None:
        """Initialize the flow manager."""
        __tmp1.hass = hass
        __tmp1._progress = {}  # type: Dict[str, Any]
        __tmp1._async_create_flow = async_create_flow
        __tmp1._async_finish_flow = __tmp8

    @callback
    def async_progress(__tmp1) :
        """Return the flows in progress."""
        return [{
            'flow_id': flow.flow_id,
            'handler': flow.handler,
            'context': flow.context,
        } for flow in __tmp1._progress.values()]

    async def __tmp5(__tmp1, handler, *,
                         context: Optional[__typ7] = None,
                         data: __typ6 = None) :
        """Start a configuration flow."""
        flow = await __tmp1._async_create_flow(
            handler, context=context, data=data)
        flow.hass = __tmp1.hass
        flow.handler = handler
        flow.flow_id = uuid.uuid4().hex
        flow.context = context
        __tmp1._progress[flow.flow_id] = flow

        return await __tmp1._async_handle_step(flow, flow.init_step, data)

    async def async_configure(
            __tmp1, flow_id, __tmp9: Optional[__typ7] = None) :
        """Continue a configuration flow."""
        flow = __tmp1._progress.get(flow_id)

        if flow is None:
            raise __typ0

        __tmp7, data_schema = flow.cur_step

        if data_schema is not None and __tmp9 is not None:
            __tmp9 = data_schema(__tmp9)

        return await __tmp1._async_handle_step(
            flow, __tmp7, __tmp9)

    @callback
    def __tmp6(__tmp1, flow_id) -> None:
        """Abort a flow."""
        if __tmp1._progress.pop(flow_id, None) is None:
            raise __typ0

    async def _async_handle_step(__tmp1, flow: __typ6, __tmp7,
                                 __tmp9: Optional[__typ7]) :
        """Handle a step of a flow."""
        method = "async_step_{}".format(__tmp7)

        if not hasattr(flow, method):
            __tmp1._progress.pop(flow.flow_id)
            raise __typ3("Handler {} doesn't support step {}".format(
                flow.__class__.__name__, __tmp7))

        result = await getattr(flow, method)(__tmp9)  # type: Dict

        if result['type'] not in (RESULT_TYPE_FORM, RESULT_TYPE_CREATE_ENTRY,
                                  RESULT_TYPE_ABORT):
            raise ValueError(
                'Handler returned incorrect type: {}'.format(result['type']))

        if result['type'] == RESULT_TYPE_FORM:
            flow.cur_step = (result['step_id'], result['data_schema'])
            return result

        # We pass a copy of the result because we're mutating our version
        result = await __tmp1._async_finish_flow(flow, dict(result))

        # _async_finish_flow may change result type, check it again
        if result['type'] == RESULT_TYPE_FORM:
            flow.cur_step = (result['step_id'], result['data_schema'])
            return result

        # Abort and Success results both finish the flow
        __tmp1._progress.pop(flow.flow_id)

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
    def __tmp0(__tmp1, *, __tmp7, data_schema: vol.Schema = None,
                        errors: Optional[__typ7] = None,
                        description_placeholders: Optional[__typ7] = None) \
            :
        """Return the definition of a form to gather user input."""
        return {
            'type': RESULT_TYPE_FORM,
            'flow_id': __tmp1.flow_id,
            'handler': __tmp1.handler,
            'step_id': __tmp7,
            'data_schema': data_schema,
            'errors': errors,
            'description_placeholders': description_placeholders,
        }

    @callback
    def __tmp2(__tmp1, *, __tmp3, data: __typ7,
                           description: Optional[str] = None,
                           description_placeholders: Optional[__typ7] = None) \
            :
        """Finish config flow and create a config entry."""
        return {
            'version': __tmp1.VERSION,
            'type': RESULT_TYPE_CREATE_ENTRY,
            'flow_id': __tmp1.flow_id,
            'handler': __tmp1.handler,
            'title': __tmp3,
            'data': data,
            'description': description,
            'description_placeholders': description_placeholders,
        }

    @callback
    def __tmp6(__tmp1, *, reason: <FILL>) :
        """Abort the config flow."""
        return {
            'type': RESULT_TYPE_ABORT,
            'flow_id': __tmp1.flow_id,
            'handler': __tmp1.handler,
            'reason': reason
        }

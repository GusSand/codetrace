from typing import TypeAlias
__typ1 : TypeAlias = "Callable"
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "Hashable"
__typ3 : TypeAlias = "Dict"
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


class __typ4(FlowError):
    """Unknown handler specified."""


class UnknownFlow(FlowError):
    """Uknown flow specified."""


class UnknownStep(FlowError):
    """Unknown step specified."""


class FlowManager:
    """Manage all the flows that are in progress."""

    def __tmp12(__tmp0, hass, __tmp1,
                 __tmp14) :
        """Initialize the flow manager."""
        __tmp0.hass = hass
        __tmp0._progress = {}  # type: Dict[str, Any]
        __tmp0._async_create_flow = __tmp1
        __tmp0._async_finish_flow = __tmp14

    @callback
    def __tmp4(__tmp0) :
        """Return the flows in progress."""
        return [{
            'flow_id': __tmp8.flow_id,
            'handler': __tmp8.handler,
            'context': __tmp8.context,
        } for __tmp8 in __tmp0._progress.values()]

    async def __tmp10(__tmp0, handler, *,
                         context: Optional[__typ3] = None,
                         __tmp3: __typ2 = None) :
        """Start a configuration flow."""
        __tmp8 = await __tmp0._async_create_flow(
            handler, context=context, __tmp3=__tmp3)
        __tmp8.hass = __tmp0.hass
        __tmp8.handler = handler
        __tmp8.flow_id = uuid.uuid4().hex
        __tmp8.context = context
        __tmp0._progress[__tmp8.flow_id] = __tmp8

        return await __tmp0._async_handle_step(__tmp8, __tmp8.init_step, __tmp3)

    async def __tmp5(
            __tmp0, flow_id, __tmp15: Optional[__typ3] = None) :
        """Continue a configuration flow."""
        __tmp8 = __tmp0._progress.get(flow_id)

        if __tmp8 is None:
            raise UnknownFlow

        __tmp13, data_schema = __tmp8.cur_step

        if data_schema is not None and __tmp15 is not None:
            __tmp15 = data_schema(__tmp15)

        return await __tmp0._async_handle_step(
            __tmp8, __tmp13, __tmp15)

    @callback
    def __tmp11(__tmp0, flow_id) :
        """Abort a flow."""
        if __tmp0._progress.pop(flow_id, None) is None:
            raise UnknownFlow

    async def _async_handle_step(__tmp0, __tmp8, __tmp13: <FILL>,
                                 __tmp15) :
        """Handle a step of a flow."""
        method = "async_step_{}".format(__tmp13)

        if not hasattr(__tmp8, method):
            __tmp0._progress.pop(__tmp8.flow_id)
            raise UnknownStep("Handler {} doesn't support step {}".format(
                __tmp8.__class__.__name__, __tmp13))

        result = await getattr(__tmp8, method)(__tmp15)  # type: Dict

        if result['type'] not in (RESULT_TYPE_FORM, RESULT_TYPE_CREATE_ENTRY,
                                  RESULT_TYPE_ABORT):
            raise ValueError(
                'Handler returned incorrect type: {}'.format(result['type']))

        if result['type'] == RESULT_TYPE_FORM:
            __tmp8.cur_step = (result['step_id'], result['data_schema'])
            return result

        # We pass a copy of the result because we're mutating our version
        result = await __tmp0._async_finish_flow(__tmp8, dict(result))

        # _async_finish_flow may change result type, check it again
        if result['type'] == RESULT_TYPE_FORM:
            __tmp8.cur_step = (result['step_id'], result['data_schema'])
            return result

        # Abort and Success results both finish the flow
        __tmp0._progress.pop(__tmp8.flow_id)

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
    def __tmp2(__tmp0, *, __tmp13, data_schema: vol.Schema = None,
                        errors: Optional[__typ3] = None,
                        description_placeholders: Optional[__typ3] = None) \
            :
        """Return the definition of a form to gather user input."""
        return {
            'type': RESULT_TYPE_FORM,
            'flow_id': __tmp0.flow_id,
            'handler': __tmp0.handler,
            'step_id': __tmp13,
            'data_schema': data_schema,
            'errors': errors,
            'description_placeholders': description_placeholders,
        }

    @callback
    def __tmp6(__tmp0, *, __tmp9, __tmp3,
                           description: Optional[str] = None,
                           description_placeholders: Optional[__typ3] = None) \
            :
        """Finish config flow and create a config entry."""
        return {
            'version': __tmp0.VERSION,
            'type': RESULT_TYPE_CREATE_ENTRY,
            'flow_id': __tmp0.flow_id,
            'handler': __tmp0.handler,
            'title': __tmp9,
            'data': __tmp3,
            'description': description,
            'description_placeholders': description_placeholders,
        }

    @callback
    def __tmp11(__tmp0, *, __tmp7) :
        """Abort the config flow."""
        return {
            'type': RESULT_TYPE_ABORT,
            'flow_id': __tmp0.flow_id,
            'handler': __tmp0.handler,
            'reason': __tmp7
        }

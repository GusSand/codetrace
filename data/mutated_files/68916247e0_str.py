from typing import TypeAlias
__typ0 : TypeAlias = "Any"
# See readme.md for instructions on running this code.

from typing import Dict, Any, Optional, Callable
import wit
import sys
import importlib.util

class WitaiHandler(object):
    def __tmp6(__tmp0) :
        return '''
        Wit.ai bot uses pywit API to interact with Wit.ai. In order to use
        Wit.ai bot, `witai.conf` must be set up. See `doc.md` for more details.
        '''

    def __tmp5(__tmp0, __tmp2) :
        config = __tmp2.get_config_info('witai')

        token = config.get('token')
        if not token:
            raise KeyError('No `token` was specified')

        # `handler_location` should be the location of a module which contains
        # the function `handle`. See `doc.md` for more details.
        handler_location = config.get('handler_location')
        if not handler_location:
            raise KeyError('No `handler_location` was specified')
        handle = __tmp3(handler_location)
        if handle is None:
            raise Exception('Could not get handler from handler_location.')
        else:
            __tmp0.handle = handle

        help_message = config.get('help_message')
        if not help_message:
            raise KeyError('No `help_message` was specified')
        __tmp0.help_message = help_message

        __tmp0.client = wit.Wit(token)

    def __tmp1(__tmp0, message, __tmp2) :
        if message['content'] == '' or message['content'] == 'help':
            __tmp2.send_reply(message, __tmp0.help_message)
            return

        try:
            res = __tmp0.client.message(message['content'])
            message_for_user = __tmp0.handle(res)

            if message_for_user:
                __tmp2.send_reply(message, message_for_user)
        except wit.wit.WitError:
            __tmp2.send_reply(message, 'Sorry, I don\'t know how to respond to that!')
        except Exception as e:
            __tmp2.send_reply(message, 'Sorry, there was an internal error.')
            print(e)
            return

handler_class = WitaiHandler

def __tmp3(__tmp4: <FILL>) :
    '''Returns a function to be used when generating a response from Wit.ai
    bot. This function is the function named `handle` in the module at the
    given `location`. For an example of a `handle` function, see `doc.md`.

    For example,

        handle = get_handle('/Users/someuser/witai_handler.py')  # Get the handler function.
        res = witai_client.message(message['content'])  # Get the Wit.ai response.
        message_res = self.handle(res)  # Handle the response and find what to show the user.
        bot_handler.send_reply(message, message_res)  # Send it to the user.

    Parameters:
     - location: The absolute path to the module to look for `handle` in.
    '''
    try:
        spec = importlib.util.spec_from_file_location('module.name', __tmp4)
        handler = importlib.util.module_from_spec(spec)
        loader = spec.loader
        if loader is None:
            return None
        loader.exec_module(handler)
        return handler.handle  # type: ignore
    except Exception as e:
        print(e)
        return None

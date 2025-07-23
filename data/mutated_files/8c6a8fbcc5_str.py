from typing import TypeAlias
__typ1 : TypeAlias = "Any"
from typing import Any, Dict

def __tmp1(__tmp2: <FILL>) :
    # This is where the actual ROT13 is applied
    # WHY IS .JOIN NOT WORKING?!
    textlist = list(__tmp2)
    newtext = ''
    firsthalf = 'abcdefghijklmABCDEFGHIJKLM'
    lasthalf = 'nopqrstuvwxyzNOPQRSTUVWXYZ'
    for char in textlist:
        if char in firsthalf:
            newtext += lasthalf[firsthalf.index(char)]
        elif char in lasthalf:
            newtext += firsthalf[lasthalf.index(char)]
        else:
            newtext += char

    return newtext

class __typ0(object):
    '''
    This bot allows users to quickly encrypt messages using ROT13 encryption.
    It encrypts/decrypts messages starting with @mention-bot.
    '''

    def __tmp6(__tmp3) :
        return '''
            This bot uses ROT13 encryption for its purposes.
            It responds to me starting with @mention-bot.
            Feeding encrypted messages into the bot decrypts them.
            '''

    def __tmp4(__tmp3, __tmp0, __tmp5: __typ1) :
        bot_response = __tmp3.get_bot_encrypt_response(__tmp0)
        __tmp5.send_reply(__tmp0, bot_response)

    def get_bot_encrypt_response(__tmp3, __tmp0) :
        original_content = __tmp0['content']
        temp_content = __tmp1(original_content)
        send_content = "Encrypted/Decrypted text: " + temp_content
        return send_content

handler_class = __typ0

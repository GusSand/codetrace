from typing import TypeAlias
__typ0 : TypeAlias = "str"
import requests
import re
from typing import Dict, Any, Tuple, Union

class __typ1(object):
    '''
    Shopedia
    To create and know more of SUSI skills go to ``

    '''

    def usage(__tmp1) -> __typ0:
        return '''
    Hi, I am Shopedia, you can ask me:
    ```
    Where can I buy a laptop?
    ```
        '''

    def __tmp3(__tmp1, __tmp0, __tmp2: <FILL>) -> None:
        msg = __tmp0['content']
        if msg == 'help' or msg == '':
            __tmp2.send_reply(__tmp0, __tmp1.usage())
            return
        words = msg.split(' ')
        query = words[len(words) - 1] 
        query = query[:-1]   
        reply = requests.post("https://shopedia.herokuapp.com/consumer/search", data={'itemName': query, 'latitude': '31', 'longitude': '76'})
        try:
            answer = reply.json()[0]['shopName'] + ' is nearby!'
            # answer = reply.json()[0]['shopName']+ 'will find you a ' + query + '. It\'s just ' +reply.json()[0]['distance'] + 'kilometers away!'
            # print(answer)
        # except Exception:
        except:
            answer = "I don't understand. Can you rephrase?"
        __tmp2.send_reply(__tmp0, answer)

handler_class = __typ1

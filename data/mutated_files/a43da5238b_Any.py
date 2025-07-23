import requests
from typing import Dict, Any, Tuple, Union

class SusiHandler(object):
    '''
    Susi AI Bot
    To create and know more of SUSI skills go to `https://skills.susi.ai/`
    '''

    def usage(__tmp1) :
        return '''
    Hi, I am Susi, people generally ask me these questions:
    ```
    What is the exchange rate of USD to BTC
    How to cook biryani
    draw a card
    word starting with m and ending with v
    question me
    random GIF
    image of a bird
    flip a coin
    let us play
    who is Albert Einstein
    search wikipedia for artificial intelligence
    when is christmas
    what is hello in french
    name a popular movie
    news
    tell me a joke
    buy a dress
    currency of singapore
    distance between india and singapore
    tell me latest phone by LG
    ```
        '''

    def __tmp3(__tmp1, __tmp0, __tmp2: <FILL>) -> None:
        msg = __tmp0['content']
        if msg == 'help' or msg == '':
            __tmp2.send_reply(__tmp0, __tmp1.usage())
            return
        reply = requests.get("https://api.susi.ai/susi/chat.json", params=dict(q=msg))
        try:
            answer = reply.json()['answers'][0]['actions'][0]['expression']
        except Exception:
            answer = "I don't understand. Can you rephrase?"
        __tmp2.send_reply(__tmp0, answer)

handler_class = SusiHandler

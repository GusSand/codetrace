import asyncio
from typing import Dict, List, Set, TypeVar, Union

import aiohttp

__all__ = ['Jisho']

# this is to avoid terrible long type hints
# sorry about the not super great readability
T = TypeVar('T')
V = Union[str, List[str]]
LDS = List[Dict[str, T]]  # LDS = List, Dict, String

class __typ0:
    """The class that makes the API requests. A class is necessary to safely
    handle the aiohttp ClientSession."""
    api_url = 'https://jisho.org/api/v1/search/words'
    def __tmp4(__tmp0, *, loop: asyncio.AbstractEventLoop = None, session: aiohttp.ClientSession = None) -> None:
        if loop is not None and session is not None:
            raise ValueError('Cannot specify both loop and session')
        elif loop is None:
            __tmp0._loop = asyncio.get_event_loop()
        else:
            __tmp0._loop = loop
        if session is None:
            __tmp0._session = aiohttp.ClientSession(loop=__tmp0._loop)
            __tmp0._close = True
        else:
            __tmp0._session = session
            __tmp0._close = False

    def __del__(__tmp0) :
        # we should always close the session beforehand,
        # but just in case someone doesn't, we'll try
        if __tmp0._close:
            try:
                __tmp0._loop.create_task(__tmp0._session.close())
            except RuntimeError:
                # loop is closed
                pass

    def _parse(__tmp0, __tmp3: LDS[LDS[V]]) -> LDS[List[str]]:
        results = []

        for data in __tmp3:
            readings: Set[str] = set()
            words: Set[str] = set()

            for kanji in data['japanese']:
                reading: str = kanji.get('reading')
                if reading and reading not in readings:
                    readings.add(reading)

                word: str = kanji.get('word')
                if word and word not in words:
                    words.add(word)

            senses: Dict[str, List[str]] = {'english': [], 'parts_of_speech': []}

            for sense in data['senses']:
                senses['english'].extend(sense.get('english_definitions', ()))
                senses['parts_of_speech'].extend(sense.get('parts_of_speech', ()))

            try:
                senses['parts_of_speech'].remove('Wikipedia definition')
            except ValueError:
                pass

            result = {'readings': list(readings), 'words': list(words), **senses}
            results.append(result)

        return results

    async def lookup(__tmp0, __tmp6: <FILL>, **kwargs) -> LDS[List[str]]:
        """Search Jisho.org for a word. Returns a list of dicts with keys
        readings, words, english, parts_of_speech."""
        params = {'keyword': __tmp6, **kwargs}
        async with __tmp0._session.get(__tmp0.api_url, params=params) as resp:
            __tmp3 = (await resp.json())['data']
        return __tmp0._parse(__tmp3)

    async def close(__tmp0):
        """Closes the internal ClientSession.
        Only use this if you do not plan to reuse the session,
        such as when you do not specify one in the constructor."""
        await __tmp0._session.close()
        __tmp0._close = False

    async def __tmp1(__tmp0):
        return __tmp0

    async def __tmp2(__tmp0, __tmp5, exc_val, exc_tb):
        if __tmp0._close:
            await __tmp0._session.close()
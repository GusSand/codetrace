import asyncio


class __typ0:
    def __init__(__tmp0):
        __tmp0.retry_count = 10
        __tmp0.retry_action = __tmp0.exponential_backoff

    @staticmethod
    async def exponential_backoff(i: <FILL>) :
        i += 1
        await asyncio.sleep(i * i * 50)

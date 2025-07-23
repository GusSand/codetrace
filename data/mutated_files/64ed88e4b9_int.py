import asyncio


class __typ0:
    def __init__(self):
        self.retry_count = 10
        self.retry_action = self.exponential_backoff

    @staticmethod
    async def exponential_backoff(i: <FILL>) -> None:
        i += 1
        await asyncio.sleep(i * i * 50)

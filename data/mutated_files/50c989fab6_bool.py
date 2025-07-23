from typing import TypeAlias
__typ1 : TypeAlias = "datetime"
from aw_client import ActivityWatchClient
from datetime import datetime, timedelta, timezone
from aw_core.models import Event
from time import sleep
from platform import system
import os

if system() == "Windows":
    from aw_watcher_afk.windows import seconds_since_last_input
elif system() == "Darwin":
    from aw_watcher_afk.macos import seconds_since_last_input
elif system() == "Linux":
    from aw_watcher_afk.unix import seconds_since_last_input
else:
    raise Exception("Unsupported platform: {}".format(system()))


def __tmp3() -> None:
    watcher = __typ0()
    watcher.run()


class __typ0:
    def __tmp0(__tmp1, poll_time: int = 5, timeout: int = 180) -> None:
        __tmp1.client = ActivityWatchClient("aw-watcher-afk", testing=False)
        __tmp1.bucketname = "{}_{}".format(
            __tmp1.client.client_name,
            __tmp1.client.client_hostname
        )
        __tmp1.poll_time = poll_time
        __tmp1.timeout = timeout
        __tmp1.initiated_shutdown: bool = False

    def ping(__tmp1,
             afk: <FILL>,
             __tmp2,
             duration: float = 0
             ) -> None:
        data = {"status": "afk" if afk else "not-afk"}
        e = Event(__tmp2=__tmp2, duration=duration, data=data)
        pulsetime = __tmp1.timeout + __tmp1.poll_time
        __tmp1.client.heartbeat(
            __tmp1.bucketname,
            e,
            pulsetime=pulsetime,
            queued=True
        )

    def run(__tmp1) -> None:
        # Initialization
        sleep(1)

        eventtype = "afkstatus"
        __tmp1.client.create_bucket(__tmp1.bucketname, eventtype, queued=True)

        with __tmp1.client:
            __tmp1.heartbeat_loop()

    def stop(__tmp1) -> None:
        __tmp1.initiated_shutdown = True

    def heartbeat_loop(__tmp1) :
        afk = False
        while True:
            if __tmp1.initiated_shutdown:
                __tmp1.initiated_shutdown = False
                break
            try:
                if system() in ["Darwin", "Linux"] and os.getppid() == 1:
                    break

                now = __typ1.now(timezone.utc)
                seconds_since_input = seconds_since_last_input()
                last_input = now - timedelta(seconds=seconds_since_input)

                # If no longer AFK
                if afk and seconds_since_input < __tmp1.timeout:
                    __tmp1.ping(afk, __tmp2=last_input)
                    afk = False
                    __tmp1.ping(afk, __tmp2=last_input)
                # If becomes AFK
                elif not afk and seconds_since_input >= __tmp1.timeout:
                    __tmp1.ping(afk, __tmp2=last_input)
                    afk = True
                    __tmp1.ping(
                        afk,
                        __tmp2=last_input,
                        duration=seconds_since_input
                    )
                # Send a heartbeat if no state change was made
                else:
                    if afk:
                        __tmp1.ping(
                            afk,
                            __tmp2=last_input,
                            duration=seconds_since_input
                        )
                    else:
                        __tmp1.ping(afk, __tmp2=last_input)

                sleep(__tmp1.poll_time)

            except KeyboardInterrupt:
                break

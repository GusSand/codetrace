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


def __tmp1() :
    watcher = AfkRunner()
    watcher.run()


class AfkRunner:
    def __tmp3(__tmp0, poll_time: int = 5, timeout: int = 180) :
        __tmp0.client = ActivityWatchClient("aw-watcher-afk", testing=False)
        __tmp0.bucketname = "{}_{}".format(
            __tmp0.client.client_name,
            __tmp0.client.client_hostname
        )
        __tmp0.poll_time = poll_time
        __tmp0.timeout = timeout
        __tmp0.initiated_shutdown: bool = False

    def ping(__tmp0,
             afk,
             __tmp4: <FILL>,
             duration: float = 0
             ) -> None:
        data = {"status": "afk" if afk else "not-afk"}
        e = Event(__tmp4=__tmp4, duration=duration, data=data)
        pulsetime = __tmp0.timeout + __tmp0.poll_time
        __tmp0.client.heartbeat(
            __tmp0.bucketname,
            e,
            pulsetime=pulsetime,
            queued=True
        )

    def run(__tmp0) :
        # Initialization
        sleep(1)

        eventtype = "afkstatus"
        __tmp0.client.create_bucket(__tmp0.bucketname, eventtype, queued=True)

        with __tmp0.client:
            __tmp0.heartbeat_loop()

    def __tmp2(__tmp0) :
        __tmp0.initiated_shutdown = True

    def heartbeat_loop(__tmp0) -> None:
        afk = False
        while True:
            if __tmp0.initiated_shutdown:
                __tmp0.initiated_shutdown = False
                break
            try:
                if system() in ["Darwin", "Linux"] and os.getppid() == 1:
                    break

                now = datetime.now(timezone.utc)
                seconds_since_input = seconds_since_last_input()
                last_input = now - timedelta(seconds=seconds_since_input)

                # If no longer AFK
                if afk and seconds_since_input < __tmp0.timeout:
                    __tmp0.ping(afk, __tmp4=last_input)
                    afk = False
                    __tmp0.ping(afk, __tmp4=last_input)
                # If becomes AFK
                elif not afk and seconds_since_input >= __tmp0.timeout:
                    __tmp0.ping(afk, __tmp4=last_input)
                    afk = True
                    __tmp0.ping(
                        afk,
                        __tmp4=last_input,
                        duration=seconds_since_input
                    )
                # Send a heartbeat if no state change was made
                else:
                    if afk:
                        __tmp0.ping(
                            afk,
                            __tmp4=last_input,
                            duration=seconds_since_input
                        )
                    else:
                        __tmp0.ping(afk, __tmp4=last_input)

                sleep(__tmp0.poll_time)

            except KeyboardInterrupt:
                break

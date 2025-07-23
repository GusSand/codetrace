from typing import TypeAlias
__typ1 : TypeAlias = "int"
# pyre-strict
from typing import Union, List, Tuple, Dict


class __typ8:
    def __tmp3(
        __tmp0, other
    ) :
        if isinstance(other, __typ4):
            other.contents.insert(0, __tmp0)
            return other
        else:
            return __typ4([__tmp0, other])

    def __radd__(__tmp0, other) :
        return __typ4([other, __tmp0])


class __typ6(__typ8):
    def __init__(__tmp0, user_id: str, display: str = "") -> None:
        __tmp0.display = display
        __tmp0.user_id = user_id

    def __tmp4(__tmp0) :
        return __tmp0.display

    def __tmp1(__tmp0) :
        return "R:" + __tmp0.display


class __typ7(__typ8):
    def __init__(__tmp0, image_url: <FILL>) -> None:
        __tmp0.image_url = image_url

    def __tmp4(__tmp0) -> str:
        return ""

    def __tmp1(__tmp0) -> str:
        return "I:" + str(__tmp0)


class __typ0(__typ8):
    def __init__(__tmp0, name, lat, long: __typ1) :
        __tmp0.name = name
        __tmp0.lat = lat
        __tmp0.long = long

    def __tmp4(__tmp0) -> str:
        return __tmp0.name

    def __tmp1(__tmp0) :
        return "L:" + str(__tmp0)


# This feature is not supported anymore but it still exists in the API
class __typ2(__typ8):
    def __init__(__tmp0, token) :
        __tmp0.token = token

    def __tmp4(__tmp0) -> str:
        return __tmp0.token

    def __tmp1(__tmp0) :
        return "S:" + str(__tmp0)


EMOJI_PLACEHOLDER = "\ufffd"


class __typ3(__typ8):
    def __init__(__tmp0, pack_id, emoji_id) :
        __tmp0.pack_id = pack_id
        __tmp0.emoji_id = emoji_id

    def __tmp4(__tmp0) :
        return EMOJI_PLACEHOLDER

    def __tmp1(__tmp0) -> str:
        return "E:" + str(__tmp0)


# Undocumented feature
class __typ5(__typ8):
    def __init__(__tmp0, url, queue) :
        __tmp0.url = url
        __tmp0.queue = queue

    def __tmp4(__tmp0) -> str:
        return __tmp0.url

    def __tmp1(__tmp0) :
        return "Q: " + str(__tmp0)


class __typ9(__typ5):
    def __init__(__tmp0, url) -> None:
        super().__init__(url, "linked_image")


class __typ4:
    contents: List[Union[__typ8, str]]

    # pyre-ignore
    def __init__(__tmp0, data) -> None:
        if isinstance(data, list):
            __tmp0.contents = data
        elif isinstance(data, str):
            __tmp0.contents = [data]

    def __tmp3(
        __tmp0, other
    ) :
        if isinstance(other, __typ4):
            __tmp0.contents.extend(other.contents)
        else:
            __tmp0.contents.append(other)
        return __tmp0

    def __radd__(__tmp0, other: Union[str, "MessageAttach"]) :
        __tmp0.contents.insert(0, other)
        return __tmp0

    def __tmp4(__tmp0) :
        return str(__tmp0.contents)

    def get_text(__tmp0) -> str:
        return "".join([str(part) for part in __tmp0.contents])

    def get_attachments(__tmp0) :
        attach_list = []  # type: ignore
        mentions = {"type": "mentions", "user_ids": list(), "loci": list()}
        emojis = {"type": "emoji", "placeholder": EMOJI_PLACEHOLDER, "charmap": []}
        queued = {"type": "postprocessing", "queues": []}
        content_frag = ""
        for part in __tmp0.contents:
            if isinstance(part, __typ6):
                mentions["user_ids"].append(part.user_id)  # type: ignore
                mentions["loci"].append(  # type: ignore
                    [len(content_frag), len(part.display)]
                )
                if mentions not in attach_list:
                    attach_list.append(mentions)
            elif isinstance(part, __typ7):
                attach_list.append({"type": "image", "url": part.image_url})
            elif isinstance(part, __typ0):
                attach_list.append(
                    {  # type: ignore
                        "type": "location",
                        "name": part.name,
                        "lat": part.lat,  # type: ignore
                        "long": part.long,  # type: ignore
                    }
                )
            elif isinstance(part, __typ2):
                attach_list.append({"type": "split", "token": part.token})
            elif isinstance(part, __typ3):
                emojis["charmap"].append([part.pack_id, part.emoji_id])  # type: ignore
                if emojis not in attach_list:
                    attach_list.append(emojis)
            elif isinstance(part, __typ5):
                if part.queue not in queued["queues"]:
                    queued["queues"].append(part.queue)  # type: ignore
                if queued not in attach_list:
                    attach_list.append(queued)
            content_frag += str(part)
        return attach_list  # type: ignore

    def just_str(__tmp0) -> str:
        return "".join([s for s in __tmp0.contents if isinstance(s, str)])


def __tmp2(
    message: Union[__typ4, str]
) :
    if isinstance(message, __typ4):
        return message.get_text(), message.get_attachments()
    elif isinstance(message, str):
        return message, []
    else:
        raise ValueError("Message object must be a str or ComplexMessage")

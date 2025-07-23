from typing import TypeAlias
__typ0 : TypeAlias = "int"
# pyre-strict
from typing import Union, List, Tuple, Dict


class MessageAttach:
    def __tmp4(
        __tmp1, __tmp2: Union["ComplexMessage", str, "MessageAttach"]
    ) -> "ComplexMessage":
        if isinstance(__tmp2, __typ2):
            __tmp2.contents.insert(0, __tmp1)
            return __tmp2
        else:
            return __typ2([__tmp1, __tmp2])

    def __radd__(__tmp1, __tmp2: Union[str, "MessageAttach"]) -> "ComplexMessage":
        return __typ2([__tmp2, __tmp1])


class __typ3(MessageAttach):
    def __init__(__tmp1, user_id: str, display: str = "") -> None:
        __tmp1.display = display
        __tmp1.user_id = user_id

    def __str__(__tmp1) -> str:
        return __tmp1.display

    def __repr__(__tmp1) -> str:
        return "R:" + __tmp1.display


class __typ4(MessageAttach):
    def __init__(__tmp1, image_url: str) :
        __tmp1.image_url = image_url

    def __str__(__tmp1) -> str:
        return ""

    def __repr__(__tmp1) -> str:
        return "I:" + str(__tmp1)


class LocationAttach(MessageAttach):
    def __init__(__tmp1, name, lat, long: __typ0) -> None:
        __tmp1.name = name
        __tmp1.lat = lat
        __tmp1.long = long

    def __str__(__tmp1) :
        return __tmp1.name

    def __repr__(__tmp1) -> str:
        return "L:" + str(__tmp1)


# This feature is not supported anymore but it still exists in the API
class SplitAttach(MessageAttach):
    def __init__(__tmp1, token: str) -> None:
        __tmp1.token = token

    def __str__(__tmp1) -> str:
        return __tmp1.token

    def __repr__(__tmp1) :
        return "S:" + str(__tmp1)


EMOJI_PLACEHOLDER = "\ufffd"


class __typ1(MessageAttach):
    def __init__(__tmp1, pack_id: __typ0, emoji_id: __typ0) -> None:
        __tmp1.pack_id = pack_id
        __tmp1.emoji_id = emoji_id

    def __str__(__tmp1) -> str:
        return EMOJI_PLACEHOLDER

    def __repr__(__tmp1) -> str:
        return "E:" + str(__tmp1)


# Undocumented feature
class QueuedAttach(MessageAttach):
    def __init__(__tmp1, url: str, queue: str) -> None:
        __tmp1.url = url
        __tmp1.queue = queue

    def __str__(__tmp1) :
        return __tmp1.url

    def __repr__(__tmp1) -> str:
        return "Q: " + str(__tmp1)


class __typ5(QueuedAttach):
    def __init__(__tmp1, url: <FILL>) -> None:
        super().__init__(url, "linked_image")


class __typ2:
    contents: List[Union[MessageAttach, str]]

    # pyre-ignore
    def __init__(__tmp1, data: Union[list, str, MessageAttach]) :
        if isinstance(data, list):
            __tmp1.contents = data
        elif isinstance(data, str):
            __tmp1.contents = [data]

    def __tmp4(
        __tmp1, __tmp2: Union["ComplexMessage", str, "MessageAttach"]
    ) -> "ComplexMessage":
        if isinstance(__tmp2, __typ2):
            __tmp1.contents.extend(__tmp2.contents)
        else:
            __tmp1.contents.append(__tmp2)
        return __tmp1

    def __radd__(__tmp1, __tmp2: Union[str, "MessageAttach"]) -> "ComplexMessage":
        __tmp1.contents.insert(0, __tmp2)
        return __tmp1

    def __str__(__tmp1) -> str:
        return str(__tmp1.contents)

    def get_text(__tmp1) -> str:
        return "".join([str(part) for part in __tmp1.contents])

    def get_attachments(__tmp1) :
        attach_list = []  # type: ignore
        mentions = {"type": "mentions", "user_ids": list(), "loci": list()}
        emojis = {"type": "emoji", "placeholder": EMOJI_PLACEHOLDER, "charmap": []}
        queued = {"type": "postprocessing", "queues": []}
        content_frag = ""
        for part in __tmp1.contents:
            if isinstance(part, __typ3):
                mentions["user_ids"].append(part.user_id)  # type: ignore
                mentions["loci"].append(  # type: ignore
                    [len(content_frag), len(part.display)]
                )
                if mentions not in attach_list:
                    attach_list.append(mentions)
            elif isinstance(part, __typ4):
                attach_list.append({"type": "image", "url": part.image_url})
            elif isinstance(part, LocationAttach):
                attach_list.append(
                    {  # type: ignore
                        "type": "location",
                        "name": part.name,
                        "lat": part.lat,  # type: ignore
                        "long": part.long,  # type: ignore
                    }
                )
            elif isinstance(part, SplitAttach):
                attach_list.append({"type": "split", "token": part.token})
            elif isinstance(part, __typ1):
                emojis["charmap"].append([part.pack_id, part.emoji_id])  # type: ignore
                if emojis not in attach_list:
                    attach_list.append(emojis)
            elif isinstance(part, QueuedAttach):
                if part.queue not in queued["queues"]:
                    queued["queues"].append(part.queue)  # type: ignore
                if queued not in attach_list:
                    attach_list.append(queued)
            content_frag += str(part)
        return attach_list  # type: ignore

    def __tmp3(__tmp1) -> str:
        return "".join([s for s in __tmp1.contents if isinstance(s, str)])


def smart_split_complex_message(
    __tmp0: Union[__typ2, str]
) :
    if isinstance(__tmp0, __typ2):
        return __tmp0.get_text(), __tmp0.get_attachments()
    elif isinstance(__tmp0, str):
        return __tmp0, []
    else:
        raise ValueError("Message object must be a str or ComplexMessage")

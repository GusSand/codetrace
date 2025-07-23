from typing import TypeAlias
__typ5 : TypeAlias = "str"
# pyre-strict
from typing import Union, List, Tuple, Dict


class __typ7:
    def __add__(
        __tmp1, other: Union["ComplexMessage", __typ5, "MessageAttach"]
    ) -> "ComplexMessage":
        if isinstance(other, __typ3):
            other.contents.insert(0, __tmp1)
            return other
        else:
            return __typ3([__tmp1, other])

    def __radd__(__tmp1, other: Union[__typ5, "MessageAttach"]) -> "ComplexMessage":
        return __typ3([other, __tmp1])


class __typ4(__typ7):
    def __init__(__tmp1, user_id: __typ5, display: __typ5 = "") -> None:
        __tmp1.display = display
        __tmp1.user_id = user_id

    def __tmp2(__tmp1) -> __typ5:
        return __tmp1.display

    def __tmp3(__tmp1) -> __typ5:
        return "R:" + __tmp1.display


class __typ6(__typ7):
    def __init__(__tmp1, image_url: __typ5) -> None:
        __tmp1.image_url = image_url

    def __tmp2(__tmp1) :
        return ""

    def __tmp3(__tmp1) -> __typ5:
        return "I:" + __typ5(__tmp1)


class __typ1(__typ7):
    def __init__(__tmp1, name: __typ5, lat: int, long: int) -> None:
        __tmp1.name = name
        __tmp1.lat = lat
        __tmp1.long = long

    def __tmp2(__tmp1) -> __typ5:
        return __tmp1.name

    def __tmp3(__tmp1) -> __typ5:
        return "L:" + __typ5(__tmp1)


# This feature is not supported anymore but it still exists in the API
class SplitAttach(__typ7):
    def __init__(__tmp1, token: __typ5) -> None:
        __tmp1.token = token

    def __tmp2(__tmp1) -> __typ5:
        return __tmp1.token

    def __tmp3(__tmp1) -> __typ5:
        return "S:" + __typ5(__tmp1)


EMOJI_PLACEHOLDER = "\ufffd"


class __typ2(__typ7):
    def __init__(__tmp1, pack_id: int, emoji_id: <FILL>) -> None:
        __tmp1.pack_id = pack_id
        __tmp1.emoji_id = emoji_id

    def __tmp2(__tmp1) -> __typ5:
        return EMOJI_PLACEHOLDER

    def __tmp3(__tmp1) -> __typ5:
        return "E:" + __typ5(__tmp1)


# Undocumented feature
class __typ0(__typ7):
    def __init__(__tmp1, url: __typ5, queue: __typ5) -> None:
        __tmp1.url = url
        __tmp1.queue = queue

    def __tmp2(__tmp1) -> __typ5:
        return __tmp1.url

    def __tmp3(__tmp1) -> __typ5:
        return "Q: " + __typ5(__tmp1)


class __typ8(__typ0):
    def __init__(__tmp1, url: __typ5) -> None:
        super().__init__(url, "linked_image")


class __typ3:
    contents: List[Union[__typ7, __typ5]]

    # pyre-ignore
    def __init__(__tmp1, data: Union[list, __typ5, __typ7]) -> None:
        if isinstance(data, list):
            __tmp1.contents = data
        elif isinstance(data, __typ5):
            __tmp1.contents = [data]

    def __add__(
        __tmp1, other: Union["ComplexMessage", __typ5, "MessageAttach"]
    ) -> "ComplexMessage":
        if isinstance(other, __typ3):
            __tmp1.contents.extend(other.contents)
        else:
            __tmp1.contents.append(other)
        return __tmp1

    def __radd__(__tmp1, other: Union[__typ5, "MessageAttach"]) -> "ComplexMessage":
        __tmp1.contents.insert(0, other)
        return __tmp1

    def __tmp2(__tmp1) -> __typ5:
        return __typ5(__tmp1.contents)

    def get_text(__tmp1) -> __typ5:
        return "".join([__typ5(part) for part in __tmp1.contents])

    def get_attachments(__tmp1) -> List[Dict[__typ5, __typ5]]:
        attach_list = []  # type: ignore
        mentions = {"type": "mentions", "user_ids": list(), "loci": list()}
        emojis = {"type": "emoji", "placeholder": EMOJI_PLACEHOLDER, "charmap": []}
        queued = {"type": "postprocessing", "queues": []}
        content_frag = ""
        for part in __tmp1.contents:
            if isinstance(part, __typ4):
                mentions["user_ids"].append(part.user_id)  # type: ignore
                mentions["loci"].append(  # type: ignore
                    [len(content_frag), len(part.display)]
                )
                if mentions not in attach_list:
                    attach_list.append(mentions)
            elif isinstance(part, __typ6):
                attach_list.append({"type": "image", "url": part.image_url})
            elif isinstance(part, __typ1):
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
            elif isinstance(part, __typ2):
                emojis["charmap"].append([part.pack_id, part.emoji_id])  # type: ignore
                if emojis not in attach_list:
                    attach_list.append(emojis)
            elif isinstance(part, __typ0):
                if part.queue not in queued["queues"]:
                    queued["queues"].append(part.queue)  # type: ignore
                if queued not in attach_list:
                    attach_list.append(queued)
            content_frag += __typ5(part)
        return attach_list  # type: ignore

    def just_str(__tmp1) -> __typ5:
        return "".join([s for s in __tmp1.contents if isinstance(s, __typ5)])


def __tmp0(
    message: Union[__typ3, __typ5]
) -> Tuple[__typ5, List[Dict[__typ5, __typ5]]]:
    if isinstance(message, __typ3):
        return message.get_text(), message.get_attachments()
    elif isinstance(message, __typ5):
        return message, []
    else:
        raise ValueError("Message object must be a str or ComplexMessage")

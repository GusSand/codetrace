from typing import TypeAlias
__typ1 : TypeAlias = "int"
# pyre-strict
from typing import Union, List, Tuple, Dict


class MessageAttach:
    def __add__(
        __tmp1, __tmp0
    ) -> "ComplexMessage":
        if isinstance(__tmp0, __typ4):
            __tmp0.contents.insert(0, __tmp1)
            return __tmp0
        else:
            return __typ4([__tmp1, __tmp0])

    def __radd__(__tmp1, __tmp0: Union[str, "MessageAttach"]) -> "ComplexMessage":
        return __typ4([__tmp0, __tmp1])


class __typ6(MessageAttach):
    def __init__(__tmp1, user_id: str, display: str = "") -> None:
        __tmp1.display = display
        __tmp1.user_id = user_id

    def __tmp2(__tmp1) -> str:
        return __tmp1.display

    def __repr__(__tmp1) -> str:
        return "R:" + __tmp1.display


class ImageAttach(MessageAttach):
    def __init__(__tmp1, image_url: str) :
        __tmp1.image_url = image_url

    def __tmp2(__tmp1) -> str:
        return ""

    def __repr__(__tmp1) :
        return "I:" + str(__tmp1)


class __typ5(MessageAttach):
    def __init__(__tmp1, name, lat: __typ1, long: __typ1) -> None:
        __tmp1.name = name
        __tmp1.lat = lat
        __tmp1.long = long

    def __tmp2(__tmp1) -> str:
        return __tmp1.name

    def __repr__(__tmp1) :
        return "L:" + str(__tmp1)


# This feature is not supported anymore but it still exists in the API
class __typ2(MessageAttach):
    def __init__(__tmp1, token: <FILL>) -> None:
        __tmp1.token = token

    def __tmp2(__tmp1) -> str:
        return __tmp1.token

    def __repr__(__tmp1) -> str:
        return "S:" + str(__tmp1)


EMOJI_PLACEHOLDER = "\ufffd"


class __typ3(MessageAttach):
    def __init__(__tmp1, pack_id, emoji_id: __typ1) -> None:
        __tmp1.pack_id = pack_id
        __tmp1.emoji_id = emoji_id

    def __tmp2(__tmp1) -> str:
        return EMOJI_PLACEHOLDER

    def __repr__(__tmp1) :
        return "E:" + str(__tmp1)


# Undocumented feature
class __typ0(MessageAttach):
    def __init__(__tmp1, url: str, queue: str) -> None:
        __tmp1.url = url
        __tmp1.queue = queue

    def __tmp2(__tmp1) :
        return __tmp1.url

    def __repr__(__tmp1) -> str:
        return "Q: " + str(__tmp1)


class __typ7(__typ0):
    def __init__(__tmp1, url: str) -> None:
        super().__init__(url, "linked_image")


class __typ4:
    contents: List[Union[MessageAttach, str]]

    # pyre-ignore
    def __init__(__tmp1, data: Union[list, str, MessageAttach]) -> None:
        if isinstance(data, list):
            __tmp1.contents = data
        elif isinstance(data, str):
            __tmp1.contents = [data]

    def __add__(
        __tmp1, __tmp0: Union["ComplexMessage", str, "MessageAttach"]
    ) -> "ComplexMessage":
        if isinstance(__tmp0, __typ4):
            __tmp1.contents.extend(__tmp0.contents)
        else:
            __tmp1.contents.append(__tmp0)
        return __tmp1

    def __radd__(__tmp1, __tmp0) :
        __tmp1.contents.insert(0, __tmp0)
        return __tmp1

    def __tmp2(__tmp1) -> str:
        return str(__tmp1.contents)

    def get_text(__tmp1) -> str:
        return "".join([str(part) for part in __tmp1.contents])

    def get_attachments(__tmp1) -> List[Dict[str, str]]:
        attach_list = []  # type: ignore
        mentions = {"type": "mentions", "user_ids": list(), "loci": list()}
        emojis = {"type": "emoji", "placeholder": EMOJI_PLACEHOLDER, "charmap": []}
        queued = {"type": "postprocessing", "queues": []}
        content_frag = ""
        for part in __tmp1.contents:
            if isinstance(part, __typ6):
                mentions["user_ids"].append(part.user_id)  # type: ignore
                mentions["loci"].append(  # type: ignore
                    [len(content_frag), len(part.display)]
                )
                if mentions not in attach_list:
                    attach_list.append(mentions)
            elif isinstance(part, ImageAttach):
                attach_list.append({"type": "image", "url": part.image_url})
            elif isinstance(part, __typ5):
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
            elif isinstance(part, __typ0):
                if part.queue not in queued["queues"]:
                    queued["queues"].append(part.queue)  # type: ignore
                if queued not in attach_list:
                    attach_list.append(queued)
            content_frag += str(part)
        return attach_list  # type: ignore

    def just_str(__tmp1) -> str:
        return "".join([s for s in __tmp1.contents if isinstance(s, str)])


def smart_split_complex_message(
    message: Union[__typ4, str]
) :
    if isinstance(message, __typ4):
        return message.get_text(), message.get_attachments()
    elif isinstance(message, str):
        return message, []
    else:
        raise ValueError("Message object must be a str or ComplexMessage")

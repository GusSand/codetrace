from typing import TypeAlias
__typ0 : TypeAlias = "str"
# pyre-strict
from typing import Union, List, Tuple, Dict


class __typ2:
    def __tmp3(
        __tmp0, __tmp4
    ) -> "ComplexMessage":
        if isinstance(__tmp4, __typ3):
            __tmp4.contents.insert(0, __tmp0)
            return __tmp4
        else:
            return __typ3([__tmp0, __tmp4])

    def __tmp2(__tmp0, __tmp4) :
        return __typ3([__tmp4, __tmp0])


class RefAttach(__typ2):
    def __init__(__tmp0, user_id: __typ0, display: __typ0 = "") :
        __tmp0.display = display
        __tmp0.user_id = user_id

    def __tmp8(__tmp0) :
        return __tmp0.display

    def __tmp7(__tmp0) -> __typ0:
        return "R:" + __tmp0.display


class ImageAttach(__typ2):
    def __init__(__tmp0, image_url: __typ0) :
        __tmp0.image_url = image_url

    def __tmp8(__tmp0) -> __typ0:
        return ""

    def __tmp7(__tmp0) :
        return "I:" + __typ0(__tmp0)


class LocationAttach(__typ2):
    def __init__(__tmp0, name, lat: int, long: int) -> None:
        __tmp0.name = name
        __tmp0.lat = lat
        __tmp0.long = long

    def __tmp8(__tmp0) :
        return __tmp0.name

    def __tmp7(__tmp0) -> __typ0:
        return "L:" + __typ0(__tmp0)


# This feature is not supported anymore but it still exists in the API
class SplitAttach(__typ2):
    def __init__(__tmp0, token: __typ0) -> None:
        __tmp0.token = token

    def __tmp8(__tmp0) -> __typ0:
        return __tmp0.token

    def __tmp7(__tmp0) :
        return "S:" + __typ0(__tmp0)


EMOJI_PLACEHOLDER = "\ufffd"


class EmojiAttach(__typ2):
    def __init__(__tmp0, pack_id: <FILL>, emoji_id: int) :
        __tmp0.pack_id = pack_id
        __tmp0.emoji_id = emoji_id

    def __tmp8(__tmp0) -> __typ0:
        return EMOJI_PLACEHOLDER

    def __tmp7(__tmp0) -> __typ0:
        return "E:" + __typ0(__tmp0)


# Undocumented feature
class __typ1(__typ2):
    def __init__(__tmp0, url, queue) -> None:
        __tmp0.url = url
        __tmp0.queue = queue

    def __tmp8(__tmp0) -> __typ0:
        return __tmp0.url

    def __tmp7(__tmp0) -> __typ0:
        return "Q: " + __typ0(__tmp0)


class LinkedImageAttach(__typ1):
    def __init__(__tmp0, url) -> None:
        super().__init__(url, "linked_image")


class __typ3:
    contents: List[Union[__typ2, __typ0]]

    # pyre-ignore
    def __init__(__tmp0, __tmp1: Union[list, __typ0, __typ2]) :
        if isinstance(__tmp1, list):
            __tmp0.contents = __tmp1
        elif isinstance(__tmp1, __typ0):
            __tmp0.contents = [__tmp1]

    def __tmp3(
        __tmp0, __tmp4: Union["ComplexMessage", __typ0, "MessageAttach"]
    ) -> "ComplexMessage":
        if isinstance(__tmp4, __typ3):
            __tmp0.contents.extend(__tmp4.contents)
        else:
            __tmp0.contents.append(__tmp4)
        return __tmp0

    def __tmp2(__tmp0, __tmp4: Union[__typ0, "MessageAttach"]) :
        __tmp0.contents.insert(0, __tmp4)
        return __tmp0

    def __tmp8(__tmp0) :
        return __typ0(__tmp0.contents)

    def get_text(__tmp0) :
        return "".join([__typ0(part) for part in __tmp0.contents])

    def get_attachments(__tmp0) :
        attach_list = []  # type: ignore
        mentions = {"type": "mentions", "user_ids": list(), "loci": list()}
        emojis = {"type": "emoji", "placeholder": EMOJI_PLACEHOLDER, "charmap": []}
        queued = {"type": "postprocessing", "queues": []}
        content_frag = ""
        for part in __tmp0.contents:
            if isinstance(part, RefAttach):
                mentions["user_ids"].append(part.user_id)  # type: ignore
                mentions["loci"].append(  # type: ignore
                    [len(content_frag), len(part.display)]
                )
                if mentions not in attach_list:
                    attach_list.append(mentions)
            elif isinstance(part, ImageAttach):
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
            elif isinstance(part, EmojiAttach):
                emojis["charmap"].append([part.pack_id, part.emoji_id])  # type: ignore
                if emojis not in attach_list:
                    attach_list.append(emojis)
            elif isinstance(part, __typ1):
                if part.queue not in queued["queues"]:
                    queued["queues"].append(part.queue)  # type: ignore
                if queued not in attach_list:
                    attach_list.append(queued)
            content_frag += __typ0(part)
        return attach_list  # type: ignore

    def __tmp5(__tmp0) -> __typ0:
        return "".join([s for s in __tmp0.contents if isinstance(s, __typ0)])


def __tmp6(
    message
) :
    if isinstance(message, __typ3):
        return message.get_text(), message.get_attachments()
    elif isinstance(message, __typ0):
        return message, []
    else:
        raise ValueError("Message object must be a str or ComplexMessage")

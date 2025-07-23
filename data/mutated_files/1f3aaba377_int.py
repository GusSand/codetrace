from typing import TypeAlias
__typ3 : TypeAlias = "str"
# pyre-strict
from typing import Union, List, Tuple, Dict


class MessageAttach:
    def __tmp2(
        __tmp1, __tmp3
    ) -> "ComplexMessage":
        if isinstance(__tmp3, ComplexMessage):
            __tmp3.contents.insert(0, __tmp1)
            return __tmp3
        else:
            return ComplexMessage([__tmp1, __tmp3])

    def __radd__(__tmp1, __tmp3) -> "ComplexMessage":
        return ComplexMessage([__tmp3, __tmp1])


class RefAttach(MessageAttach):
    def __init__(__tmp1, user_id: __typ3, display: __typ3 = "") :
        __tmp1.display = display
        __tmp1.user_id = user_id

    def __tmp6(__tmp1) -> __typ3:
        return __tmp1.display

    def __tmp5(__tmp1) -> __typ3:
        return "R:" + __tmp1.display


class __typ4(MessageAttach):
    def __init__(__tmp1, image_url: __typ3) -> None:
        __tmp1.image_url = image_url

    def __tmp6(__tmp1) -> __typ3:
        return ""

    def __tmp5(__tmp1) :
        return "I:" + __typ3(__tmp1)


class __typ1(MessageAttach):
    def __init__(__tmp1, name: __typ3, lat: <FILL>, long) -> None:
        __tmp1.name = name
        __tmp1.lat = lat
        __tmp1.long = long

    def __tmp6(__tmp1) :
        return __tmp1.name

    def __tmp5(__tmp1) :
        return "L:" + __typ3(__tmp1)


# This feature is not supported anymore but it still exists in the API
class __typ2(MessageAttach):
    def __init__(__tmp1, token: __typ3) -> None:
        __tmp1.token = token

    def __tmp6(__tmp1) :
        return __tmp1.token

    def __tmp5(__tmp1) -> __typ3:
        return "S:" + __typ3(__tmp1)


EMOJI_PLACEHOLDER = "\ufffd"


class EmojiAttach(MessageAttach):
    def __init__(__tmp1, pack_id, emoji_id) -> None:
        __tmp1.pack_id = pack_id
        __tmp1.emoji_id = emoji_id

    def __tmp6(__tmp1) -> __typ3:
        return EMOJI_PLACEHOLDER

    def __tmp5(__tmp1) -> __typ3:
        return "E:" + __typ3(__tmp1)


# Undocumented feature
class __typ0(MessageAttach):
    def __init__(__tmp1, url, queue) -> None:
        __tmp1.url = url
        __tmp1.queue = queue

    def __tmp6(__tmp1) :
        return __tmp1.url

    def __tmp5(__tmp1) :
        return "Q: " + __typ3(__tmp1)


class LinkedImageAttach(__typ0):
    def __init__(__tmp1, url) -> None:
        super().__init__(url, "linked_image")


class ComplexMessage:
    contents: List[Union[MessageAttach, __typ3]]

    # pyre-ignore
    def __init__(__tmp1, data) -> None:
        if isinstance(data, list):
            __tmp1.contents = data
        elif isinstance(data, __typ3):
            __tmp1.contents = [data]

    def __tmp2(
        __tmp1, __tmp3
    ) -> "ComplexMessage":
        if isinstance(__tmp3, ComplexMessage):
            __tmp1.contents.extend(__tmp3.contents)
        else:
            __tmp1.contents.append(__tmp3)
        return __tmp1

    def __radd__(__tmp1, __tmp3) -> "ComplexMessage":
        __tmp1.contents.insert(0, __tmp3)
        return __tmp1

    def __tmp6(__tmp1) :
        return __typ3(__tmp1.contents)

    def get_text(__tmp1) :
        return "".join([__typ3(part) for part in __tmp1.contents])

    def get_attachments(__tmp1) :
        attach_list = []  # type: ignore
        mentions = {"type": "mentions", "user_ids": list(), "loci": list()}
        emojis = {"type": "emoji", "placeholder": EMOJI_PLACEHOLDER, "charmap": []}
        queued = {"type": "postprocessing", "queues": []}
        content_frag = ""
        for part in __tmp1.contents:
            if isinstance(part, RefAttach):
                mentions["user_ids"].append(part.user_id)  # type: ignore
                mentions["loci"].append(  # type: ignore
                    [len(content_frag), len(part.display)]
                )
                if mentions not in attach_list:
                    attach_list.append(mentions)
            elif isinstance(part, __typ4):
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
            elif isinstance(part, __typ2):
                attach_list.append({"type": "split", "token": part.token})
            elif isinstance(part, EmojiAttach):
                emojis["charmap"].append([part.pack_id, part.emoji_id])  # type: ignore
                if emojis not in attach_list:
                    attach_list.append(emojis)
            elif isinstance(part, __typ0):
                if part.queue not in queued["queues"]:
                    queued["queues"].append(part.queue)  # type: ignore
                if queued not in attach_list:
                    attach_list.append(queued)
            content_frag += __typ3(part)
        return attach_list  # type: ignore

    def __tmp4(__tmp1) :
        return "".join([s for s in __tmp1.contents if isinstance(s, __typ3)])


def smart_split_complex_message(
    __tmp0
) :
    if isinstance(__tmp0, ComplexMessage):
        return __tmp0.get_text(), __tmp0.get_attachments()
    elif isinstance(__tmp0, __typ3):
        return __tmp0, []
    else:
        raise ValueError("Message object must be a str or ComplexMessage")

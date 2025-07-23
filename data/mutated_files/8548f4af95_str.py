from typing import TypeAlias
__typ1 : TypeAlias = "int"
# pyre-strict
from typing import Union, List, Tuple, Dict


class MessageAttach:
    def __add__(
        self, other
    ) -> "ComplexMessage":
        if isinstance(other, __typ4):
            other.contents.insert(0, self)
            return other
        else:
            return __typ4([self, other])

    def __radd__(self, other) :
        return __typ4([other, self])


class RefAttach(MessageAttach):
    def __init__(self, user_id: <FILL>, display: str = "") -> None:
        self.display = display
        self.user_id = user_id

    def __str__(self) :
        return self.display

    def __repr__(self) :
        return "R:" + self.display


class ImageAttach(MessageAttach):
    def __init__(self, image_url) :
        self.image_url = image_url

    def __str__(self) :
        return ""

    def __repr__(self) :
        return "I:" + str(self)


class __typ3(MessageAttach):
    def __init__(self, name, lat, long) :
        self.name = name
        self.lat = lat
        self.long = long

    def __str__(self) :
        return self.name

    def __repr__(self) :
        return "L:" + str(self)


# This feature is not supported anymore but it still exists in the API
class __typ2(MessageAttach):
    def __init__(self, token) -> None:
        self.token = token

    def __str__(self) :
        return self.token

    def __repr__(self) :
        return "S:" + str(self)


EMOJI_PLACEHOLDER = "\ufffd"


class __typ5(MessageAttach):
    def __init__(self, pack_id, emoji_id) :
        self.pack_id = pack_id
        self.emoji_id = emoji_id

    def __str__(self) :
        return EMOJI_PLACEHOLDER

    def __repr__(self) :
        return "E:" + str(self)


# Undocumented feature
class __typ0(MessageAttach):
    def __init__(self, url, queue) :
        self.url = url
        self.queue = queue

    def __str__(self) :
        return self.url

    def __repr__(self) :
        return "Q: " + str(self)


class LinkedImageAttach(__typ0):
    def __init__(self, url) :
        super().__init__(url, "linked_image")


class __typ4:
    contents: List[Union[MessageAttach, str]]

    # pyre-ignore
    def __init__(self, data) -> None:
        if isinstance(data, list):
            self.contents = data
        elif isinstance(data, str):
            self.contents = [data]

    def __add__(
        self, other
    ) :
        if isinstance(other, __typ4):
            self.contents.extend(other.contents)
        else:
            self.contents.append(other)
        return self

    def __radd__(self, other) :
        self.contents.insert(0, other)
        return self

    def __str__(self) :
        return str(self.contents)

    def get_text(self) :
        return "".join([str(part) for part in self.contents])

    def get_attachments(self) :
        attach_list = []  # type: ignore
        mentions = {"type": "mentions", "user_ids": list(), "loci": list()}
        emojis = {"type": "emoji", "placeholder": EMOJI_PLACEHOLDER, "charmap": []}
        queued = {"type": "postprocessing", "queues": []}
        content_frag = ""
        for part in self.contents:
            if isinstance(part, RefAttach):
                mentions["user_ids"].append(part.user_id)  # type: ignore
                mentions["loci"].append(  # type: ignore
                    [len(content_frag), len(part.display)]
                )
                if mentions not in attach_list:
                    attach_list.append(mentions)
            elif isinstance(part, ImageAttach):
                attach_list.append({"type": "image", "url": part.image_url})
            elif isinstance(part, __typ3):
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
            elif isinstance(part, __typ5):
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

    def just_str(self) :
        return "".join([s for s in self.contents if isinstance(s, str)])


def smart_split_complex_message(
    __tmp0
) :
    if isinstance(__tmp0, __typ4):
        return __tmp0.get_text(), __tmp0.get_attachments()
    elif isinstance(__tmp0, str):
        return __tmp0, []
    else:
        raise ValueError("Message object must be a str or ComplexMessage")

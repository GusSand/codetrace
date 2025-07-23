

class RequestResponseCallbacks:
    def __init__(__tmp2):
        __tmp2.data = {}
        __tmp2.meta = {}

    def __tmp1(__tmp2):
        pass

    def on_url(__tmp2, url):
        __tmp2.data["url"] = url.decode("utf-8")

    def on_header(__tmp2, name, value):
        key = name.decode("utf-8")
        val = value.decode("utf-8")
        if not "headers" in __tmp2.data:
            __tmp2.data["headers"] = {}
        if key in __tmp2.data["headers"] and __tmp2.data["headers"][key].__class__.__name__ == "list":
            l = __tmp2.data["headers"][key]
            l.append(val)
            __tmp2.data["headers"][key] = l
        elif key in __tmp2.data["headers"]:
            l = [__tmp2.data["headers"][key], val]
            __tmp2.data["headers"][key] = l
        else:
            __tmp2.data["headers"][key] = val

    def on_header_field(__tmp2):
        pass

    def on_headers_complete(__tmp2):
        pass

    def on_body(__tmp2, __tmp0: <FILL>):
        if "body" not in __tmp2.data:
            __tmp2.data["body"] = bytearray()
        __tmp2.data["body"].extend(__tmp0)

    def on_message_complete(__tmp2):
        pass

    def on_chunk_header(__tmp2):
        pass

    def on_chunk_complete(__tmp2):
        pass

    def on_status(__tmp2, status):
        s_status = status.decode("utf-8")
        __tmp2.meta["status_text"] = s_status
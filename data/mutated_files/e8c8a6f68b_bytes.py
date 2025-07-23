

class RequestResponseCallbacks:
    def __tmp5(__tmp1):
        __tmp1.data = {}
        __tmp1.meta = {}

    def __tmp8(__tmp1):
        pass

    def __tmp2(__tmp1, url: bytes):
        __tmp1.data["url"] = url.decode("utf-8")

    def __tmp4(__tmp1, name: <FILL>, __tmp3: bytes):
        key = name.decode("utf-8")
        val = __tmp3.decode("utf-8")
        if not "headers" in __tmp1.data:
            __tmp1.data["headers"] = {}
        if key in __tmp1.data["headers"] and __tmp1.data["headers"][key].__class__.__name__ == "list":
            l = __tmp1.data["headers"][key]
            l.append(val)
            __tmp1.data["headers"][key] = l
        elif key in __tmp1.data["headers"]:
            l = [__tmp1.data["headers"][key], val]
            __tmp1.data["headers"][key] = l
        else:
            __tmp1.data["headers"][key] = val

    def __tmp9(__tmp1):
        pass

    def on_headers_complete(__tmp1):
        pass

    def on_body(__tmp1, __tmp0):
        if "body" not in __tmp1.data:
            __tmp1.data["body"] = bytearray()
        __tmp1.data["body"].extend(__tmp0)

    def on_message_complete(__tmp1):
        pass

    def __tmp6(__tmp1):
        pass

    def __tmp7(__tmp1):
        pass

    def on_status(__tmp1, status: bytes):
        s_status = status.decode("utf-8")
        __tmp1.meta["status_text"] = s_status
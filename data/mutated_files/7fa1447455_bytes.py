

class RequestResponseCallbacks:
    def __tmp10(__tmp2):
        __tmp2.data = {}
        __tmp2.meta = {}

    def __tmp13(__tmp2):
        pass

    def __tmp3(__tmp2, __tmp7):
        __tmp2.data["url"] = __tmp7.decode("utf-8")

    def __tmp6(__tmp2, __tmp15, __tmp5: <FILL>):
        key = __tmp15.decode("utf-8")
        val = __tmp5.decode("utf-8")
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

    def __tmp14(__tmp2):
        pass

    def __tmp8(__tmp2):
        pass

    def on_body(__tmp2, __tmp0):
        if "body" not in __tmp2.data:
            __tmp2.data["body"] = bytearray()
        __tmp2.data["body"].extend(__tmp0)

    def __tmp4(__tmp2):
        pass

    def __tmp11(__tmp2):
        pass

    def __tmp12(__tmp2):
        pass

    def __tmp9(__tmp2, __tmp1):
        s_status = __tmp1.decode("utf-8")
        __tmp2.meta["status_text"] = s_status
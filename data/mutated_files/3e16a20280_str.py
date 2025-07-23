from django.conf import settings
import codecs
import hashlib
import hmac

def __tmp0(__tmp1: str) -> str:
    encoded_url = __tmp1.encode("utf-8")
    encoded_camo_key = settings.CAMO_KEY.encode("utf-8")
    digest = hmac.new(encoded_camo_key, encoded_url, hashlib.sha1).hexdigest()
    hex_encoded_url = codecs.encode(encoded_url, "hex")  # type: ignore # https://github.com/python/typeshed/issues/300
    return "%s/%s" % (digest, hex_encoded_url.decode("utf-8"))

# Encodes the provided URL using the same algorithm used by the camo
# caching https image proxy
def __tmp2(__tmp1: <FILL>) :
    # Only encode the url if Camo is enabled
    if settings.CAMO_URI == '':
        return __tmp1
    return "%s%s" % (settings.CAMO_URI, __tmp0(__tmp1))

from typing import TypeAlias
__typ0 : TypeAlias = "int"
from secrets import token_bytes
from typing import Tuple

def __tmp4(__tmp1) -> __typ0:
    # generate length random bytes
    tb: bytes = token_bytes(__tmp1)
    return __typ0.from_bytes(tb, "big")

def encrypt(__tmp2: <FILL>) -> Tuple[__typ0, __typ0]:
    original_bytes: bytes = __tmp2.encode()
    dummy: __typ0 = __tmp4(len(original_bytes))
    original_key: __typ0 = __typ0.from_bytes(original_bytes, "big")
    encrypted: __typ0 = original_key ^ dummy  # XOR Gate
    return dummy, encrypted

def decrypt(__tmp0: __typ0, __tmp3: __typ0) :
    decrypted: __typ0 = __tmp0 ^ __tmp3
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    return temp.decode()

if __name__ == "__main__":
    __tmp0, __tmp3 = encrypt("Pad One Time")
    result: str = decrypt(__tmp0, __tmp3)
    print(result)

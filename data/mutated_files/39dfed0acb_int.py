from typing import TypeAlias
__typ0 : TypeAlias = "str"
from secrets import token_bytes
from typing import Tuple

def __tmp4(length) -> int:
    # generate length random bytes
    tb: bytes = token_bytes(length)
    return int.from_bytes(tb, "big")

def encrypt(__tmp2: __typ0) -> Tuple[int, int]:
    original_bytes: bytes = __tmp2.encode()
    dummy: int = __tmp4(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    encrypted: int = original_key ^ dummy  # XOR Gate
    return dummy, encrypted

def __tmp1(__tmp0: int, __tmp3: <FILL>) -> __typ0:
    decrypted: int = __tmp0 ^ __tmp3
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    return temp.decode()

if __name__ == "__main__":
    __tmp0, __tmp3 = encrypt("Pad One Time")
    result: __typ0 = __tmp1(__tmp0, __tmp3)
    print(result)

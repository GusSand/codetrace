from typing import TypeAlias
__typ0 : TypeAlias = "str"
from secrets import token_bytes
from typing import Tuple

def random_key(__tmp2: <FILL>) -> int:
    # generate length random bytes
    tb: bytes = token_bytes(__tmp2)
    return int.from_bytes(tb, "big")

def __tmp0(__tmp3) :
    original_bytes: bytes = __tmp3.encode()
    dummy: int = random_key(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    encrypted: int = original_key ^ dummy  # XOR Gate
    return dummy, encrypted

def decrypt(__tmp1, __tmp4) :
    decrypted: int = __tmp1 ^ __tmp4
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    return temp.decode()

if __name__ == "__main__":
    __tmp1, __tmp4 = __tmp0("Pad One Time")
    result: __typ0 = decrypt(__tmp1, __tmp4)
    print(result)

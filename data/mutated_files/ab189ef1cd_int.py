from secrets import token_bytes
from typing import Tuple

def __tmp0(length: int) -> int:
    # generate length random bytes
    tb: bytes = token_bytes(length)
    return int.from_bytes(tb, "big")

def encrypt(__tmp1: str) :
    original_bytes: bytes = __tmp1.encode()
    dummy: int = __tmp0(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    encrypted: int = original_key ^ dummy  # XOR Gate
    return dummy, encrypted

def __tmp3(__tmp2: <FILL>, key2: int) -> str:
    decrypted: int = __tmp2 ^ key2
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    return temp.decode()

if __name__ == "__main__":
    __tmp2, key2 = encrypt("Pad One Time")
    result: str = __tmp3(__tmp2, key2)
    print(result)

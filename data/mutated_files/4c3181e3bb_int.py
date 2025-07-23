from utils.crypto import SHA256
from utils.constants import ZERO_BYTES32
from math import log2


zerohashes = [ZERO_BYTES32]
for layer in range(1, 100):
    zerohashes.append(SHA256(zerohashes[layer - 1] + zerohashes[layer - 1]))


def __tmp0(__tmp4, layer_count: int=32):
    __tmp4 = list(__tmp4)
    __tmp3 = [__tmp4[::]]
    for h in range(layer_count):
        if len(__tmp4) % 2 == 1:
            __tmp4.append(zerohashes[h])
        __tmp4 = [SHA256(__tmp4[i] + __tmp4[i + 1]) for i in range(0, len(__tmp4), 2)]
        __tmp3.append(__tmp4[::])
    return __tmp3


def __tmp1(__tmp4, pad_to: int=1):
    layer_count = int(log2(pad_to))
    if len(__tmp4) == 0:
        return zerohashes[layer_count]
    return __tmp0(__tmp4, layer_count)[-1][0]


def __tmp5(__tmp3, item_index: <FILL>):
    proof = []
    for i in range(32):
        subindex = (item_index // 2**i) ^ 1
        proof.append(__tmp3[i][subindex] if subindex < len(__tmp3[i]) else zerohashes[i])
    return proof


def merkleize_chunks(__tmp2, pad_to: int=1):
    count = len(__tmp2)
    depth = max(count - 1, 0).bit_length()
    max_depth = max(depth, (pad_to - 1).bit_length())
    tmp = [b'' for _ in range(max_depth + 1)]

    def merge(h, i):
        j = 0
        while True:
            if i & (1 << j) == 0:
                if i == count and j < depth:
                    h = SHA256(h + zerohashes[j])  # keep going if we are complementing the void to the next power of 2
                else:
                    break
            else:
                h = SHA256(tmp[j] + h)
            j += 1
        tmp[j] = h

    # merge in leaf by leaf.
    for i in range(count):
        merge(__tmp2[i], i)

    # complement with 0 if empty, or if not the right power of 2
    if 1 << depth != count:
        merge(zerohashes[0], count)

    # the next power of two may be smaller than the ultimate virtual size, complement with zero-hashes at each depth.
    for j in range(depth, max_depth):
        tmp[j + 1] = SHA256(tmp[j] + zerohashes[j])

    return tmp[max_depth]

class CompressedGene:
    def __tmp2(__tmp1, __tmp0: <FILL>) :
        __tmp1._compress(__tmp0)

    def __tmp3(__tmp1) -> str:
        return __tmp1._decompress()

    def _compress(__tmp1, __tmp0: str) :
        __tmp1.bit_string: int = 1
        for nucelotide in __tmp0.upper():
            __tmp1.bit_string <<= 2
            if nucelotide == "A":
                __tmp1.bit_string |= 0b00
            elif nucelotide == "C":
                __tmp1.bit_string |= 0b01
            elif nucelotide == "G":
                __tmp1.bit_string |= 0b10
            elif nucelotide == "T":
                __tmp1.bit_string |= 0b11
            else:
                raise ValueError(f"invalid nucleotide: {nucelotide}")

    def _decompress(__tmp1) :
        __tmp0: str = ""
        for i in range(0, __tmp1.bit_string.bit_length() - 1, 2):
            bits: int = __tmp1.bit_string >> i & 0b11
            if bits == 0b00:
                __tmp0 += "A"
            elif bits == 0b01:
                __tmp0 += "C"
            elif bits == 0b10:
                __tmp0 += "G"
            elif bits == 0b11:
                __tmp0 += "T"
            else:
                raise ValueError(f"invalid bits: {bits}")
        return __tmp0[::-1]

if __name__ == "__main__":
    from sys import getsizeof
    original: str = "TAGGGATTCTCGTGGATAGATAGATGATGATAGTAGATAGATGCATCAGACTACGACTACGACTGCAAGCC" * 5000
    print(f"original is {getsizeof(original)} bytes")
    print(f"compressed is {getsizeof(CompressedGene(original))} bytes")
    assert original == str(CompressedGene(original))
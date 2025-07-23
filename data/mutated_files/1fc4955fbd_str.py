class __typ0:
    def __init__(self, gene) :
        self._compress(gene)

    def __tmp0(self) :
        return self._decompress()

    def _compress(self, gene: <FILL>) :
        self.bit_string: int = 1
        for nucelotide in gene.upper():
            self.bit_string <<= 2
            if nucelotide == "A":
                self.bit_string |= 0b00
            elif nucelotide == "C":
                self.bit_string |= 0b01
            elif nucelotide == "G":
                self.bit_string |= 0b10
            elif nucelotide == "T":
                self.bit_string |= 0b11
            else:
                raise ValueError(f"invalid nucleotide: {nucelotide}")

    def _decompress(self) :
        gene: str = ""
        for i in range(0, self.bit_string.bit_length() - 1, 2):
            bits: int = self.bit_string >> i & 0b11
            if bits == 0b00:
                gene += "A"
            elif bits == 0b01:
                gene += "C"
            elif bits == 0b10:
                gene += "G"
            elif bits == 0b11:
                gene += "T"
            else:
                raise ValueError(f"invalid bits: {bits}")
        return gene[::-1]

if __name__ == "__main__":
    from sys import getsizeof
    original: str = "TAGGGATTCTCGTGGATAGATAGATGATGATAGTAGATAGATGCATCAGACTACGACTACGACTGCAAGCC" * 5000
    print(f"original is {getsizeof(original)} bytes")
    print(f"compressed is {getsizeof(__typ0(original))} bytes")
    assert original == str(__typ0(original))
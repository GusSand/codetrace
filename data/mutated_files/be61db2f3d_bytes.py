from typing import TypeAlias
__typ1 : TypeAlias = "int"
from protoactor.сluster.hash_algorithms.fnv1a32 import FNV1A32

is_import = False
if is_import:
    from protoactor.сluster.member_strategy import AbstractMemberStrategy


class __typ0:
    def __init__(__tmp1, member_strategy):
        __tmp1._member_strategy = member_strategy
        __tmp1._hash_algorithm = FNV1A32()
        __tmp1._member_hashes = None
        __tmp1.update_rdv()

    def __tmp2(__tmp1, __tmp0: str):
        members = __tmp1._member_strategy.get_all_members()
        if members is None or len(members) == 0:
            return ''

        if len(members) == 1:
            return members[0].address

        key_bytes = __tmp0.encode()
        max_score = 0
        max_node = None

        for i in range(len(members)):
            member = members[i]
            if member.alive:
                hash_bytes = __tmp1._member_hashes[i]
                score = __tmp1._rdv_hash(hash_bytes, key_bytes)
                if score > max_score:
                    max_score = score
                    max_node = member

        if max_node is None:
            return ''
        else:
            return max_node.address

    def update_rdv(__tmp1):
        __tmp1._member_hashes = [member.address.encode() for member in __tmp1._member_strategy.get_all_members()]

    def _rdv_hash(__tmp1, __tmp3: bytes, __tmp0: <FILL>) -> __typ1:
        hash_bytes = __tmp0 + __tmp3
        return __tmp1._hash_algorithm.compute_hash(hash_bytes)

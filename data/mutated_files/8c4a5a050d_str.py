from typing import TypeAlias
__typ1 : TypeAlias = "bytes"
from protoactor.сluster.hash_algorithms.fnv1a32 import FNV1A32

is_import = False
if is_import:
    from protoactor.сluster.member_strategy import AbstractMemberStrategy


class __typ0:
    def __tmp2(__tmp0, member_strategy):
        __tmp0._member_strategy = member_strategy
        __tmp0._hash_algorithm = FNV1A32()
        __tmp0._member_hashes = None
        __tmp0.update_rdv()

    def __tmp1(__tmp0, __tmp4: <FILL>):
        members = __tmp0._member_strategy.get_all_members()
        if members is None or len(members) == 0:
            return ''

        if len(members) == 1:
            return members[0].address

        key_bytes = __tmp4.encode()
        max_score = 0
        max_node = None

        for i in range(len(members)):
            member = members[i]
            if member.alive:
                hash_bytes = __tmp0._member_hashes[i]
                score = __tmp0._rdv_hash(hash_bytes, key_bytes)
                if score > max_score:
                    max_score = score
                    max_node = member

        if max_node is None:
            return ''
        else:
            return max_node.address

    def update_rdv(__tmp0):
        __tmp0._member_hashes = [member.address.encode() for member in __tmp0._member_strategy.get_all_members()]

    def _rdv_hash(__tmp0, __tmp3: __typ1, __tmp4: __typ1) :
        hash_bytes = __tmp4 + __tmp3
        return __tmp0._hash_algorithm.compute_hash(hash_bytes)

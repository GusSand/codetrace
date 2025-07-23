from typing import TypeAlias
__typ0 : TypeAlias = "int"
from argparse import ArgumentParser
from typing import (
    List,
    Union,
    Dict,
)
from ssz import (
    Serializable,
    bytes32,
    bytes48,
    bytes96,
    uint64,
)
import json

from key_derivation.mnemonic import get_mnemonic
from key_derivation.path import mnemonic_and_path_to_key
from keystores import ScryptKeystore
from utils.bls import (
    bls_sign,
    bls_priv_to_pub,
)
from utils.crypto import SHA256


def get_args():
    parser = ArgumentParser(description='🦄 : the validator deposit assistant')
    parser.add_argument('--num_validators', type=__typ0, required=True, help='Number of Eth2 validator instances to create. (Each requires a 32 Eth deposit)')  # noqa: E501
    parser.add_argument('--mnemonic_pwd', default='', type=str, help='Add an additional security to your mnemonic by using a password. (Not reccomended)')  # noqa: E501
    parser.add_argument('--save_withdrawal_keys', action='store_true', help='Saves withdrawal keys as keystores')  # noqa: E501

    args = parser.parse_args()
    return args


def __tmp3() :
    mnemonic = get_mnemonic()
    print('Below is your seed phrase. Write it down and store it in a safe place. It is the ONLY way to withdraw your funds.')  # noqa: E501
    print('\n\n\n\n%s\n\n\n\n' % mnemonic)
    input("Press Enter when you have written down your mnemonic.")
    return mnemonic


def __tmp7(mnemonic, __tmp6: <FILL>, num_validators) :
    __tmp1 = [{
        'withdrawal_path': 'm/12381/3600/%s/0' % i,
        'withdrawal_sk': mnemonic_and_path_to_key(mnemonic, __tmp6, 'm/12381/3600/%s/0' % i),
        'signing_path': 'm/12381/3600/%s/0/0' % i,
        'signing_sk': mnemonic_and_path_to_key(mnemonic, __tmp6, 'm/12381/3600/%s/0/0' % i),
        'amount': 32 * 10**9,
    } for i in range(num_validators)]
    return __tmp1


def __tmp8(__tmp1, folder: str='./', save_withdrawal_keys: bool=False):
    def __tmp2(__tmp4):
        __tmp6 = input('Enter the password that secures your %s keys.' % __tmp4)
        confirm_password = input('Type your password again to confirm.')
        while __tmp6 != confirm_password:
            print("\n Your passwords didn't match, please try again.\n")
            __tmp6 = input('Enter the password that secures your %s keys.' % __tmp4)
            confirm_password = input('Type your password again to confirm.')
        for credential in __tmp1:
            keystore = ScryptKeystore.encrypt(secret=__typ0(credential['%s_sk' % __tmp4]).to_bytes(32, 'big'),
                                              __tmp6=__tmp6, path=str(credential['%s_path' % __tmp4]))
            keystore.save(folder + '%s-keystore-%s.json' % (__tmp4, keystore.path.replace('/', '_')))

    __tmp2('signing')
    if save_withdrawal_keys:
        __tmp2('withdrawal')


class __typ2(Serializable):
    fields = [
        ('pubkey', bytes48),
        ('withdrawal_credentials', bytes32),
        ('amount', uint64),
    ]


class __typ1(Serializable):
    fields = [
        ('pubkey', bytes48),
        ('withdrawal_credentials', bytes32),
        ('amount', uint64),
        ('signature', bytes96)
    ]


def __tmp5(__tmp1, file: str='./deposit_data.json'):
    deposit_data = list()
    for credential in __tmp1:
        deposit_message = __typ2(
            pubkey=bls_priv_to_pub(__typ0(credential['signing_sk'])),
            withdrawal_credentials=SHA256(bls_priv_to_pub(__typ0(credential['withdrawal_sk']))),
            amount=credential['amount'],
        )

        deposit = __typ1(
            **deposit_message.as_dict(),
            signature=bls_sign(__typ0(credential['signing_sk']), deposit_message.hash_tree_root),
        )
        
        deposit_data_dict = deposit.as_dict()
        deposit_data_dict.update({'deposit_data_root':deposit.hash_tree_root})

        deposit_data.append(deposit_data_dict)
    with open(file, 'w') as f:
        json.dump(deposit_data, f, default=lambda x: x.hex())


def __tmp0():
    args = get_args()
    mnemonic = __tmp3()
    __tmp1 = __tmp7(mnemonic, args.mnemonic_pwd, args.num_validators)
    __tmp8(__tmp1, save_withdrawal_keys=args.save_withdrawal_keys)
    __tmp5(__tmp1)


if __name__ == '__main__':
    __tmp0()

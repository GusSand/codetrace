from typing import TypeAlias
__typ0 : TypeAlias = "bytes"
__typ1 : TypeAlias = "dict"
from dataclasses import (
    asdict,
    dataclass,
    fields,
    field as dataclass_field
)
import json
from secrets import randbits
from uuid import uuid4
from utils.crypto import (
    AES_128_CTR,
    PBKDF2,
    scrypt,
    SHA256,
)
from py_ecc.bls import G2ProofOfPossession as bls

hexdigits = set('0123456789abcdef')


def to_bytes(__tmp2):
    if isinstance(__tmp2, str):
        if all(c in hexdigits for c in __tmp2):
            return __typ0.fromhex(__tmp2)
    elif isinstance(__tmp2, __typ1):
        for key, value in __tmp2.items():
            __tmp2[key] = to_bytes(value)
    return __tmp2


class BytesDataclass:
    def __tmp3(__tmp1):
        for field in fields(__tmp1):
            if field.type in (__typ1, __typ0):
                __tmp1.__setattr__(field.name, to_bytes(__tmp1.__getattribute__(field.name)))

    def as_json(__tmp1) :
        return json.dumps(asdict(__tmp1), default=lambda x: x.hex())


@dataclass
class __typ2(BytesDataclass):
    function: str = ''
    params: __typ1 = dataclass_field(default_factory=__typ1)
    message: __typ0 = __typ0()


@dataclass
class KeystoreCrypto(BytesDataclass):
    kdf: __typ2 = __typ2()
    checksum: __typ2 = __typ2()
    cipher: __typ2 = __typ2()

    @classmethod
    def from_json(__tmp4, __tmp6):
        kdf = __typ2(**__tmp6['kdf'])
        checksum = __typ2(**__tmp6['checksum'])
        cipher = __typ2(**__tmp6['cipher'])
        return __tmp4(kdf=kdf, checksum=checksum, cipher=cipher)


@dataclass
class Keystore(BytesDataclass):
    crypto: KeystoreCrypto = KeystoreCrypto()
    pubkey: str = ''
    path: str = ''
    uuid: str = str(uuid4())  # Generate a new uuid
    version: int = 4

    def kdf(__tmp1, **kwargs):
        return scrypt(**kwargs) if 'scrypt' in __tmp1.crypto.kdf.function else PBKDF2(**kwargs)

    def __tmp0(__tmp1, __tmp7):
        with open(__tmp7, 'w') as f:
            f.write(__tmp1.as_json())

    @classmethod
    def open(__tmp4, __tmp7):
        with open(__tmp7, 'r') as f:
            return __tmp4.from_json(f.read())

    @classmethod
    def from_json(__tmp4, json_str: <FILL>):
        __tmp6 = json.loads(json_str)
        crypto = KeystoreCrypto.from_json(__tmp6['crypto'])
        pubkey = __tmp6['pubkey']
        path = __tmp6['path']
        uuid = __tmp6['uuid']
        version = __tmp6['version']
        return __tmp4(crypto=crypto, pubkey=pubkey, path=path, uuid=uuid, version=version)

    @classmethod
    def encrypt(__tmp4, *, secret: __typ0, __tmp5: str, path: str='',
                kdf_salt: __typ0=randbits(256).to_bytes(32, 'big'),
                aes_iv: __typ0=randbits(128).to_bytes(16, 'big')):
        keystore = __tmp4()
        keystore.crypto.kdf.params['salt'] = kdf_salt
        decryption_key = keystore.kdf(__tmp5=__tmp5, **keystore.crypto.kdf.params)
        keystore.crypto.cipher.params['iv'] = aes_iv
        cipher = AES_128_CTR(key=decryption_key[:16], **keystore.crypto.cipher.params)
        keystore.crypto.cipher.message = cipher.encrypt(secret)
        keystore.crypto.checksum.message = SHA256(decryption_key[16:32] + keystore.crypto.cipher.message)
        keystore.pubkey = bls.PrivToPub(int.from_bytes(secret, 'big')).hex()
        keystore.path = path
        return keystore

    def decrypt(__tmp1, __tmp5) :
        decryption_key = __tmp1.kdf(__tmp5=__tmp5, **__tmp1.crypto.kdf.params)
        assert SHA256(decryption_key[16:32] + __tmp1.crypto.cipher.message) == __tmp1.crypto.checksum.message
        cipher = AES_128_CTR(key=decryption_key[:16], **__tmp1.crypto.cipher.params)
        return cipher.decrypt(__tmp1.crypto.cipher.message)


@dataclass
class Pbkdf2Keystore(Keystore):
    crypto: KeystoreCrypto = KeystoreCrypto(
        kdf=__typ2(
            function='pbkdf2',
            params={
                'c': 2**18,
                'dklen': 32,
                "prf": 'hmac-sha256'
            },
        ),
        checksum=__typ2(
            function='sha256',
        ),
        cipher=__typ2(
            function='aes-128-ctr',
        )
    )


@dataclass
class ScryptKeystore(Keystore):
    crypto: KeystoreCrypto = KeystoreCrypto(
        kdf=__typ2(
            function='scrypt',
            params={
                'dklen': 32,
                'n': 2**18,
                'r': 8,
                'p': 1,
            },
        ),
        checksum=__typ2(
            function='sha256',
        ),
        cipher=__typ2(
            function='aes-128-ctr',
        )
    )

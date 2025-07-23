from typing import TypeAlias
__typ2 : TypeAlias = "dict"
__typ4 : TypeAlias = "bytes"
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


def to_bytes(__tmp3):
    if isinstance(__tmp3, str):
        if all(c in hexdigits for c in __tmp3):
            return __typ4.fromhex(__tmp3)
    elif isinstance(__tmp3, __typ2):
        for key, value in __tmp3.items():
            __tmp3[key] = to_bytes(value)
    return __tmp3


class BytesDataclass:
    def __tmp4(__tmp2):
        for field in fields(__tmp2):
            if field.type in (__typ2, __typ4):
                __tmp2.__setattr__(field.name, to_bytes(__tmp2.__getattribute__(field.name)))

    def as_json(__tmp2) :
        return json.dumps(asdict(__tmp2), default=lambda x: x.hex())


@dataclass
class KeystoreModule(BytesDataclass):
    function: str = ''
    params: __typ2 = dataclass_field(default_factory=__typ2)
    message: __typ4 = __typ4()


@dataclass
class __typ1(BytesDataclass):
    kdf: KeystoreModule = KeystoreModule()
    checksum: KeystoreModule = KeystoreModule()
    cipher: KeystoreModule = KeystoreModule()

    @classmethod
    def from_json(__tmp5, __tmp7):
        kdf = KeystoreModule(**__tmp7['kdf'])
        checksum = KeystoreModule(**__tmp7['checksum'])
        cipher = KeystoreModule(**__tmp7['cipher'])
        return __tmp5(kdf=kdf, checksum=checksum, cipher=cipher)


@dataclass
class Keystore(BytesDataclass):
    crypto: __typ1 = __typ1()
    pubkey: str = ''
    path: str = ''
    uuid: str = str(uuid4())  # Generate a new uuid
    version: int = 4

    def kdf(__tmp2, **kwargs):
        return scrypt(**kwargs) if 'scrypt' in __tmp2.crypto.kdf.function else PBKDF2(**kwargs)

    def __tmp1(__tmp2, __tmp8):
        with open(__tmp8, 'w') as f:
            f.write(__tmp2.as_json())

    @classmethod
    def open(__tmp5, __tmp8: <FILL>):
        with open(__tmp8, 'r') as f:
            return __tmp5.from_json(f.read())

    @classmethod
    def from_json(__tmp5, __tmp0):
        __tmp7 = json.loads(__tmp0)
        crypto = __typ1.from_json(__tmp7['crypto'])
        pubkey = __tmp7['pubkey']
        path = __tmp7['path']
        uuid = __tmp7['uuid']
        version = __tmp7['version']
        return __tmp5(crypto=crypto, pubkey=pubkey, path=path, uuid=uuid, version=version)

    @classmethod
    def encrypt(__tmp5, *, secret, __tmp6, path: str='',
                kdf_salt: __typ4=randbits(256).to_bytes(32, 'big'),
                aes_iv: __typ4=randbits(128).to_bytes(16, 'big')):
        keystore = __tmp5()
        keystore.crypto.kdf.params['salt'] = kdf_salt
        decryption_key = keystore.kdf(__tmp6=__tmp6, **keystore.crypto.kdf.params)
        keystore.crypto.cipher.params['iv'] = aes_iv
        cipher = AES_128_CTR(key=decryption_key[:16], **keystore.crypto.cipher.params)
        keystore.crypto.cipher.message = cipher.encrypt(secret)
        keystore.crypto.checksum.message = SHA256(decryption_key[16:32] + keystore.crypto.cipher.message)
        keystore.pubkey = bls.PrivToPub(int.from_bytes(secret, 'big')).hex()
        keystore.path = path
        return keystore

    def decrypt(__tmp2, __tmp6) :
        decryption_key = __tmp2.kdf(__tmp6=__tmp6, **__tmp2.crypto.kdf.params)
        assert SHA256(decryption_key[16:32] + __tmp2.crypto.cipher.message) == __tmp2.crypto.checksum.message
        cipher = AES_128_CTR(key=decryption_key[:16], **__tmp2.crypto.cipher.params)
        return cipher.decrypt(__tmp2.crypto.cipher.message)


@dataclass
class __typ3(Keystore):
    crypto: __typ1 = __typ1(
        kdf=KeystoreModule(
            function='pbkdf2',
            params={
                'c': 2**18,
                'dklen': 32,
                "prf": 'hmac-sha256'
            },
        ),
        checksum=KeystoreModule(
            function='sha256',
        ),
        cipher=KeystoreModule(
            function='aes-128-ctr',
        )
    )


@dataclass
class __typ0(Keystore):
    crypto: __typ1 = __typ1(
        kdf=KeystoreModule(
            function='scrypt',
            params={
                'dklen': 32,
                'n': 2**18,
                'r': 8,
                'p': 1,
            },
        ),
        checksum=KeystoreModule(
            function='sha256',
        ),
        cipher=KeystoreModule(
            function='aes-128-ctr',
        )
    )

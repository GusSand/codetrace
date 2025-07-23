from typing import TypeAlias
__typ0 : TypeAlias = "str"
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


def to_bytes(obj):
    if isinstance(obj, __typ0):
        if all(c in hexdigits for c in obj):
            return bytes.fromhex(obj)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = to_bytes(value)
    return obj


class BytesDataclass:
    def __post_init__(__tmp2):
        for field in fields(__tmp2):
            if field.type in (dict, bytes):
                __tmp2.__setattr__(field.name, to_bytes(__tmp2.__getattribute__(field.name)))

    def as_json(__tmp2) :
        return json.dumps(asdict(__tmp2), default=lambda x: x.hex())


@dataclass
class KeystoreModule(BytesDataclass):
    function: __typ0 = ''
    params: dict = dataclass_field(default_factory=dict)
    message: bytes = bytes()


@dataclass
class KeystoreCrypto(BytesDataclass):
    kdf: KeystoreModule = KeystoreModule()
    checksum: KeystoreModule = KeystoreModule()
    cipher: KeystoreModule = KeystoreModule()

    @classmethod
    def from_json(__tmp3, __tmp0):
        kdf = KeystoreModule(**__tmp0['kdf'])
        checksum = KeystoreModule(**__tmp0['checksum'])
        cipher = KeystoreModule(**__tmp0['cipher'])
        return __tmp3(kdf=kdf, checksum=checksum, cipher=cipher)


@dataclass
class Keystore(BytesDataclass):
    crypto: KeystoreCrypto = KeystoreCrypto()
    pubkey: __typ0 = ''
    path: __typ0 = ''
    uuid: __typ0 = __typ0(uuid4())  # Generate a new uuid
    version: int = 4

    def kdf(__tmp2, **kwargs):
        return scrypt(**kwargs) if 'scrypt' in __tmp2.crypto.kdf.function else PBKDF2(**kwargs)

    def save(__tmp2, file: __typ0):
        with open(file, 'w') as f:
            f.write(__tmp2.as_json())

    @classmethod
    def open(__tmp3, file):
        with open(file, 'r') as f:
            return __tmp3.from_json(f.read())

    @classmethod
    def from_json(__tmp3, __tmp1: __typ0):
        __tmp0 = json.loads(__tmp1)
        crypto = KeystoreCrypto.from_json(__tmp0['crypto'])
        pubkey = __tmp0['pubkey']
        path = __tmp0['path']
        uuid = __tmp0['uuid']
        version = __tmp0['version']
        return __tmp3(crypto=crypto, pubkey=pubkey, path=path, uuid=uuid, version=version)

    @classmethod
    def encrypt(__tmp3, *, secret: <FILL>, password, path: __typ0='',
                kdf_salt: bytes=randbits(256).to_bytes(32, 'big'),
                aes_iv: bytes=randbits(128).to_bytes(16, 'big')):
        keystore = __tmp3()
        keystore.crypto.kdf.params['salt'] = kdf_salt
        decryption_key = keystore.kdf(password=password, **keystore.crypto.kdf.params)
        keystore.crypto.cipher.params['iv'] = aes_iv
        cipher = AES_128_CTR(key=decryption_key[:16], **keystore.crypto.cipher.params)
        keystore.crypto.cipher.message = cipher.encrypt(secret)
        keystore.crypto.checksum.message = SHA256(decryption_key[16:32] + keystore.crypto.cipher.message)
        keystore.pubkey = bls.PrivToPub(int.from_bytes(secret, 'big')).hex()
        keystore.path = path
        return keystore

    def decrypt(__tmp2, password) :
        decryption_key = __tmp2.kdf(password=password, **__tmp2.crypto.kdf.params)
        assert SHA256(decryption_key[16:32] + __tmp2.crypto.cipher.message) == __tmp2.crypto.checksum.message
        cipher = AES_128_CTR(key=decryption_key[:16], **__tmp2.crypto.cipher.params)
        return cipher.decrypt(__tmp2.crypto.cipher.message)


@dataclass
class Pbkdf2Keystore(Keystore):
    crypto: KeystoreCrypto = KeystoreCrypto(
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
class ScryptKeystore(Keystore):
    crypto: KeystoreCrypto = KeystoreCrypto(
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

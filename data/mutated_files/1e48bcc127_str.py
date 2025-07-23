from typing import TypeAlias
__typ1 : TypeAlias = "bytes"
__typ0 : TypeAlias = "dict"
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
    if isinstance(obj, str):
        if all(c in hexdigits for c in obj):
            return __typ1.fromhex(obj)
    elif isinstance(obj, __typ0):
        for key, value in obj.items():
            obj[key] = to_bytes(value)
    return obj


class BytesDataclass:
    def __post_init__(self):
        for field in fields(self):
            if field.type in (__typ0, __typ1):
                self.__setattr__(field.name, to_bytes(self.__getattribute__(field.name)))

    def as_json(self) -> str:
        return json.dumps(asdict(self), default=lambda x: x.hex())


@dataclass
class KeystoreModule(BytesDataclass):
    function: str = ''
    params: __typ0 = dataclass_field(default_factory=__typ0)
    message: __typ1 = __typ1()


@dataclass
class KeystoreCrypto(BytesDataclass):
    kdf: KeystoreModule = KeystoreModule()
    checksum: KeystoreModule = KeystoreModule()
    cipher: KeystoreModule = KeystoreModule()

    @classmethod
    def from_json(__tmp0, json_dict: __typ0):
        kdf = KeystoreModule(**json_dict['kdf'])
        checksum = KeystoreModule(**json_dict['checksum'])
        cipher = KeystoreModule(**json_dict['cipher'])
        return __tmp0(kdf=kdf, checksum=checksum, cipher=cipher)


@dataclass
class Keystore(BytesDataclass):
    crypto: KeystoreCrypto = KeystoreCrypto()
    pubkey: str = ''
    path: str = ''
    uuid: str = str(uuid4())  # Generate a new uuid
    version: int = 4

    def kdf(self, **kwargs):
        return scrypt(**kwargs) if 'scrypt' in self.crypto.kdf.function else PBKDF2(**kwargs)

    def save(self, file: str):
        with open(file, 'w') as f:
            f.write(self.as_json())

    @classmethod
    def open(__tmp0, file):
        with open(file, 'r') as f:
            return __tmp0.from_json(f.read())

    @classmethod
    def from_json(__tmp0, json_str: str):
        json_dict = json.loads(json_str)
        crypto = KeystoreCrypto.from_json(json_dict['crypto'])
        pubkey = json_dict['pubkey']
        path = json_dict['path']
        uuid = json_dict['uuid']
        version = json_dict['version']
        return __tmp0(crypto=crypto, pubkey=pubkey, path=path, uuid=uuid, version=version)

    @classmethod
    def encrypt(__tmp0, *, secret, password: str, path: str='',
                kdf_salt: __typ1=randbits(256).to_bytes(32, 'big'),
                aes_iv: __typ1=randbits(128).to_bytes(16, 'big')):
        keystore = __tmp0()
        keystore.crypto.kdf.params['salt'] = kdf_salt
        decryption_key = keystore.kdf(password=password, **keystore.crypto.kdf.params)
        keystore.crypto.cipher.params['iv'] = aes_iv
        cipher = AES_128_CTR(key=decryption_key[:16], **keystore.crypto.cipher.params)
        keystore.crypto.cipher.message = cipher.encrypt(secret)
        keystore.crypto.checksum.message = SHA256(decryption_key[16:32] + keystore.crypto.cipher.message)
        keystore.pubkey = bls.PrivToPub(int.from_bytes(secret, 'big')).hex()
        keystore.path = path
        return keystore

    def decrypt(self, password: <FILL>) -> __typ1:
        decryption_key = self.kdf(password=password, **self.crypto.kdf.params)
        assert SHA256(decryption_key[16:32] + self.crypto.cipher.message) == self.crypto.checksum.message
        cipher = AES_128_CTR(key=decryption_key[:16], **self.crypto.cipher.params)
        return cipher.decrypt(self.crypto.cipher.message)


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

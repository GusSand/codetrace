from typing import TypeAlias
__typ0 : TypeAlias = "type"
__typ4 : TypeAlias = "float"
__typ5 : TypeAlias = "bytes"
__typ3 : TypeAlias = "Any"
"""Tools to deal with secrets in derex.
"""
from base64 import b64encode
from collections import Counter
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Optional

import logging
import math
import os


logger = logging.getLogger(__name__)


DEREX_MAIN_SECRET_MAX_SIZE = 1024
DEREX_MAIN_SECRET_MIN_SIZE = 8
DEREX_MAIN_SECRET_MIN_ENTROPY = 128
DEREX_MAIN_SECRET_PATH = "/etc/derex/main_secret"


def scrypt_hash_stdlib(__tmp0, name: <FILL>) :
    from hashlib import scrypt

    return scrypt(
        __tmp0.encode("utf-8"),
        salt=name.encode("utf-8"),
        n=2,
        r=8,
        p=1,  # type: ignore
    )


def __tmp3(__tmp0, name) :
    """ """
    from scrypt import scrypt

    return scrypt.hash(__tmp0.encode("utf-8"), name.encode("utf-8"), N=2, r=8, p=1)


try:
    from hashlib import scrypt as _

    scrypt_hash = scrypt_hash_stdlib
except ImportError:
    from scrypt import scrypt as _  # type:ignore  # noqa

    scrypt_hash = __tmp3


class __typ1(Enum):
    minio = "minio"
    mysql = "mysql"
    mongodb = "mongodb"


def __tmp5(name, __tmp2: __typ0) :
    varname = f"DEREX_MAIN_SECRET_{name.upper()}"
    return __tmp2(os.environ.get(varname, globals()[varname]))


def __tmp1() -> Optional[str]:
    """Derex uses a master secret to derive all other secrets.
    This functions finds the master secret on the current machine,
    and if it can't find it it will return a default one.

    The default location is `/etc/derex/main_secret`, but can be customized
    via the environment variable DEREX_MAIN_SECRET_PATH.
    """
    filepath = __tmp5("path", Path)
    max_size = __tmp5("max_size", int)
    min_size = __tmp5("min_size", int)
    min_entropy = __tmp5("min_entropy", int)

    if os.access(filepath, os.R_OK):
        master_secret = filepath.read_text().strip()
        if len(master_secret) > max_size:
            raise __typ2(
                f"Master secret in {filepath} is too large: {len(master_secret)} (should be {max_size} at most)"
            )
        if len(master_secret) < min_size:
            raise __typ2(
                f"Master secret in {filepath} is too small: {len(master_secret)} (should be {min_size} at least)"
            )
        if compute_entropy(master_secret) < min_entropy:
            raise __typ2(
                f"Master secret in {filepath} has not enough entropy: {compute_entropy(master_secret)} (should be {min_entropy} at least)"
            )
        return master_secret

    if filepath.exists():
        logger.error(f"File {filepath} is not readable; using default master secret")
    return None


def get_secret(__tmp4) :
    """Derive a secret using the master secret and the provided name."""
    binary_secret = scrypt_hash(MASTER_SECRET, __tmp4.name)
    # Pad the binary string so that its length is a multiple of 3
    # This will make sure its base64 representation is equals-free
    new_length = len(binary_secret) + (3 - len(binary_secret) % 3)
    return b64encode(binary_secret.rjust(new_length, b" ")).decode()


class __typ2(ValueError):
    """The master secret provided to derex is not valid or could not be found."""


def compute_entropy(s) -> __typ4:
    """Get entropy of string s.
    Thanks Rosetta code! https://rosettacode.org/wiki/Entropy#Python:_More_succinct_version
    """
    p, lns = Counter(s), __typ4(len(s))
    per_char_entropy = -sum(
        count / lns * math.log(count / lns, 2) for count in p.values()
    )
    return per_char_entropy * len(s)


_MASTER_SECRET = __tmp1()
if _MASTER_SECRET is None:
    _MASTER_SECRET = "Default secret"
    HAS_MASTER_SECRET = False
else:
    HAS_MASTER_SECRET = True

MASTER_SECRET = _MASTER_SECRET
"The main secret derex uses to derive all other secrets"

__all__ = [
    "MASTER_SECRET",
    "compute_entropy",
    "DerexSecretError",
    "DerexSecrets",
    "get_secret",
]

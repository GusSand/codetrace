"""Config object."""

# annotations cannot be used along with marshmallow_dataclass
# from __future__ import annotations

import dataclasses

from typing import Any, ClassVar, Dict, Optional, Type, get_type_hints

import marshmallow_dataclass
import toml


@dataclasses.dataclass(frozen=True)
class Config:
    """Definitions for configurations that will be loaded at runtime."""

    SECRET_KEY: str
    ALLOWED_HOST: str
    DATABASE_URL: str
    EXPORT_AS_BOOKMARK_REDIS_URL: str

    DEBUG: bool = False
    USE_X_FORWARDED_HOST: bool = False
    SEMANTICUI_BASE_DIR: str = ".smanticui_static/"

    # Static file Configurations
    USE_S3: bool = False
    # S3
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_STORAGE_BUCKET_NAME: Optional[str] = None
    AWS_DEFAULT_ACL: Optional[str] = "public-read"
    AWS_BUCKET_ACL: Optional[str] = "public-read"
    AWS_AUTO_CREATE_BUCKET: bool = True
    AWS_LOCATION: Optional[str] = None
    AWS_S3_ENDPOINT_URL: Optional[str] = None  # Endpoint to upload files
    AWS_S3_CUSTOM_DOMAIN: Optional[str] = None
    # Local Filesystem
    STATIC_URL: str = "/webtools/static/"
    STATIC_ROOT: str = "static_deploy/webtools/static/"

    # Non default but required to pass
    # manage.py check --deploy --fail-level WARINING
    SECURE_HSTS_SECONDS: int = 3600  # 1 hour
    SECURE_HSTS_INCLUDE_SUBDOMAINS: bool = True
    SECURE_HSTS_PRELOAD: bool = True

    SECURE_CONTENT_TYPE_NOSNIFF: bool = True
    SECURE_BROWSER_XSS_FILTER: bool = True
    SECURE_SSL_REDIRECT: bool = True
    SESSION_COOKIE_SECURE: bool = True
    CSRF_COOKIE_SECURE: bool = True
    X_FRAME_OPTIONS: str = "DENY"
    SECURE_REFERRER_POLICY: str = "no-referrer-when-downgrade"

    WEBTOOLS_REVISION_FILEPATH: Optional[str] = "HEAD.txt"

    @classmethod
    def from_dict(cls, args) :
        """Set up config from dict object.

        :param args: Dict of configuration names and values
        :returns: Config instance
        """
        schema = marshmallow_dataclass.class_schema(cls)()
        ret: "Config" = schema.load(args)
        return ret

    @classmethod
    def from_toml(cls, filepath, section: <FILL>) :
        """Set up config from TOML file.

        :param filepath: Input TOML file path
        :param section: Section name in TOML file
        :returns: Config instance
        """
        with open(filepath) as f:
            obj = toml.load(f)
        return cls.from_dict(obj[section])

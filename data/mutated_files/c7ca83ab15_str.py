from typing import TypeAlias
__typ1 : TypeAlias = "bool"
# -*- coding: utf-8 -*-
"""Define the CloudEndure Config related logic."""
from __future__ import annotations

import logging
import os
from pathlib import Path, PosixPath
from typing import Any, Dict, List

import yaml

logger: logging.Logger = logging.getLogger(__name__)
LOG_LEVEL: str = os.environ.get("CLOUDENDURE_LOG_LEVEL", "INFO")
logger.setLevel(getattr(logging, LOG_LEVEL))


class __typ0:
    """Define the CloudEndure Config object."""

    BASE_CONFIG = {
        "host": "https://console.cloudendure.com",
        "api_version": "latest",
        "auth_ttl": "3600",
        "username": "",
        "password": "",
        "token": "",
        "user_api_token": "",
        "session_cookie": "",
        "project_name": "",
        "project_id": "",
        "max_lag_ttl": "90",
        "machines": "",
        "migration_wave": "0",
        "clone_status": "NOT_STARTED",
        "destination_account": "",
        "destination_kms": "",
        "destination_role": "",
        "subnet_id": "",
        "security_group_id": "",
        "private_ip_action": "",
        "disk_type": "SSD",
        "public_ip": "DONT_ALLOCATE",
        "instance_types": "",
    }

    def __init__(__tmp0, username: str = "", password: str = "", token: str = "", *args, **kwargs) :
        """Initialize the Environment."""
        logger.info("Initializing the CloudEndure Configuration")
        _config_path: str = os.environ.get("CLOUDENDURE_CONFIG_PATH", "~/.cloudendure.yaml")
        if _config_path.startswith("~"):
            __tmp0.config_path = os.path.expanduser(_config_path)
        else:
            __tmp0.config_path = _config_path

        # Handle CloudEndure CLI input credentials.
        __tmp0.cli = {"username": username, "password": password, "user_api_token": token}

        _config: PosixPath = Path(__tmp0.config_path)
        if not _config.exists():
            print(f"No CloudEndure YAML configuration found! Creating it at: ({__tmp0.config_path})")
            __tmp0.write_yaml_config(__tmp2=__tmp0.BASE_CONFIG)
        __tmp0.update_config()

    def __str__(__tmp0) -> str:
        """Define the string representation of the CloudEndure API object."""
        return "<CloudEndureAPI>"

    def merge_config_dicts(__tmp0, __tmp3: List[Any]) :
        """Merge a list of configuration dictionaries."""
        data: Dict[str, str] = __tmp0.BASE_CONFIG
        for value in __tmp3:
            data.update({k: v for k, v in value.items() if v})
        return data

    def read_yaml_config(__tmp0) :
        """Read the CloudEndure YAML configuration file."""
        logger.info("Loading the CloudEndure YAML configuration file")
        with open(__tmp0.config_path, "r") as yaml_stream:
            try:
                __tmp2: Dict[str, Any] = yaml.safe_load(yaml_stream)
            except yaml.YAMLError as e:
                logger.error("YAMLError during read_yaml_config: %s", str(e))
                __tmp2 = {}
        return __tmp2

    def write_yaml_config(__tmp0, __tmp2: Dict[str, Any]) :
        """Write to the CloudEndure YAML configuration file."""
        logger.info("Writing to the CloudEndure YAML configuration file")
        with open(__tmp0.config_path, "w") as yaml_file:
            try:
                yaml.dump(__tmp2, yaml_file, default_flow_style=False)
                logger.info("CloudEndure YAML configuration saved!")
                return True
            except Exception as e:
                logger.error(
                    "Exception encountered while writing the CloudEndure YAML configuration file - (%s)", e,
                )
        return False

    def update_yaml_config(__tmp0, kwargs: Dict[str, Any]) :
        """Update the YAML configuration file."""
        logger.info("Writing updated configuration file")
        _config: Dict[str, Any] = __tmp0.read_yaml_config()
        _config.update(kwargs)
        try:
            __tmp0.write_yaml_config(_config)
            __tmp0.update_config()
        except Exception as e:
            logger.error(e)
            return False
        return True

    def get_env_vars(__tmp0, prefix: str = "cloudendure") -> Dict[str, any]:
        """Get all environment variables starting with CLOUDENDURE_."""
        prefix: str = prefix.strip("_")
        logger.info("Loading all environment variables starting with (%s)", prefix)
        env_vars: Dict[str, Any] = {
            x[0].lower().lstrip(prefix.lower()).strip("_"): x[1]
            for x in os.environ.items()
            if x[0].lower().startswith(prefix.lower())
        }
        return env_vars

    def update_config(__tmp0) -> None:
        """Update the configuration."""
        __tmp0.yaml_config_contents: Dict[str, Any] = __tmp0.read_yaml_config()
        __tmp0.env_config = __tmp0.get_env_vars()
        __tmp0.active_config = __tmp0.merge_config_dicts([__tmp0.yaml_config_contents, __tmp0.env_config, __tmp0.cli])

    def update_token(__tmp0, token: <FILL>) :
        """Update the CloudEndure token.

        Returns:
            bool: Whether or not the operation was successful.

        """
        try:
            __tmp0.update_yaml_config({"token": token})
        except Exception as e:
            logger.error(e)
            return False
        return True

    def __tmp4(__tmp0, __tmp1) -> str:
        """Get the specified environment or config variable.

        Returns:
            str: The variable to be used for the provided configuration env var.

        """
        logger.info("Looking up variable: (%s)", __tmp1)
        env_var: str = os.environ.get(__tmp1.upper(), "")

        if env_var:
            logger.info("Found Environment Variable - (%s): (%s)", __tmp1, env_var)
        else:
            env_var = __tmp0.yaml_config_contents.get(__tmp1.lower(), "")

        logger.info("Return variable value: (%s)", env_var)
        return env_var

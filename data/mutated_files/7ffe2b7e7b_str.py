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

    def __tmp3(__tmp1, username: str = "", password: str = "", __tmp0: str = "", *args, **__tmp2) :
        """Initialize the Environment."""
        logger.info("Initializing the CloudEndure Configuration")
        _config_path: str = os.environ.get("CLOUDENDURE_CONFIG_PATH", "~/.cloudendure.yaml")
        if _config_path.startswith("~"):
            __tmp1.config_path = os.path.expanduser(_config_path)
        else:
            __tmp1.config_path = _config_path

        # Handle CloudEndure CLI input credentials.
        __tmp1.cli = {"username": username, "password": password, "user_api_token": __tmp0}

        _config: PosixPath = Path(__tmp1.config_path)
        if not _config.exists():
            print(f"No CloudEndure YAML configuration found! Creating it at: ({__tmp1.config_path})")
            __tmp1.write_yaml_config(__tmp4=__tmp1.BASE_CONFIG)
        __tmp1.update_config()

    def __tmp5(__tmp1) -> str:
        """Define the string representation of the CloudEndure API object."""
        return "<CloudEndureAPI>"

    def merge_config_dicts(__tmp1, values: List[Any]) -> Dict[str, str]:
        """Merge a list of configuration dictionaries."""
        data: Dict[str, str] = __tmp1.BASE_CONFIG
        for value in values:
            data.update({k: v for k, v in value.items() if v})
        return data

    def read_yaml_config(__tmp1) -> Dict[str, Any]:
        """Read the CloudEndure YAML configuration file."""
        logger.info("Loading the CloudEndure YAML configuration file")
        with open(__tmp1.config_path, "r") as yaml_stream:
            try:
                __tmp4: Dict[str, Any] = yaml.safe_load(yaml_stream)
            except yaml.YAMLError as e:
                logger.error("YAMLError during read_yaml_config: %s", str(e))
                __tmp4 = {}
        return __tmp4

    def write_yaml_config(__tmp1, __tmp4: Dict[str, Any]) :
        """Write to the CloudEndure YAML configuration file."""
        logger.info("Writing to the CloudEndure YAML configuration file")
        with open(__tmp1.config_path, "w") as yaml_file:
            try:
                yaml.dump(__tmp4, yaml_file, default_flow_style=False)
                logger.info("CloudEndure YAML configuration saved!")
                return True
            except Exception as e:
                logger.error(
                    "Exception encountered while writing the CloudEndure YAML configuration file - (%s)", e,
                )
        return False

    def update_yaml_config(__tmp1, __tmp2) :
        """Update the YAML configuration file."""
        logger.info("Writing updated configuration file")
        _config: Dict[str, Any] = __tmp1.read_yaml_config()
        _config.update(__tmp2)
        try:
            __tmp1.write_yaml_config(_config)
            __tmp1.update_config()
        except Exception as e:
            logger.error(e)
            return False
        return True

    def get_env_vars(__tmp1, prefix: str = "cloudendure") -> Dict[str, any]:
        """Get all environment variables starting with CLOUDENDURE_."""
        prefix: str = prefix.strip("_")
        logger.info("Loading all environment variables starting with (%s)", prefix)
        env_vars: Dict[str, Any] = {
            x[0].lower().lstrip(prefix.lower()).strip("_"): x[1]
            for x in os.environ.items()
            if x[0].lower().startswith(prefix.lower())
        }
        return env_vars

    def update_config(__tmp1) -> None:
        """Update the configuration."""
        __tmp1.yaml_config_contents: Dict[str, Any] = __tmp1.read_yaml_config()
        __tmp1.env_config = __tmp1.get_env_vars()
        __tmp1.active_config = __tmp1.merge_config_dicts([__tmp1.yaml_config_contents, __tmp1.env_config, __tmp1.cli])

    def update_token(__tmp1, __tmp0: str) -> __typ1:
        """Update the CloudEndure token.

        Returns:
            bool: Whether or not the operation was successful.

        """
        try:
            __tmp1.update_yaml_config({"token": __tmp0})
        except Exception as e:
            logger.error(e)
            return False
        return True

    def __tmp6(__tmp1, var: <FILL>) -> str:
        """Get the specified environment or config variable.

        Returns:
            str: The variable to be used for the provided configuration env var.

        """
        logger.info("Looking up variable: (%s)", var)
        env_var: str = os.environ.get(var.upper(), "")

        if env_var:
            logger.info("Found Environment Variable - (%s): (%s)", var, env_var)
        else:
            env_var = __tmp1.yaml_config_contents.get(var.lower(), "")

        logger.info("Return variable value: (%s)", env_var)
        return env_var

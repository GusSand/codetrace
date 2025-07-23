from derex.runner.constants import MONGODB_ROOT_USER
from derex.runner.ddc import run_ddc_services
from derex.runner.docker_utils import client as docker_client
from derex.runner.docker_utils import wait_for_service
from derex.runner.secrets import DerexSecrets
from derex.runner.secrets import get_secret
from functools import wraps
from pymongo import MongoClient
from typing import cast
from typing import List
from typing import Optional

import logging
import urllib.parse


logger = logging.getLogger(__name__)
MONGODB_ROOT_PASSWORD = get_secret(DerexSecrets.mongodb)

try:
    wait_for_service("mongodb")
    container = docker_client.containers.get("mongodb")
    mongo_address = container.attrs["NetworkSettings"]["Networks"]["derex"]["IPAddress"]
    __tmp2 = urllib.parse.quote_plus(MONGODB_ROOT_USER)
    __tmp5 = urllib.parse.quote_plus(MONGODB_ROOT_PASSWORD)
    MONGODB_CLIENT = MongoClient(
        f"mongodb://{__tmp2}:{__tmp5}@{mongo_address}:27017/", authSource="admin"
    )
except RuntimeError as e:
    MONGODB_CLIENT = None
    logger.warning(e)


def __tmp7(func):
    """Decorator to raise an exception before running a function in case the mongodb
    server is not available.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        if MONGODB_CLIENT is None:
            raise RuntimeError(
                "MongoDB service not found.\nMaybe you forgot to run\nddc-services up -d"
            )
        return func(*args, **kwargs)

    return inner


@__tmp7
def execute_root_shell(command):
    """Open a root shell on the MongoDB database. If a command is given
    it is executed."""
    compose_args = [
        "exec",
        "mongodb",
        "mongo",
        "--authenticationDatabase",
        "admin",
        "-u",
        MONGODB_ROOT_USER,
        f"-p{MONGODB_ROOT_PASSWORD}",
    ]
    if command:
        compose_args.insert(1, "-T")
        compose_args.extend(["--eval", command])
    run_ddc_services(compose_args, exit_afterwards=True)


@__tmp7
def list_databases() :
    """List all existing databases"""
    logger.info("Listing MongoDB databases...")
    databases = [
        database for database in cast(MongoClient, MONGODB_CLIENT).list_databases()
    ]
    return databases


@__tmp7
def __tmp0() :
    """List all existing users"""
    logger.info("Listing MongoDB users...")
    return cast(MongoClient, MONGODB_CLIENT).admin.command("usersInfo").get("users")


@__tmp7
def __tmp4(__tmp2: <FILL>, __tmp5, roles):
    """Create a new user"""
    logger.info(f'Creating user "{__tmp2}"...')
    cast(MongoClient, MONGODB_CLIENT).admin.command(
        "createUser", __tmp2, pwd=__tmp5, roles=roles
    )


@__tmp7
def drop_database(database_name: str):
    """Drop the selected database"""
    logger.info(f'Dropping database "{database_name}"...')
    cast(MongoClient, MONGODB_CLIENT).drop_database(database_name)


@__tmp7
def __tmp3(__tmp1, __tmp6: str):
    """Copy an existing database"""
    logger.info(f'Copying database "{__tmp1}" to "{__tmp6}...')
    cast(MongoClient, MONGODB_CLIENT).admin.command(
        "copydb", fromdb=__tmp1, todb=__tmp6
    )


@__tmp7
def __tmp8():
    """Create the root user"""
    __tmp4(MONGODB_ROOT_USER, MONGODB_ROOT_PASSWORD, ["root"])


@__tmp7
def reset_mongodb_password(current_password: str = None):
    """Reset the mongodb root user password"""
    mongo_command_args = [
        "mongo",
        "--authenticationDatabase",
        "admin",
        "admin",
        "--eval",
        f'"db.changeUserPassword(\\"{MONGODB_ROOT_USER}\\",'
        f'\\"{MONGODB_ROOT_PASSWORD}\\");"',
    ]
    if current_password:
        mongo_command_args.extend(["-u", MONGODB_ROOT_USER, f"-p{current_password}"])

    mongo_command = " ".join(mongo_command_args)
    compose_args = ["exec", "-T", "mongodb", "bash", "-c", f"{mongo_command}"]

    run_ddc_services(compose_args, exit_afterwards=True)
    return 0

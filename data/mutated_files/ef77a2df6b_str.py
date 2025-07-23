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
    __tmp3 = urllib.parse.quote_plus(MONGODB_ROOT_USER)
    password = urllib.parse.quote_plus(MONGODB_ROOT_PASSWORD)
    MONGODB_CLIENT = MongoClient(
        f"mongodb://{__tmp3}:{password}@{mongo_address}:27017/", authSource="admin"
    )
except RuntimeError as e:
    MONGODB_CLIENT = None
    logger.warning(e)


def __tmp8(func):
    """Decorator to raise an exception before running a function in case the mongodb
    server is not available.
    """

    @wraps(func)
    def __tmp0(*args, **kwargs):
        if MONGODB_CLIENT is None:
            raise RuntimeError(
                "MongoDB service not found.\nMaybe you forgot to run\nddc-services up -d"
            )
        return func(*args, **kwargs)

    return __tmp0


@__tmp8
def __tmp7(command: Optional[str]):
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


@__tmp8
def list_databases() -> List[dict]:
    """List all existing databases"""
    logger.info("Listing MongoDB databases...")
    databases = [
        database for database in cast(MongoClient, MONGODB_CLIENT).list_databases()
    ]
    return databases


@__tmp8
def __tmp1() :
    """List all existing users"""
    logger.info("Listing MongoDB users...")
    return cast(MongoClient, MONGODB_CLIENT).admin.command("usersInfo").get("users")


@__tmp8
def __tmp5(__tmp3, password, roles: List[str]):
    """Create a new user"""
    logger.info(f'Creating user "{__tmp3}"...')
    cast(MongoClient, MONGODB_CLIENT).admin.command(
        "createUser", __tmp3, pwd=password, roles=roles
    )


@__tmp8
def drop_database(__tmp2: str):
    """Drop the selected database"""
    logger.info(f'Dropping database "{__tmp2}"...')
    cast(MongoClient, MONGODB_CLIENT).drop_database(__tmp2)


@__tmp8
def __tmp4(source_db_name: str, destination_db_name: <FILL>):
    """Copy an existing database"""
    logger.info(f'Copying database "{source_db_name}" to "{destination_db_name}...')
    cast(MongoClient, MONGODB_CLIENT).admin.command(
        "copydb", fromdb=source_db_name, todb=destination_db_name
    )


@__tmp8
def __tmp9():
    """Create the root user"""
    __tmp5(MONGODB_ROOT_USER, MONGODB_ROOT_PASSWORD, ["root"])


@__tmp8
def __tmp6(current_password: str = None):
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

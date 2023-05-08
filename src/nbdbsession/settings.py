import os
import re
import subprocess
from dataclasses import dataclass
from urllib import parse

import tomllib

from .exceptions import EnvironmentDoesNotExistError, CredsFileNotFoundError


@dataclass
class Settings:
    db_driver: str
    user: str
    password: str
    db_url: str
    port: str
    database: str
    ssh_cmd: str = None


def show_connections():
    connections, file_path = read_toml_file()
    keys = connections.keys()
    print(f"You have defined {len(keys)} connections in {file_path}:")
    for k in keys:
        print(f"  - {k}")


def get_settings(connection: str, quote_password=True) -> Settings:
    settings = read_toml_file()[0]

    if connection not in settings.keys():
        raise EnvironmentDoesNotExistError(
            "Invalid connection, no such connection defined in config / settings."
        )

    s: dict = settings[connection]
    s = read_env_vars(s)

    # sql alchemy DSN connection string works only with a quoted password (for special chars)
    if quote_password:
        s["password"] = parse.quote(s["password"])

    return Settings(
        db_driver=s["db_driver"],
        user=s["user"],
        password=s["password"],
        db_url=s["db_url"],
        port=s["port"],
        database=s["database"],
        ssh_cmd=s.get("ssh_cmd"),
    )


def read_toml_file(file_path: str = None) -> tuple[dict, str]:
    """Parse toml file that contains the database credentials.

    If the file_path is not passed, this function will scan these places:

    - env var $SETTINGS_FILE_PATH
    - (root directory of a git project)/.settings.toml
    - $HOME/.nbdbsession.creds.toml

    returns:
        data (dict): the data parsed from the toml file
        file_path (str): the path to the toml file
    """

    if file_path is None:
        file_path = os.environ.get("SETTINGS_FILE_PATH")

    if file_path is None:
        # default to toplevel .settings.toml
        ps = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True
        )
        root_dir = ps.stdout.decode().strip("\n")
        file_path = os.path.join(root_dir, ".settings.toml")

    if not os.path.isfile(file_path):
        home_dir = os.environ.get("HOME")
        file_path = os.path.join(home_dir, ".nbdbsession.creds.toml")

    if not os.path.isfile(file_path):
        raise CredsFileNotFoundError(
            "Please make sure to define your database credentials in a toml file (either $HOME/.nbdbsession_creds.toml or in .settings.toml at the root level of your git repository)"
        )

    with open(file_path, "rb") as f:
        data: dict = tomllib.load(f)
        return data, file_path


def read_env_vars(data: dict):
    """replace all strings with ${ENV_VAR} with os.environ[ENV_VAR]"""
    for k, v in data.items():
        # skip if not string
        if not isinstance(v, str):
            continue

        if re.search(r"\${[A-Z_\d]*}", v):
            env_var_key = v[2:-1]
            data[k] = os.environ[env_var_key]

    return data

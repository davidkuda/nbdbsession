import os
import re
import subprocess
from dataclasses import dataclass
from urllib import parse

import tomllib

from .exceptions import EnvironmentDoesNotExistError


@dataclass
class Settings:
    db_driver: str
    user: str
    password: str
    db_url: str
    port: str
    database: str
    ssh_cmd: str


def get_settings(environment: str) -> Settings:
    settings = parse_toml()

    if environment not in settings.keys():
        raise EnvironmentDoesNotExistError(
            "Invalid environment, no such config / settings."
        )

    s: dict = settings[environment]

    return Settings(
        db_driver=s["db_driver"],
        user=s["user"],
        password=s["password"],
        db_url=s["db_url"],
        port=s["port"],
        database=s["database"],
        ssh_cmd=s.get("ssh_cmd"),
    )


def parse_toml(file_path: str = None) -> dict:
    """Parse .settings.toml that should be at top level of this repo."""

    if file_path is None:
        file_path = os.environ.get("SETTINGS_FILE_PATH")

    if file_path is None:
        # default to toplevel .settings.toml
        ps = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True
        )
        root_dir = ps.stdout.decode().strip("\n")
        file_path = os.path.join(root_dir, ".settings.toml")

    with open(file_path, "rb") as f:
        data: dict = tomllib.load(f)

        for section in data.keys():

            # First, replace all strings with ${ENV_VAR} with os.environ[ENV_VAR]
            for k, v in data[section].items():

                # skip if not string
                if not isinstance(v, str):
                    continue

                if re.search(r"\${[A-Z_\d]*}", v):
                    env_var_key = v[2:-1]
                    data[section][k] = os.environ[env_var_key]

            # Then, replace password with quoted password
            for k, v in data[section].items():
                if k == "password":
                    data[section][k] = parse.quote(v)

        return data

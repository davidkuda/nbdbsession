# Author: David Kuda
# Creation Date: October 2022
# License: MIT License

# This module makes connecting to databases with SSH and
# sql alchemy conn_strings easier and is meant to be used
# in jupyter lab / notebooks with the fantastic ipython
# magic "sql" package.

import os

from .connection_string import get_conn_str
from .ipython_magic import invoke_ipython_sql_magic
from .settings import get_settings
from .ssh_tunnel import SSHTunnel


def connect(environment: str):
    """Build conn_string from .settings.toml, export env_var, open ssh tunnel (if given).

    conn_string will be made available as env var DATABASE_URL and DATABASE_URL_ + environment.

    Args:
        environment (string):
            An environment corresponding to the objects in ".settings.toml", e.g.
            "production" or "staging".

    Returns:
        None
    """
    if environment is None:
        environment = os.environ["ENVIRONMENT"]

    settings = get_settings(environment)

    if settings.ssh_cmd is not None:
        SSHTunnel(settings.ssh_cmd).main()

    invoke_ipython_sql_magic()

    conn_str = get_conn_str(settings)
    env_var = "DATABASE_URL_" + environment.upper().replace("-", "_")
    os.environ[env_var] = conn_str

    os.environ["DATABASE_URL"] = conn_str

    return


if __name__ == "ndbdsession.sqlconn":
    # this block would run on import
    pass

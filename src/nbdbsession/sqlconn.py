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


def connect(environment: str = None) -> str:
    """Build conn_string from .settings.toml, export env_var, open ssh tunnel (if given).

    conn_string will be made available as env var DATABASE_URL and DATABASE_URL_ + environment.

    Args:
        environment (string):
            An environment corresponding to the objects in ".settings.toml", e.g.
            "production" or "staging".

    Returns:
        A connection string that can be used with sqlalchemy, and that can be used with
        iPython magic sql.
    """
    if environment is None:
        environment = os.environ["ENVIRONMENT"]
        print(f'Environment set to "{environment}".')

    settings = get_settings(environment)

    if settings.ssh_cmd is not None:
        SSHTunnel(settings.ssh_cmd).main()

    invoke_ipython_sql_magic()

    conn_str = get_conn_str(settings)
    env_var = "DATABASE_URL_" + environment.upper().replace("-", "_")
    os.environ[env_var] = conn_str
    print(f"Exported env var {env_var}.")

    os.environ["DATABASE_URL"] = conn_str
    print(f"Set DATABASE_URL for {environment}")

    # TODO: connect_to_db(conn_str)

    return conn_str


if __name__ == "db_connector.main":
    # this block would run on import
    pass

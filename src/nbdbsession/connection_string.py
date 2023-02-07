from .settings import Settings


def get_conn_str(settings: Settings) -> str:
    """Returns db connection string that can be used with sqlalchemy.

    Args:
        config (Settings): Config of db connection.

    Returns:
        A string that can be used to connect to the database.

        Example / Format: "postgresql://user:password@url:port/database"
    """
    s = settings

    if settings.ssh_cmd:
        url = "127.0.0.1"
    else:
        url = settings.db_url

    return f"postgresql://{s.user}:{s.password}@{url}:{s.port}/{s.database}"

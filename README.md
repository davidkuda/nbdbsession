# jupyter_database_io

I use notebooks all the time to connect to databases like postgres. With the notebook sessions, I create my PoCs (proof of concept). Or I also use such sessions to debug my code.

[`catherinedevlin`](https://github.com/catherinedevlin) has created open source software that I love: [`ipython-sql`](https://pypi.org/project/ipython-sql/). This code helps you to manage connections.

In the usual way, you would create a connection string, something like this:

```python
%load_ext sql 

import parse

# make a connection string for your database connection
config = {
    "user": "postgres",
    "password": parse.quote("postgres"),
    "url": "127.0.0.1",
    "port": 5432,
    "database": "postgres",
}

conn_string = f'postgresql://{c["user"]}:{c["password"]}@{c["url"]}:{c["port"]}/{c["database"]}'
# results in: 'postgresql://postgres:postgres@127.0.0.1:5432/postgres'

%sql $conn_string
```

With the code in this repo, you reduce all that to one line:

```python
from nb_db_session import prepare_connection

# this will enable ipython sql and use the conn str that you choose:
prepare_connection("staging")

%sql
```

You need to define your connections in a file called `.settings.toml`:

```toml
# .settings.toml
[staging]
user = "davidkuda"
password = "${ENV_VAR}"
db_url = "db.kuda.ai"
port = 5432
database = "dev"
# the ssh command is optional:
ssh_cmd = "ssh -fL 5432:db.kuda.ai:5432"
```

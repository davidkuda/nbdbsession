# nbdbsession

__This code helps you to manage connections to sql databases in jupyter notebooks.__

`nbdbsession` stands for "notebook database session".

I use notebooks all the time to connect to databases like postgres. With the notebook sessions, I often work on PoCs (proof of concept), on presentations or on debugging.

[`catherinedevlin`](https://github.com/catherinedevlin) has created open source software that I love: [`ipython-sql`](https://pypi.org/project/ipython-sql/).

This code -- `nbdbsession` -- lets you connect to sql databases from your notebook, and run queries.

### How To Use `nbdbsession`

First, install it:

```
pip install nbdbsession
```

Then, in your git repository where you start your notebook, create a `.settings.toml` file with your database login credentials:

```toml
# .settings.toml on top level of your git repo
[davidkuda]
db_driver = "postgresql"
database = "dev"
user = "davidkuda"
password = "${DB_PASSWORD}" # you can use environment variables
db_url = "localhost"
port = 5439
# the ssh command is optional:
ssh_cmd = "ssh -fL 5432:db.kuda.ai:5432"
```

Finally, you can connect to your database in your notebook by running the following code in a cell:

```python
from nbdbsession.sqlconn import connect

connect("davidkuda") # note: this is the name as defined in .settings.toml
```

Once you have done that, you can run sql commands by prepending `%sql` (one line) `%%sql` (multi-line) in the notebook.

__Run single line sql commands directly in your notebook:__

```sql
%sql SELECT * FROM table LIMIT 10;
```

__Run multi-line sql commands directly in your notebook:__

```sql
%%sql
SELECT
    *
FROM
    table
LIMIT
    10;
```

### Managing the conn without this repo

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
from nbdbsession.sqlconn import connect

# this will enable ipython sql and use the conn str that you choose:
connect("staging")

%sql
```


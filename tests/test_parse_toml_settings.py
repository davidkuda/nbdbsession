import os


from nbdbsession.settings import read_toml_file, read_env_vars


def get_test_creds_file_path():
    d = os.path.dirname(__file__)  # get path of this file's directory
    f = os.path.join(d, ".nbdbsession.testcreds.toml")
    return f


TEST_CREDS_FILE_PATH = get_test_creds_file_path()


def test_read_toml_file():
    connections = read_toml_file(TEST_CREDS_FILE_PATH)[0]
    assert "test_conn" in connections
    assert connections["test_conn"]["user"] == "davidkuda"


def test_read_env_vars():
    d = read_toml_file(TEST_CREDS_FILE_PATH)[0]
    c = d["test_conn"]
    assert c["password"] == "${DB_PASSWORD}"
    os.environ["DB_PASSWORD"] = "42"
    read_env_vars(c)
    assert c["password"] == "42"

from distutils.core import setup
from setuptools import find_packages

# nb_db_session := notebook_database_session
setup(
    name="nb_db_session",
    version="0.1",
    description="Config mgt to connect to databases from jupyter notebooks.",
    author="David Kuda",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/davidkuda/jupyter_database_io",
)

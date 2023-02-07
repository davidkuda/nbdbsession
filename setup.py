from distutils.core import setup
from pathlib import Path
from setuptools import find_packages


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


# nbdbsession := notebook_database_session
setup(
    name="nbdbsession",
    version="0.1.1",
    description="Config mgt to connect to databases from jupyter notebooks.",
    author="David Kuda",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/davidkuda/jupyter_database_io",
    long_description=long_description,
    long_description_content_type='text/markdown',
)

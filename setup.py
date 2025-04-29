import os
import codecs

from setuptools import setup
from setuptools import find_packages


## Basic Information
NAME        = "pyenvoy"
DESCRIPTION = "An API client for TRISA Envoy nodes that enables travel rule compliance."
AUTHOR      = "Rotational Labs"
EMAIL       = "support@rotational.io"
MAINTAINER  = "Rotational Labs"
LICENSE     = "MIT"
REPOSITORY  = "https://github.com/trisacrypto/pyenvoy"
PACKAGE     = "envoy"
URL         = "https://trisa.dev"


## Define the keywords
KEYWORDS = [
    "travel rule",
    "trisa",
    "envoy",
    "api client",
]


## Define the classifiers
## See https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries :: Python Modules",
]


## Important Paths
PROJECT = os.path.abspath(os.path.dirname(__file__))
REQUIRE_PATH = "requirements.txt"
VERSION_PATH = os.path.join(PACKAGE, "version.py")
PKG_DESCRIBE = "README.md"


## Directories to ignore in find_packages
EXCLUDES = [
    "tests",
    "tests.*",
    "bin",
    "docs",
    "docs.*",
    "fixtures",
]


def read(*parts):
    """
    Assume UTF-8 encoding and return the contents of the file located at the
    absolute path from the REPOSITORY joined with *parts.
    """
    with codecs.open(os.path.join(PROJECT, *parts), "rb", "utf-8") as f:
        return f.read()


def get_version(path=VERSION_PATH):
    """
    Reads the python file defined in the VERSION_PATH to find the get_version
    function, and executes it to ensure that it is loaded correctly. Separating
    the version in this way ensures no additional code is executed.
    """
    namespace = {}
    exec(read(path), namespace)
    return namespace["get_version"](short=True)


def get_requires(path=REQUIRE_PATH):
    """
    Yields a generator of requirements as defined by the REQUIRE_PATH which
    should point to a requirements.txt output by `pip freeze`.
    """
    for line in read(path).splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            yield line


def get_description_type(path=PKG_DESCRIBE):
    """
    Returns the long_description_content_type based on the extension of the
    package describe path (e.g. .txt, .rst, or .md).
    """
    _, ext = os.path.splitext(path)
    return {".rst": "text/x-rst", ".txt": "text/plain", ".md": "text/markdown"}[ext]


if __name__ == "__main__":
    config = {
        "name": NAME,
        "version": get_version(),
        "description": DESCRIPTION,
        "long_description": read(PKG_DESCRIBE),
        "long_description_content_type": get_description_type(PKG_DESCRIBE),
        "classifiers": CLASSIFIERS,
        "keywords": KEYWORDS,
        "license": LICENSE,
        "author": AUTHOR,
        "author_email": EMAIL,
        "url": URL,
        "maintainer": MAINTAINER,
        "maintainer_email": EMAIL,
        "project_urls": {
            "Documentation": URL,
            "Download": "{}/tarball/v{}".format(REPOSITORY, get_version()),
            "Source": REPOSITORY,
            "Tracker": "{}/issues".format(REPOSITORY),
        },
        "download_url": "{}/tarball/v{}".format(REPOSITORY, get_version()),
        "packages": find_packages(where=PROJECT, exclude=EXCLUDES),
        "package_data": {},
        "zip_safe": True,
        "entry_points": {},
        "install_requires": list(get_requires()),
        "python_requires": ">=3.10, <4",
    }

    setup(**config)

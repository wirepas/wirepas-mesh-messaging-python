"""
    Wirepas Messaging
    =================
    Installation script

    Copyright Wirepas Ltd 2019 licensed under Apache 2.0

    Please see License file for full text.
"""

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme_file = "README.md"
license_file = "LICENSE"

with open(readme_file) as f:
    long_description = f.read()


def get_absolute_path(*args):
    """ Transform relative pathnames into absolute pathnames """
    return os.path.join(here, *args)


about = {}
with open(get_absolute_path("./wirepas_mesh_messaging/__about__.py")) as f:
    exec(f.read(), about)

setup(
    name=about["__pkg_name__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    classifiers=about["__classifiers__"],
    keywords=about["__keywords__"],
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=[
        "protobuf~=6.31.1"
    ]
)

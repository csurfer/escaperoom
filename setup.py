#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os import path
from typing import Dict

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst")) as f:
    long_description = f.read()

# Get package and author details.
about: Dict[str, str] = {}
with open(path.join(here, "escaperoom", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    # Name of the module
    name="escaperoom",
    # Details
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    # The project's main homepage.
    url=about["__url__"],
    # Author details
    author=about["__author__"],
    author_email=about["__author_email__"],
    # License
    license=about["__license__"],
    packages=["escaperoom"],
    entry_points={"console_scripts": ["escaperoom=escaperoom.server:main"]},
    keywords="Generate virtual escape rooms from JSON config without a single line of code.",
    classifiers=[
        # Intended Audience.
        "Intended Audience :: Developers",
        # License.
        "License :: OSI Approved :: MIT License",
        # Project maturity.
        "Development Status :: 3 - Alpha",
        # Operating Systems.
        "Operating System :: POSIX",
        # Supported Languages.
        "Programming Language :: Python :: 3.8",
        # Topics
        "Topic :: Games/Entertainment",
    ],
    install_requires=["Flask", "jsonschema"],
)

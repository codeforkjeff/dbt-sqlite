#!/usr/bin/env python
import os
import re
from setuptools import find_packages
from setuptools import setup

# bits for pulling version from __version__.py taken from dbt snowflake plugin

this_directory = os.path.abspath(os.path.dirname(__file__))

# get this package's version from dbt/adapters/<name>/__version__.py
def _get_plugin_version():
    _version_path = os.path.join(
        this_directory, 'dbt', 'adapters', 'sqlite', '__version__.py'
    )
    with open(_version_path) as f:
        line = f.read().strip()
        delim = '"' if '"' in line else "'"
        return line.split(delim)[1]


package_name = "dbt-sqlite"
package_version = _get_plugin_version()
description = """A SQLite adapter plugin for dbt (data build tool)"""
long_description = "Please see the github repository for detailed information"

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=long_description,
    author='Jeff Chiu',
    author_email='jeff@codefork.com',
    url='https://github.com/codeforkjeff/dbt-sqlite',
    packages=[
        'dbt.adapters.sqlite',
        'dbt.include.sqlite',
    ],
    package_data={
        'dbt.include.sqlite': [
            'macros/*.sql',
            'macros/**/*.sql',
            'macros/**/**/*.sql',
            'dbt_project.yml',
            'sample_profiles.yml',
        ]
    },
    install_requires=[
        "dbt-core~=1.4.0"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',

        'License :: OSI Approved :: Apache Software License',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux'
    ]
)

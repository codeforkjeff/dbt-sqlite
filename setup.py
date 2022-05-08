#!/usr/bin/env python
import os
import re
from setuptools import find_packages
from setuptools import setup

# bits for pulling version from __version__.py taken from dbt snowflake plugin

this_directory = os.path.abspath(os.path.dirname(__file__))

# get this package's version from dbt/adapters/<name>/__version__.py
def _get_plugin_version_dict():
    _version_path = os.path.join(
        this_directory, 'dbt', 'adapters', 'sqlite', '__version__.py'
    )
    _semver = r'''(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'''

    # not sure why this works in dbt-snowflake:
    # it causes setuptools to populate prekind and pre with 'None' strings
    # so we just don't parse it

    #_pre = r'''((?P<prekind>a|b|rc)(?P<pre>\d+))?'''
    #_version_pattern = fr'''version\s*=\s*["']{_semver}{_pre}["']'''

    _version_pattern = fr'''version\s*=\s*["']{_semver}["']'''
    with open(_version_path) as f:
        match = re.search(_version_pattern, f.read().strip())
        if match is None:
            raise ValueError(f'invalid version at {_version_path}')
        return match.groupdict()


def _get_plugin_version():
    parts = _get_plugin_version_dict()
    #return "{major}.{minor}.{patch}{prekind}{pre}".format(**parts)
    return "{major}.{minor}.{patch}".format(**parts)


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
        "dbt-core>=1.1.0"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',

        'License :: OSI Approved :: Apache Software License',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux'
    ]
)

#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

package_name = "dbt-sqlite"
package_version = "0.0.3"
description = """A SQLite adapter plugin for dbt (data build tool)"""

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
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
        "dbt-core~=0.18.0",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: Apache Software License',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux'
    ]
)

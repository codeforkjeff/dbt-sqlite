#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

package_name = "dbt-sqlite"
package_version = "0.0.1"
description = """A SQLite adapter plugin for dbt (data build tool)"""

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    author='Jeff Chiu',
    author_email='jeff@codefork.com',
    url='https://github.com/codeforkjeff/dbt-sqlite',
    packages=find_packages(),
    package_data={
        'dbt': [
            'include/sqlite/macros/*.sql',
            'include/sqlite/dbt_project.yml',
        ]
    },
    install_requires=[
        "dbt-core>=0.18.1",
    ]
)

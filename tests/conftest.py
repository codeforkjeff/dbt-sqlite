import pytest
import os

# Import the standard functional fixtures as a plugin
# Note: fixtures with session scope need to be local
pytest_plugins = ["dbt.tests.fixtures.project"]

# The profile dictionary, used to write out profiles.yml
# dbt will supply a unique schema per test, so we do not specify 'schema' here
@pytest.fixture(scope="class")
def dbt_profile_target():
    return {
        'type': 'sqlite',
        'threads': 1,
        'database': 'adapter_test',
        'schema': 'main',
        'schemas_and_paths': {
            'main': '/tmp/dbt-sqlite-tests/adapter_test.db'
        },
        'schema_directory': '/tmp/dbt-sqlite-tests',
        'extensions' : [
            "/tmp/dbt-sqlite-tests/crypto.so"
        ]
    }

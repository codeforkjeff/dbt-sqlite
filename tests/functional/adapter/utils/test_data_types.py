import pytest
from dbt.tests.adapter.utils.data_types.test_type_bigint import BaseTypeBigInt
from dbt.tests.adapter.utils.data_types.test_type_boolean import BaseTypeBoolean
from dbt.tests.adapter.utils.data_types.test_type_float import BaseTypeFloat
from dbt.tests.adapter.utils.data_types.test_type_int import BaseTypeInt
from dbt.tests.adapter.utils.data_types.test_type_numeric import BaseTypeNumeric
from dbt.tests.adapter.utils.data_types.test_type_string import BaseTypeString
from dbt.tests.adapter.utils.data_types.test_type_timestamp import BaseTypeTimestamp

# These tests compare the resulting column types of CASTs against the types
# inferred by agate when loading seeds.
#
# There's a Column class in dbt-core that's used by the default adapter implementation
# of methods like [adapter].type_timestamp() to get a type for CASTs.
#
# Some quirks of SQLite that make these tests challenging:
#
# - a CAST seems to always result in an empty type (i.e. no type affinity) in views,
#   but not in a CREATE TABLE AS. So we tweak the tests to materialize models as tables.
#
# - CASTs to an unrecognized type will result in the type being 'NUM' which is a bit
#   mysterious.

class TestTypeBigInt(BaseTypeBigInt):
    pass


# users should imlement boolean columns as INT with values of 0 or 1
@pytest.mark.skip("boolean not supported in SQLite")
class TestTypeBoolean(BaseTypeBoolean):
    pass


class TestTypeFloat(BaseTypeFloat):

    models__actual_sql = """
{{ config(materialized='table') }}

select cast('1.2345' as {{ type_float() }}) as float_col
"""

    @pytest.fixture(scope="class")
    def models(self):
        return {"actual.sql": self.interpolate_macro_namespace(self.models__actual_sql, "type_float")}

    
class TestTypeInt(BaseTypeInt):

    models__actual_sql = """
{{ config(materialized='table') }}

select cast('12345678' as {{ type_int() }}) as int_col
"""

    @pytest.fixture(scope="class")
    def models(self):
        return {"actual.sql": self.interpolate_macro_namespace(self.models__actual_sql, "type_int")}

    
class TestTypeNumeric(BaseTypeNumeric):

    models__actual_sql = """
{{ config(materialized='table') }}

select cast('1.2345' as {{ type_numeric() }}) as numeric_col
"""

    @pytest.fixture(scope="class")
    def models(self):
        return {"actual.sql": self.interpolate_macro_namespace(self.models__actual_sql, "type_numeric")}

    def numeric_fixture_type(self):
        return "NUM"

    
class TestTypeString(BaseTypeString):

    models__actual_sql = """
{{ config(materialized='table') }}

select cast('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
as {{ type_string() }}) as string_col
"""

    @pytest.fixture(scope="class")
    def models(self):
        return {"actual.sql": self.interpolate_macro_namespace(self.models__actual_sql, "type_string")}


# casting to TIMESTAMP results in an 'NUM' type which truncates the original value
# to only the year portion. It's up to the user to properly deal with timestamps
# values from source tables.
@pytest.mark.skip("timestamp not supported in SQLite")
class TestTypeTimestamp(BaseTypeTimestamp):
    pass

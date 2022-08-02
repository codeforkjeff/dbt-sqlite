import pytest
from dbt.tests.adapter.utils.data_types.test_type_bigint import BaseTypeBigInt
from dbt.tests.adapter.utils.data_types.test_type_float import BaseTypeFloat
from dbt.tests.adapter.utils.data_types.test_type_int import BaseTypeInt
from dbt.tests.adapter.utils.data_types.test_type_numeric import BaseTypeNumeric
from dbt.tests.adapter.utils.data_types.test_type_string import BaseTypeString
from dbt.tests.adapter.utils.data_types.test_type_timestamp import BaseTypeTimestamp

# sqlite's table_info() pragma returns an empty type for columns in views
# so we tweak the models in these tests to materialize as tables

class TestTypeBigInt(BaseTypeBigInt):
    pass

    
@pytest.mark.skip("TODO: fix this")
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

    
@pytest.mark.skip("TODO: fix this")
class TestTypeNumeric(BaseTypeNumeric):
    def numeric_fixture_type(self):
        return "numeric"

    
class TestTypeString(BaseTypeString):
    pass

    
@pytest.mark.skip("TODO: fix this")
class TestTypeTimestamp(BaseTypeTimestamp):

    models__actual_sql = """
{{ config(materialized='table') }}

select cast('2021-01-01 01:01:01' as {{ type_timestamp() }}) as timestamp_col
"""

    @pytest.fixture(scope="class")
    def models(self):
        return {
            "actual.sql": self.interpolate_macro_namespace(self.models__actual_sql, "type_timestamp")
        }

    
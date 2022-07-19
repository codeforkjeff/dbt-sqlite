import pytest
from dbt.tests.adapter.utils.data_types.test_type_bigint import BaseTypeBigInt
from dbt.tests.adapter.utils.data_types.test_type_float import BaseTypeFloat
from dbt.tests.adapter.utils.data_types.test_type_int import BaseTypeInt
from dbt.tests.adapter.utils.data_types.test_type_numeric import BaseTypeNumeric
from dbt.tests.adapter.utils.data_types.test_type_string import BaseTypeString
from dbt.tests.adapter.utils.data_types.test_type_timestamp import BaseTypeTimestamp
from tests.functional.mixins import TearDownMixin

# why these fail: sqlite's table_info() pragma returns an empty type for columns in views;
# we coalsesce these to 'TEXT' in get_columns_in_relation() and _get_one_catalog() 
# in SQLAdapter. 

class TestTypeBigInt(BaseTypeBigInt, TearDownMixin):
    pass

    
@pytest.mark.skip('TODO: figure out workaround for table_info() and views')
class TestTypeFloat(BaseTypeFloat, TearDownMixin):
    pass

    
@pytest.mark.skip('TODO: figure out workaround for table_info() and views')
class TestTypeInt(BaseTypeInt, TearDownMixin):
    pass

    
@pytest.mark.skip('TODO: figure out workaround for table_info() and views')
class TestTypeNumeric(BaseTypeNumeric, TearDownMixin):
    def numeric_fixture_type(self):
        return "numeric"

    
@pytest.mark.skip('TODO: figure out workaround for table_info() and views')
class TestTypeString(BaseTypeString, TearDownMixin):
    pass

    
@pytest.mark.skip('TODO: figure out workaround for table_info() and views')
class TestTypeTimestamp(BaseTypeTimestamp, TearDownMixin):
    pass

    
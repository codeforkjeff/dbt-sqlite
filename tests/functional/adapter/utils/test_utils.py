import pytest
from dbt.tests.adapter.utils.base_utils import BaseUtils
from dbt.tests.adapter.utils.fixture_datediff import (
    seeds__data_datediff_csv,
    models__test_datediff_yml,
)
from dbt.tests.adapter.utils.fixture_dateadd import (
    seeds__data_dateadd_csv,
    models__test_dateadd_yml,
)
from dbt.tests.adapter.utils.test_any_value import BaseAnyValue
from dbt.tests.adapter.utils.test_array_append import BaseArrayAppend
from dbt.tests.adapter.utils.test_array_concat import BaseArrayConcat
from dbt.tests.adapter.utils.test_array_construct import BaseArrayConstruct
from dbt.tests.adapter.utils.test_bool_or import BaseBoolOr
from dbt.tests.adapter.utils.test_cast_bool_to_text import BaseCastBoolToText
from dbt.tests.adapter.utils.test_concat import BaseConcat
from dbt.tests.adapter.utils.test_current_timestamp import BaseCurrentTimestampNaive
from dbt.tests.adapter.utils.test_dateadd import BaseDateAdd
#from dbt.tests.adapter.utils.test_datediff import BaseDateDiff
from dbt.tests.adapter.utils.test_date_trunc import BaseDateTrunc
from dbt.tests.adapter.utils.test_escape_single_quotes import BaseEscapeSingleQuotesQuote
from dbt.tests.adapter.utils.test_escape_single_quotes import BaseEscapeSingleQuotesBackslash
from dbt.tests.adapter.utils.test_except import BaseExcept
from dbt.tests.adapter.utils.test_hash import BaseHash
from dbt.tests.adapter.utils.test_intersect import BaseIntersect
from dbt.tests.adapter.utils.test_last_day import BaseLastDay
from dbt.tests.adapter.utils.test_length import BaseLength
from dbt.tests.adapter.utils.test_listagg import BaseListagg
from dbt.tests.adapter.utils.test_position import BasePosition
from dbt.tests.adapter.utils.test_replace import BaseReplace
from dbt.tests.adapter.utils.test_right import BaseRight
from dbt.tests.adapter.utils.test_safe_cast import BaseSafeCast
from dbt.tests.adapter.utils.test_split_part import BaseSplitPart
from dbt.tests.adapter.utils.test_string_literal import BaseStringLiteral
from dbt.tests.adapter.utils.test_equals import BaseEquals
from dbt.tests.adapter.utils.test_null_compare import BaseMixedNullCompare, BaseNullCompare
from dbt.tests.adapter.utils.test_validate_sql import BaseValidateSqlMethod


class TestAnyValue(BaseAnyValue):
    pass


@pytest.mark.skip("arrays not supported in SQLite")
class TestArrayAppend(BaseArrayAppend):
    pass


@pytest.mark.skip("arrays not supported in SQLite")
class TestArrayConcat(BaseArrayConcat):
    pass


@pytest.mark.skip("arrays not supported in SQLite")
class TestArrayConstruct(BaseArrayConstruct):
    pass


class TestBoolOr(BaseBoolOr):
    pass


class TestCastBoolToText(BaseCastBoolToText):
    pass


class TestConcat(BaseConcat):
    pass


@pytest.mark.skip("timestamps not supported in SQLite")
class TestCurrentTimestampNaive(BaseCurrentTimestampNaive):
    pass

class BaseDateAdd(BaseUtils):

    models__test_dateadd_sql = """
    with data as (
        select * from {{ ref('data_dateadd') }}
    )
    
    select
        {{ dateadd('datepart', 'interval_length', 'from_time') }} AS actual,
        result as expected
    from data
    """

    @pytest.fixture(scope="class")
    def seeds(self):
        return {"data_dateadd.csv": seeds__data_dateadd_csv}

    @pytest.fixture(scope="class")
    def models(self):
        return {
            "test_dateadd.yml": models__test_dateadd_yml,
            "test_dateadd.sql": self.interpolate_macro_namespace(
                self.models__test_dateadd_sql, "dateadd"
            ),
        }


class TestDateAdd(BaseDateAdd):
    pass


class BaseDateDiff(BaseUtils):

    models__test_datediff_sql = """
    with data as (

        select * from {{ ref('data_datediff') }}

    )

    select

        case
            when datepart = 'second' then {{ datediff('first_date', 'second_date', 'second') }}
            when datepart = 'minute' then {{ datediff('first_date', 'second_date', 'minute') }}
            when datepart = 'hour' then {{ datediff('first_date', 'second_date', 'hour') }}
            when datepart = 'day' then {{ datediff('first_date', 'second_date', 'day') }}
            when datepart = 'week' then {{ datediff('first_date', 'second_date', 'week') }}
            when datepart = 'month' then {{ datediff('first_date', 'second_date', 'month') }}
            when datepart = 'year' then {{ datediff('first_date', 'second_date', 'year') }}
            else null
        end as actual,
        result as expected

    from data

    -- Also test correct casting of literal values.

    -- sqlite implementation of datediff doesn't support microsecond or quarter
    
    union all select {{ datediff("'1999-12-31 23:59:59.999999'", "'2000-01-01 00:00:00.000000'", "second") }} as actual, 1 as expected
    union all select {{ datediff("'1999-12-31 23:59:59.999999'", "'2000-01-01 00:00:00.000000'", "minute") }} as actual, 1 as expected
    union all select {{ datediff("'1999-12-31 23:59:59.999999'", "'2000-01-01 00:00:00.000000'", "hour") }} as actual, 1 as expected
    union all select {{ datediff("'1999-12-31 23:59:59.999999'", "'2000-01-01 00:00:00.000000'", "day") }} as actual, 1 as expected
    union all select {{ datediff("'1999-12-31 23:59:59.999999'", "'2000-01-03 00:00:00.000000'", "week") }} as actual, 1 as expected
    union all select {{ datediff("'1999-12-31 23:59:59.999999'", "'2000-01-01 00:00:00.000000'", "month") }} as actual, 1 as expected
    union all select {{ datediff("'1999-12-31 23:59:59.999999'", "'2000-01-01 00:00:00.000000'", "year") }} as actual, 1 as expected
    """


    @pytest.fixture(scope="class")
    def seeds(self):
        return {"data_datediff.csv": seeds__data_datediff_csv}

    @pytest.fixture(scope="class")
    def models(self):
        return {
            "test_datediff.yml": models__test_datediff_yml,
            "test_datediff.sql": self.interpolate_macro_namespace(
                self.models__test_datediff_sql, "datediff"
            ),
        }


@pytest.mark.skip("TODO: implement datediff")
class TestDateDiff(BaseDateDiff):
    pass


@pytest.mark.skip("TODO: implement date_trunc")
class TestDateTrunc(BaseDateTrunc):
    pass


class TestEscapeSingleQuotes(BaseEscapeSingleQuotesQuote):
    pass


class TestExcept(BaseExcept):
    pass


class TestHash(BaseHash):
    pass


class TestIntersect(BaseIntersect):
    pass


@pytest.mark.skip("TODO: implement lastday")
class TestLastDay(BaseLastDay):
    pass


class TestLength(BaseLength):
    pass


@pytest.mark.skip("TODO: implement listagg")
class TestListagg(BaseListagg):
    pass


class TestPosition(BasePosition):
    pass


class TestReplace(BaseReplace):
    pass


class TestRight(BaseRight):
    pass


class TestSafeCast(BaseSafeCast):
    pass

@pytest.mark.skip("TODO: implement split_part, either using sqlite>=3.8.3 for WITH RECURSIVE support, or possibly sooner using jinja and agate tables")
class TestSplitPart(BaseSplitPart):
    pass

class TestStringLiteral(BaseStringLiteral):
    pass

class TestEquals(BaseEquals):
    pass

class TestMixedNullCompare(BaseMixedNullCompare):
    pass

class TestNullCompare(BaseNullCompare):
    pass

class TestValidateSqlMethod(BaseValidateSqlMethod):
    pass
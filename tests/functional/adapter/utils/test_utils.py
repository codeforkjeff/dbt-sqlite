import pytest
from dbt.tests.adapter.utils.base_utils import BaseUtils
from dbt.tests.adapter.utils.test_any_value import BaseAnyValue
from dbt.tests.adapter.utils.test_bool_or import BaseBoolOr
from dbt.tests.adapter.utils.test_cast_bool_to_text import BaseCastBoolToText
from dbt.tests.adapter.utils.test_concat import BaseConcat
from dbt.tests.adapter.utils.test_dateadd import BaseDateAdd
from dbt.tests.adapter.utils.test_datediff import BaseDateDiff
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
from tests.functional.mixins import TearDownMixin


class TestAnyValue(BaseAnyValue, TearDownMixin):
    pass


class TestBoolOr(BaseBoolOr, TearDownMixin):
    pass


class TestCastBoolToText(BaseCastBoolToText, TearDownMixin):
    pass


class TestConcat(BaseConcat, TearDownMixin):
    pass


class TestDateAdd(BaseDateAdd, TearDownMixin):
    pass


class TestDateDiff(BaseDateDiff, TearDownMixin):
    pass


class TestDateTrunc(BaseDateTrunc, TearDownMixin):
    pass


class TestEscapeSingleQuotes(BaseEscapeSingleQuotesQuote, TearDownMixin):
    pass


class TestExcept(BaseExcept, TearDownMixin):
    pass


class TestHash(BaseHash, TearDownMixin):
    pass


class TestIntersect(BaseIntersect, TearDownMixin):
    pass


class TestLastDay(BaseLastDay, TearDownMixin):
    pass


class TestLength(BaseLength, TearDownMixin):
    pass


class TestListagg(BaseListagg, TearDownMixin):
    pass


class TestPosition(BasePosition, TearDownMixin):
    pass


class TestReplace(BaseReplace, TearDownMixin):
    pass


class TestRight(BaseRight, TearDownMixin):
    pass


class TestSafeCast(BaseSafeCast, TearDownMixin):
    pass


class TestSplitPart(BaseSplitPart, TearDownMixin):
    pass


class TestStringLiteral(BaseStringLiteral, TearDownMixin):
    pass

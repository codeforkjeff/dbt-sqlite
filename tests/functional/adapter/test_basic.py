
import glob
import os

import pytest

from dbt.tests.adapter.basic.test_base import BaseSimpleMaterializations
from dbt.tests.adapter.basic.test_singular_tests import BaseSingularTests
from dbt.tests.adapter.basic.test_singular_tests_ephemeral import BaseSingularTestsEphemeral
from dbt.tests.adapter.basic.test_empty import BaseEmpty
from dbt.tests.adapter.basic.test_ephemeral import BaseEphemeral
from dbt.tests.adapter.basic.test_incremental import BaseIncremental
from dbt.tests.adapter.basic.test_generic_tests import BaseGenericTests
from dbt.tests.adapter.basic.test_snapshot_check_cols import BaseSnapshotCheckCols
from dbt.tests.adapter.basic.test_snapshot_timestamp import BaseSnapshotTimestamp
from dbt.tests.adapter.basic.test_adapter_methods import BaseAdapterMethod


class TearDownMixin():
    @classmethod
    def teardown_class(module):
        for path in glob.glob('/tmp/dbt-sqlite-tests/*.db'):
            print("DELETING")
            os.remove(path)


class TestSimpleMaterializationsSqlite(BaseSimpleMaterializations, TearDownMixin):
    pass


class TestSingularTestsSqlite(BaseSingularTests, TearDownMixin):
    pass


class TestSingularTestsEphemeralSqlite(BaseSingularTestsEphemeral, TearDownMixin):
    pass


class TestEmptySqlite(BaseEmpty, TearDownMixin):
    pass


class TestEphemeralSqlite(BaseEphemeral, TearDownMixin):
    pass


class TestIncrementalSqlite(BaseIncremental, TearDownMixin):
    pass


class TestGenericTestsSqlite(BaseGenericTests, TearDownMixin):
    pass


class TestSnapshotCheckColsSqlite(BaseSnapshotCheckCols, TearDownMixin):
    pass


class TestSnapshotTimestampSqlite(BaseSnapshotTimestamp, TearDownMixin):
    pass


class TestBaseAdapterMethod(BaseAdapterMethod, TearDownMixin):
    pass


import glob
import os

import pytest

from dbt.tests.adapter.basic.expected_catalog import base_expected_catalog, no_stats, expected_references_catalog
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
from dbt.tests.adapter.basic.test_docs_generate import BaseDocsGenerate, BaseDocsGenReferences


class TearDownMixin():
    @classmethod
    def teardown_class(module):
        for path in glob.glob('/tmp/dbt-sqlite-tests/*.db'):
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


class TestBaseAdapterMethodSqlite(BaseAdapterMethod, TearDownMixin):
    pass


@pytest.mark.skip("TODO: views can't reference views in other schemas; make our own customized fixtures and expectations")
class TestDocsGenerateSqlite(BaseDocsGenerate, TearDownMixin):
    @pytest.fixture(scope="class")
    def expected_catalog(self, project):
        return base_expected_catalog(
            project,
            role=None,
            id_type="integer",
            text_type="text",
            time_type="DATETIME",
            view_type="view",
            table_type="table",
            model_stats=no_stats(),
            seed_stats=no_stats(),
        )


@pytest.mark.skip('TODO: figure out error with column indices not lining up for seed')
class TestDocsGenReferencesSqlite(BaseDocsGenReferences, TearDownMixin):
    @pytest.fixture(scope="class")
    def expected_catalog(self, project):
        return expected_references_catalog(
            project,
            role=None,
            id_type="integer",
            text_type="text",
            time_type="DATETIME",
            bigint_type="bigint",
            view_type="view",
            table_type="table",
            model_stats=no_stats(),
            seed_stats=no_stats(),
            view_summary_stats=no_stats(),
        )

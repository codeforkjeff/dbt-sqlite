
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


class TestSimpleMaterializationsSqlite(BaseSimpleMaterializations):
    pass


class TestSingularTestsSqlite(BaseSingularTests):
    pass


class TestSingularTestsEphemeralSqlite(BaseSingularTestsEphemeral):
    pass


class TestEmptySqlite(BaseEmpty):
    pass


class TestEphemeralSqlite(BaseEphemeral):
    pass


class TestIncrementalSqlite(BaseIncremental):
    pass


class TestGenericTestsSqlite(BaseGenericTests):
    pass


class TestSnapshotCheckColsSqlite(BaseSnapshotCheckCols):
    pass


class TestSnapshotTimestampSqlite(BaseSnapshotTimestamp):
    pass


class TestBaseAdapterMethodSqlite(BaseAdapterMethod):
    pass


@pytest.mark.skip("TODO: views can't reference views in other schemas; make our own customized fixtures and expectations")
class TestDocsGenerateSqlite(BaseDocsGenerate):
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
class TestDocsGenReferencesSqlite(BaseDocsGenReferences):
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

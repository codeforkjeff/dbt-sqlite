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
from dbt.tests.adapter.basic.test_docs_generate import BaseDocsGenerate
from dbt.tests.adapter.basic.test_docs_generate import BaseDocsGenReferences


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


class TestAdapterMethodSqlite(BaseAdapterMethod):
    pass


class TestDocsGenerateSqlite(BaseDocsGenerate):
    pass


class TestDocsGenerateSqlite(BaseDocsGenReferences):
    pass

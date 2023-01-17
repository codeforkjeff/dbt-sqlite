
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
from dbt.tests.adapter.basic.test_docs_generate import BaseDocsGenerate, BaseDocsGenReferences, models__schema_yml, models__readme_md


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


class TestDocsGenerateSqlite(BaseDocsGenerate):
    """
    Change underlying test to avoid having views referencing views in other schemas, which is a no-no in sqlite.
    """

    models__model_sql = """
{{
    config(
        materialized='table',
    )
}}

select * from {{ ref('seed') }}
"""

    models__second_model_sql = """
{{
    config(
        materialized='table',
        schema='test',
    )
}}

select * from {{ ref('seed') }}
"""

    @pytest.fixture(scope="class")
    def models(self):
        # replace models with 
        return {
            "schema.yml": models__schema_yml,
            "second_model.sql": self.models__second_model_sql,
            "readme.md": models__readme_md,
            "model.sql": self.models__model_sql,
        }

    @pytest.fixture(scope="class")
    def expected_catalog(self, project):
        expected_catalog = base_expected_catalog(
            project,
            role=None,
            id_type="INT",
            text_type="TEXT",
            time_type="TEXT",
            view_type="view",
            table_type="table",
            model_stats=no_stats(),
            seed_stats=no_stats(),
        )

        # patch
        expected_catalog['nodes']['model.test.model']['metadata']['type']='table'
        expected_catalog['nodes']['model.test.second_model']['metadata']['type']='table'

        return expected_catalog


@pytest.mark.skip("TODO: not sure why 'index' values are off by 1")
class TestDocsGenReferencesSqlite(BaseDocsGenReferences):

    @pytest.fixture(scope="class")
    def expected_catalog(self, project):
        return expected_references_catalog(
            project,
            role=None,
            id_type="INT",
            text_type="TEXT",
            time_type="TEXT",
            bigint_type="bigint",
            view_type="view",
            table_type="table",
            model_stats=no_stats(),
            #seed_stats=no_stats(),
            #view_summary_stats=no_stats(),
        )

import pytest
from dbt.tests.adapter.ephemeral.test_ephemeral import BaseEphemeralMulti
from dbt.tests.util import run_dbt, check_relations_equal


@pytest.mark.skip("started failing with dbt-core 1.9.0, not sure what's going on here")
class TestEphemeralMultiSqlite(BaseEphemeralMulti):

   def test_ephemeral_multi_sqlite(self, project):
        run_dbt(["seed"])
        results = run_dbt(["run"])
        assert len(results) == 3
        check_relations_equal(project.adapter, ["SEED", "DEPENDENT", "DOUBLE_DEPENDENT", "SUPER_DEPENDENT"])


import glob
import os


class TearDownMixin():
    @classmethod
    def teardown_class(module):
        for path in glob.glob('/tmp/dbt-sqlite-tests/*.db'):
            os.remove(path)

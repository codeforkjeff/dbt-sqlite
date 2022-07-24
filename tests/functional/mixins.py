
import glob
import os
import os.path

class TearDownMixin():
    @classmethod
    def teardown_class(module):
        for path in glob.glob(os.path.join(os.environ['TESTDATA'], '*.db')):
            os.remove(path)

import sys
import site
site.addsitedir('')
print(sys.path)
import unittest
from databases import TinyDatabase

class TestTinyDB(unittest.TestCase):

    def test_connection(self):
        pass

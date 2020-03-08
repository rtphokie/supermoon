import unittest
from supermoon import next_supermoon
from pprint import pprint
class MyTestCase(unittest.TestCase):
    def test_next(self):
        result = next_supermoon(dt=None)
        pprint(result)


if __name__ == '__main__':
    unittest.main()

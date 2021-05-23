import unittest
from supermoon.__main__ import next_supermoon
from datetime import datetime, tzinfo
from pprint import pprint
from skyfield.api import utc

class MyTestCase(unittest.TestCase):
    def test_next(self):
        result = next_supermoon(dt=None)
        year = 2021
        for month in range(1,7):
            # espenek and nolle agree, yes supermoon
            dt = datetime(year,month,1)
            dt = dt.replace(tzinfo=utc)
            result = next_supermoon(dt=dt)
            print(f"FM {result['fullmoon']['date'].strftime('%c')}",
                  f"{result['fullmoon']['distance']}",
                  f"P {result['perigee']['date'].strftime('%c')}|",
                  f"N {result['definitions']['Nolle']:1}",
                  f"E {result['definitions']['Espenak']:1}",
                  f"24 {result['definitions']['within 1 day of perigee']:1}",
                  f"dia {result['angular diameter']}",
                  )

    def test_2020(self):
        for month in [1,7]:
            # espenek and nolle agree, yes supermoon
            dt = datetime(year,month,1)
            dt = dt.replace(tzinfo=utc)
            result = next_supermoon(dt=dt)

            # http://astropixels.com/ephemeris/moon/fullperigee2001.html
            if month in [2,3,4,5]:
                self.assertTrue(result['definitions']['espenek'], 'expected espenek calculation to be True')
            else:
                self.assertFalse(result['definitions']['espenek'], 'expected espenek calculation to be False')

            # https://www.astropro.com/features/tables/cen21ce/suprmoon.html
            # https://www.timeanddate.com/moon/phases/
            if month in [3,4]:
                self.assertTrue(result['definitions']['nolle_2011'], 'expected nolle_2011 calculation to be True')
                self.assertTrue(result['definitions']['timeanddate'], 'expected timeanddate calculation to be True')
            else:
                self.assertFalse(result['definitions']['nolle_2011'], 'expected nolle_2011 calculation to be False')
                self.assertFalse(result['definitions']['timeanddate'], 'expected timeanddate calculation to be False')

            # https://earthsky.org/human-world/what-is-a-supermoon
            if month in [3,4,5]:
                self.assertTrue(result['definitions']['earthsky'], 'expected earthsky calculation to be True')
            else:
                self.assertFalse(result['definitions']['earthsky'], 'expected earthsky calculation to be False')

if __name__ == '__main__':
    unittest.main()

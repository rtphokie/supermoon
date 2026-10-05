import unittest
from datetime import datetime, timezone
from supermoon import next_supermoon, next_supermoons, supermoons, describe
from supermoon.cli import main


class MyTestCase(unittest.TestCase):
    def test_next(self):
        result = next_supermoon(dt=datetime(2025, 1, 1, tzinfo=timezone.utc))
        self.assertEqual(datetime(2025, 10, 7).date(), result['fullmoon']['date'].date())
        self.assertTrue(result['definitions']['Espenak'])
        self.assertTrue(result['definitions']['Nolle'])
        self.assertFalse(result['definitions']['Sky & Telescope'])

    def test_naive_datetime_is_utc(self):
        naive = next_supermoon(dt=datetime(2025, 1, 1))
        aware = next_supermoon(dt=datetime(2025, 1, 1, tzinfo=timezone.utc))
        self.assertEqual(aware['fullmoon']['date'], naive['fullmoon']['date'])

    def test_2020(self):
        results = {r['fullmoon']['date'].month: r['definitions'] for r in supermoons(2020)}

        # http://astropixels.com/ephemeris/moon/fullperigee2001.html
        self.assertEqual([2, 3, 4, 5], sorted(results.keys()))
        for month, definitions in results.items():
            self.assertTrue(definitions['Espenak'], f'expected Espenak calculation to be True for month {month}')

        # https://www.astropro.com/features/tables/cen21ce/suprmoon.html
        # https://www.timeanddate.com/moon/phases/
        for month in [3, 4, 5]:
            self.assertTrue(results[month]['Nolle'], f'expected Nolle calculation to be True for month {month}')
        for month in [3, 4]:
            self.assertTrue(results[month]['Time & Date'], f'expected Time & Date calculation to be True for month {month}')
        self.assertFalse(results[2]['Nolle'])
        self.assertFalse(results[5]['Time & Date'])

    def test_supermoon_counts(self):
        expected = {2020: 4, 2025: 3, 2029: 5}
        for year, cnt in expected.items():
            self.assertEqual(cnt, len(supermoons(year)), f'unexpected number of supermoons in {year}')

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            supermoons(1899)

    def test_next_supermoons(self):
        results = next_supermoons(count=3, dt=datetime(2020, 1, 1, tzinfo=timezone.utc))
        self.assertEqual([2, 3, 4], [r['fullmoon']['date'].month for r in results])

    def test_describe(self):
        result = next_supermoon(dt=datetime(2020, 3, 1, tzinfo=timezone.utc))
        lines = describe(result, perigee=True, distance=True, angulardiameter=True)
        self.assertEqual(3, len(lines))
        self.assertIn('according to all known definitions', lines[0])

    def test_cli(self):
        self.assertEqual(0, main(['2020', '-B']))


if __name__ == '__main__':
    unittest.main()

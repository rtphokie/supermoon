import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from datetime import datetime,timedelta
from supermoon import apsis, lunarphases
import pytz
from pprint import pprint
import requests
import re
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning) # ignore file closure warnings from Skyfield



# validated against retired NASA eclipse expert Fred Espenak's calculations which are based on
# Astronomical Algorithms by Jean Meeus (Willmann-Bell, Inc., Richmond, 1998).
# http://www.astropixels.com/ephemeris/astrocal/astrocal2020gmt.html

def get_espenak_apoperigees(year=2020):
    url = f"http://www.astropixels.com/ephemeris/astrocal/astrocal{year}gmt.html"
    filename = f"{year}.html"
    r = requests.get(url)
    data = []
    data_by_type = {}
    if not os.path.exists(filename):
        with open(filename, "w") as text_file:
            text_file.write(r.text.replace("&lt;", "<"))
    with open(filename, "r") as text_file:
        soup = BeautifulSoup(text_file, 'lxml')
        data_tables = soup.find_all('pre')
        # print (data_tables[4].text)
        for tableno in range(4,6):
            try:
                lines = data_tables[tableno].text.split("\n")
            except:
                print (r.text)
                raise
            month=None
            for line in lines[4:]:
                # split columnar data
                if len(line.strip()) == 0: continue # skip blank lines
                read_month = line[:3].strip()
                if len(read_month) == 3 and read_month != month:
                    month = read_month
                if line[10] == ':':
                    date_time_obj = datetime.strptime(f"{year} {month} {line[4:13]} UTC", '%Y %b %d  %H:%M %Z')
                else:
                    date_time_obj = datetime.strptime(f"{year} {month} {line[4:10]} UTC", '%Y %b %d  %H %Z')
                date_time_obj = pytz.UTC.localize(date_time_obj)
                desc = line[14:].strip()
                if 'Lunar Eclipse' in desc:
                    type = 'lunar eclipse'
                elif 'Solar Eclipse' in desc:
                    type = 'solar eclipse'
                elif ' Conjunction' in desc:
                    type = 'conjunctions'
                elif ' Occn.' in desc:
                    type = 'occultation'
                elif 'Opposition' in desc:
                    type = 'opposition'
                elif 'Solstice' in desc:
                    type = 'solstice'
                elif 'Equinox' in desc:
                    type = 'equinox'
                elif ' of ' in desc:
                    type = 'close'
                elif ' MOON' in desc:
                    type = 'moon phases'
                elif ' Perigee' in desc:
                    type = 'perigee'
                elif ' Apogee' in desc:
                    type = 'apogee'
                elif ' Perihelion' in desc:
                    type = 'perihelion'
                elif ' Aphelion' in desc:
                    type = 'aphelion'
                elif ' Node' in desc:
                    type = 'moon node'
                elif 'Meteor Shower' in desc:
                    type = 'meteor shower'
                elif 'Greatest Elong' in desc:
                    type = 'greatest elong'
                else:
                    type = 'other'

                if type not in data_by_type.keys():
                    data_by_type[type] = []
                report = {'dt': date_time_obj,
                          'desc': desc,
                          'type': type,
                          'nums': re.findall(r"[-+]?\d*\.\d+|\d+", desc)
                }
                data.append(report)
                data_by_type[type].append(report)
        return(data_by_type, data)




def nearestDate(base, dates):
    nearness = { abs(base.timestamp() - date.timestamp()) : date for date in dates }
    return nearness[min(nearness.keys())]

class MyTestCase(unittest.TestCase):
    def test_get_espenak(self):
        expected = {'2016': {'perigee': 13, 'apogee': 14},
                    '2017': {'perigee': 13, 'apogee': 13},
                    '2018': {'perigee': 14, 'apogee': 13},
                    '2019': {'perigee': 13, 'apogee': 13},
                    '2020': {'perigee': 13, 'apogee': 14},
                    '2021': {'perigee': 13, 'apogee': 13},
                    '2022': {'perigee': 14, 'apogee': 13},
                    '2023': {'perigee': 13, 'apogee': 13},
                    '2024': {'perigee': 13, 'apogee': 14},
                    '2025': {'perigee': 13, 'apogee': 13},
                    }
        for year in range(2016,2026):
            data_by_cat, data = get_espenak_apoperigees(year=year)
            for i in ['perigee', 'apogee']:
                self.assertEqual(expected[str(year)][i], len(data_by_cat[i]),
                                 f"unexpected number of {i}s in {year}")

    def test_apoperigee(self):
        max_error_dt_dt = None
        max_error_dt = 0
        max_error_d = 0
        max_error_d_dt = None
        for a in ['perigee', 'apogee']:
            for year in range(2016,2026):
                data_by_cat, data = get_espenak_apoperigees(year=year)
                for p in data_by_cat[a]:
                    new_date = p['dt'] - timedelta(days=14)
                    if a == 'perigee':
                        dt, d = apsis.next_perigee(dt=new_date)
                    elif a == 'apogee':
                        dt, d = apsis.next_apogee(dt=new_date)

                    dtdelta = (dt - p['dt']).total_seconds()
                    dt_error_limit = 60*30  # 30 minutes
                    self.assertLessEqual(dtdelta, dt_error_limit,
                                         f"calculated {a} {dt} varied from {p['dt']} by {dtdelta/60.:.1f} min")
                    if dtdelta > max_error_dt:
                        max_error_dt = dtdelta
                        max_error_dt_dt = dt

                    d_error_limit = 15
                    ddelta = abs(d - float(p['nums'][0]))
                    self.assertLessEqual(ddelta, d_error_limit,
                                         f"calculated {a} distance {d} on {dt} varied from {p['nums'][0]} by {ddelta:.1f} km")
                    if ddelta > max_error_d:
                        max_error_d = ddelta
                        max_error_d_dt = dt

            print (f"maximum {a} dt error {max_error_dt/60.:.1f} min on {max_error_dt_dt}")
            print (f"maximum {a} d error {max_error_d:.1f} km on {max_error_d_dt}")


    def test_all_phases_moon(self):
        #  2019 Jan  6  1:30        2019 Jan 21  5:17
        data = lunarphases.phases(dt=datetime(2019, 1, 1).replace(tzinfo=pytz.utc), days=30)
        self.assertEqual(4, len(data))

    def test_full_new_moon(self):
        data = lunarphases.phases(dt=datetime(2019, 1, 1).replace(tzinfo=pytz.utc), days=365,
                                  phases=[0,2])
        self.assertEqual(2, len(data))

    def test_full_moon(self):
        new_date = datetime(2019, 1, 1).replace(tzinfo=pytz.utc)
        data = lunarphases.phases(dt=new_date, days=365, phases=[2])
        dt, d = apsis.next_perigee(dt=new_date, days=365)
        # pprint(data)
        print(new_date)
        pprint(dt)
        pprint(d)
        # for k, v in data.items():
        #     print (k)
        #     print (nearestDate(k, dt))
        # self.assertEqual(2, len(data))

if __name__ == '__main__':
    unittest.main()

Finds instances of supermoon.  For more information see the [wikipedia page on the subject](https://en.wikipedia.org/wiki/Supermoon).
```
usage: supermoon [-h] [--cnt CNT] [-P] [-B] [year] [endyear]

positional arguments:
  year           find supermoons for this year (optional, defaults to current date forward)
  endyear        stop finding supermoons for this year (optional)

optional arguments:
  -h, --help     show this help message and exit
  --cnt CNT      moons to show
  -P, --perigee  include perigee time
  -B, --brief    brief output
```

Definitions used:
* Richard Nole (coined the term in 1979): A full or new Moon occurring at a 
  distance 90% or greater than the closest perigee for the calendar year.
  [source](https://www.astropro.com/features/tables/cen21ce/suprmoon.html)
* Fred Espenak (retired NASA astrophysicist, best known for lunar and solar 
  eclipse predictions)- A full Moon occurring at a distance 90% or greater 
  of perigee during the current lunation.
  [source](http://astropixels.com/ephemeris/moon/fullperigee2001.html)
* EarthSky (astronomy radio series/blog) - A full Moon occurring within 361,885 km
  [source](http://earthsky.org/astronomy-essentials/why-experts-disagree-on-what-makes-a-supermoon#nolle)
* Sky and Telescope magazine - A full Moon occurring within 223,000 miles (358,884 km)
  [source](https://skyandtelescope.org/observing/what-is-a-supermoon/)
* TimeandDate.com (Norwegian company offering website and data services on 
  time and astronomy)- A full Moon within 360,000 kilometers (223,694 mi) 
  [source](https://www.timeanddate.com/astronomy/moon/super-full-moon.html)
* additionally, full moons occurring within 24 hours of perigee have been labeled as supermoons    
```
4 supermoons during 2020:
  Sun 02/09/2020 02:33 AM EST (07:33 UTC) according to Espenak
  Mon 03/09/2020 01:47 PM EDT (17:47 UTC) according to all known definitions
  Tue 04/07/2020 10:35 PM EDT (02:35 UTC) according to all known definitions
  Thu 05/07/2020 06:45 AM EDT (10:45 UTC) according to Espenak, and, Nolle
4 supermoons during 2021:
  Sun 03/28/2021 02:48 PM EDT (18:48 UTC) according to Espenak
  Mon 04/26/2021 11:31 PM EDT (03:31 UTC) according to all known definitions
  Wed 05/26/2021 07:13 AM EDT (11:13 UTC) according to all known definitions
  Thu 06/24/2021 02:39 PM EDT (18:39 UTC) according to Espenak, and, Nolle
4 supermoons during 2022:
  Mon 05/16/2022 12:14 AM EDT (04:14 UTC) according to Espenak, and, Nolle
  Tue 06/14/2022 07:51 AM EDT (11:51 UTC) according to all known definitions
  Wed 07/13/2022 02:37 PM EDT (18:37 UTC) according to all known definitions
  Thu 08/11/2022 09:35 PM EDT (01:35 UTC) according to Espenak, and, Nolle
4 supermoons during 2023:
  Mon 07/03/2023 07:38 AM EDT (11:38 UTC) according to Espenak
  Tue 08/01/2023 02:31 PM EDT (18:31 UTC) according to all known definitions
  Wed 08/30/2023 09:35 PM EDT (01:35 UTC) according to all known definitions
  Fri 09/29/2023 05:57 AM EDT (09:57 UTC) according to Espenak, and, Nolle
4 supermoons during 2024:
  Mon 08/19/2024 02:25 PM EDT (18:25 UTC) according to Espenak
  Tue 09/17/2024 10:34 PM EDT (02:34 UTC) according to all known definitions
  Thu 10/17/2024 07:26 AM EDT (11:26 UTC) according to all known definitions
  Fri 11/15/2024 04:28 PM EST (21:28 UTC) according to Espenak
3 supermoons during 2025:
  Mon 10/06/2025 11:47 PM EDT (03:47 UTC) according to Espenak, and, Nolle
  Wed 11/05/2025 08:19 AM EST (13:19 UTC) according to all known definitions
  Thu 12/04/2025 06:14 PM EST (23:14 UTC) according to all known definitions
3 supermoons during 2026:
  Sat 01/03/2026 05:02 AM EST (10:02 UTC) according to Espenak
  Tue 11/24/2026 09:53 AM EST (14:53 UTC) according to Espenak, and, Nolle
  Wed 12/23/2026 08:28 PM EST (01:28 UTC) according to all known definitions
3 supermoons during 2027:
  Fri 01/22/2027 07:17 AM EST (12:17 UTC) according to all known definitions
  Sat 02/20/2027 06:23 PM EST (23:23 UTC) according to Espenak
  Mon 12/13/2027 11:08 AM EST (16:08 UTC) according to Espenak
4 supermoons during 2028:
  Tue 01/11/2028 11:03 PM EST (04:03 UTC) according to Espenak, and, Nolle
  Thu 02/10/2028 10:03 AM EST (15:03 UTC) according to all known definitions
  Fri 03/10/2028 08:06 PM EST (01:06 UTC) according to all known definitions
  Sun 04/09/2028 06:26 AM EDT (10:26 UTC) according to Espenak
5 supermoons during 2029:
  Tue 01/30/2029 01:03 AM EST (06:03 UTC) according to Espenak
  Wed 02/28/2029 12:10 PM EST (17:10 UTC) according to Time & Date, Espenak, and, Nolle
  Thu 03/29/2029 10:26 PM EDT (02:26 UTC) according to all known definitions
  Sat 04/28/2029 06:36 AM EDT (10:36 UTC) according to all known definitions
  Sun 05/27/2029 02:37 PM EDT (18:37 UTC) according to Espenak
5 supermoons during 2030:
  Tue 03/19/2030 01:56 PM EDT (17:56 UTC) according to Espenak
  Wed 04/17/2030 11:20 PM EDT (03:20 UTC) according to Time & Date, Espenak, and, Nolle
  Fri 05/17/2030 07:19 AM EDT (11:19 UTC) according to all known definitions
  Sat 06/15/2030 02:41 PM EDT (18:41 UTC) according to all known definitions
  Sun 07/14/2030 10:12 PM EDT (02:12 UTC) according to Espenak
5 supermoons during 2031:
  Tue 05/06/2031 11:39 PM EDT (03:39 UTC) according to Espenak
  Thu 06/05/2031 07:58 AM EDT (11:58 UTC) according to Time & Date, Espenak, and, Nolle
  Fri 07/04/2031 03:01 PM EDT (19:01 UTC) according to all known definitions
  Sat 08/02/2031 09:45 PM EDT (01:45 UTC) according to all known definitions
  Mon 09/01/2031 05:20 AM EDT (09:20 UTC) according to Espenak
5 supermoons during 2032:
  Wed 06/23/2032 07:32 AM EDT (11:32 UTC) according to Espenak
  Thu 07/22/2032 02:51 PM EDT (18:51 UTC) according to Time & Date, Espenak, Nolle, and, within 1 day of perigee
  Fri 08/20/2032 09:46 PM EDT (01:46 UTC) according to all known definitions
  Sun 09/19/2032 05:30 AM EDT (09:30 UTC) according to all known definitions
  Mon 10/18/2032 02:58 PM EDT (18:58 UTC) according to Espenak
5 supermoons during 2033:
  Wed 08/10/2033 02:07 PM EDT (18:07 UTC) according to Espenak
  Thu 09/08/2033 10:20 PM EDT (02:20 UTC) according to Time & Date, Espenak, Nolle, and, within 1 day of perigee
  Sat 10/08/2033 06:58 AM EDT (10:58 UTC) according to all known definitions
  Sun 11/06/2033 03:32 PM EST (20:32 UTC) according to all known definitions
  Tue 12/06/2033 02:22 AM EST (07:22 UTC) according to Espenak
4 supermoons during 2034:
  Wed 09/27/2034 10:56 PM EDT (02:56 UTC) according to Espenak
  Fri 10/27/2034 08:42 AM EDT (12:42 UTC) according to all known definitions
  Sat 11/25/2034 05:32 PM EST (22:32 UTC) according to all known definitions
  Mon 12/25/2034 03:54 AM EST (08:54 UTC) according to Time & Date, Espenak, Nolle, and, within 1 day of perigee
3 supermoons during 2035:
  Tue 01/23/2035 03:16 PM EST (20:16 UTC) according to Espenak
  Thu 11/15/2035 08:48 AM EST (13:48 UTC) according to Espenak
  Fri 12/14/2035 07:33 PM EST (00:33 UTC) according to all known definitions
(.venv) trice@Tonys-MacBook-Pro supermoon % 



```

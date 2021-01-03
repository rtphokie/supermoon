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
  time and astronomy)- A full Moon within 360,000 kilometres (223,694 mi) 
  [source](https://www.timeanddate.com/astronomy/moon/super-full-moon.html)
* additionally, full moons occurring within 24 hours of perigee have been labeled as supermoons    
```
4 supermoons during 2021:
  Sun 03/28/2021 02:48 PM EDT (18:48 UTC) 362,173.8 km (225,044.3 mi) according to Espenak
   perigee: 03/30/2021 02:15 EDT (35.46 hours from full moon) 360,309.0 km (223,885.6 mi)
  Mon 04/26/2021 11:31 PM EDT (03:31 UTC) 357,616.1 km (222,212.3 mi) according to all known definitions
   perigee: 04/27/2021 11:22 EDT (11.85 hours from full moon) 357,378.0 km (222,064.3 mi)
  Wed 05/26/2021 07:13 AM EDT (11:13 UTC) 357,461.0 km (222,115.9 mi) according to all known definitions
   perigee: 05/25/2021 21:49 EDT (9.40 hours from full moon) 357,311.0 km (222,022.7 mi)
  Thu 06/24/2021 02:39 PM EDT (18:39 UTC) 361,560.8 km (224,663.4 mi) according to EarthSky, Espenak, and, Nolle
   perigee: 06/23/2021 05:54 EDT (32.75 hours from full moon) 359,956.0 km (223,666.2 mi)


4 supermoons during 2020:
  Sun 02/09/2020 02:33 AM EST (07:33 UTC) according to Espenak
   perigee: 02/10/2020 15:27 EST (36.91 hours from full moon)
  Mon 03/09/2020 01:47 PM EDT (17:47 UTC) according to all known definitions
   perigee: 03/10/2020 02:29 EDT (12.70 hours from full moon)
  Tue 04/07/2020 10:35 PM EDT (02:35 UTC) according to all known definitions
   perigee: 04/07/2020 14:08 EDT (8.44 hours from full moon)
  Thu 05/07/2020 06:45 AM EDT (10:45 UTC) according to EarthSky, Espenak, and Nolle
   perigee: 05/05/2020 23:02 EDT (31.71 hours from full moon)
```

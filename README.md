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

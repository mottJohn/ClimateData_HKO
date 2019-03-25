# Introduction
Currently, Hong Kong Observatory does not provide an API access to their data. Mannually copy and paste data for large analysis is not ideal. If you look more closely the Website, you will find the data is actually loaded in XML, JSON, or CSV format. It is actually quite easy to extract.

# Usage
1. scrapPressureWind.py
    * Extract [daily extract of Meteorological Observations](http://www.hko.gov.hk/cis/dailyExtract_e.htm?y=2015&m=05)
    * Sample Data in MetData/
2. scrapStormSurveRecords.py
    * Extract [storm surge records](https://www.hko.gov.hk/wservice/tsheet/pms/stormsurgedb_e.htm) in Hong Kong
3. scrapTideData.py
    * Extract [daily observed sea levels](http://www.hko.gov.hk/cis/dailyTide_e.htm?stn=QUB&y=1971&m=1 ) at different stations
    * Sample Data in tideData/
4. seriousTyhoon.py
    * Code to summarize tide data for 6 most severe typhoon since Year 2000.
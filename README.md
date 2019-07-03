# HYDEX (HYDAT DATA EXTRACTION)

The utility code for transfer of .ts3 HYDAT flow to NetCDF.

## benefits of using this code

All the streamflow values will be converted to NetCDF file instead of ts3 format.

It is easier to read and compare them.

The data retreval is faster.

Similar starting and ending point for all the data for all the gauges.

Filling of the missing values between the starting and ending point.

## How to use

Open the Environemtn Canada and Climate Change Data Explorer ([ECCCDataExplorer](https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/explorer.html)).

Select the gauges which you are interested in by filtering the station ID, minumume area, minimume time length of the record.

Save the selected gugaes as ts3 format in a folder by selecting part of all of the stations.

Run the ts3_to_HYDAT.py by directing to the folder and ts3.

Enjoy!

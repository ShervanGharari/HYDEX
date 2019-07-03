# HYDEX (HYDAT DATA EXTRACTION)

The utility code for transfer of .ts3 HYDAT flow to NetCDF.

## Benefits of using this code

All the streamflow values will be converted to NetCDF file instead of ts3 format.

It is easier to read and compare gauges.

The data retrieval is faster.

Similar starting and ending point for all the data for all the gauges.

Filling of the missing values with NaNs.

## How to use

Open the Environemtn Canada and Climate Change Data Explorer ([ECCCDataExplorer](https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/explorer.html)).

Select the gauges which you are interested in by filtering the station ID, minumume area, minimume time length of the record.

![image](https://github.com/ShervanGharari/HYDEX/blob/master/figs/Fig_1.jpg)

Selected part or all (by right click and select all) of the filtered gugaes.

![image](https://github.com/ShervanGharari/HYDEX/blob/master/figs/Fig_2.jpg)

Export the data into ts3 by choosing export and selecting flow (or other variable, notice that the name in nc file should be ajusted accordignly) into the target folder.

![image](https://github.com/ShervanGharari/HYDEX/blob/master/figs/Fig_3.jpg)

![image](https://github.com/ShervanGharari/HYDEX/blob/master/figs/Fig_4.jpg)

Run the ts3_to_HYDAT.py by directing to the folder that the ts3 files are saved, also indicate the locaiton and name of the NetCDF file.

Enjoy!

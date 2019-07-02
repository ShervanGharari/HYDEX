# HYDEX
The utility code for transfer of .ts3 HYDAT flow to NetCDF.

## benefits of using this code

All the streamflow values will be converted to NetCDF file.

It is easier to read and compare them.

The data retreval is faster.

## How to use

open the Environemtn canada data Explorer ().

select the gauges which you are interested by filtering the names, area, etc.

save the selected gugaes as ts3 format in a folder.

run the ts3_to_HYDAT.py by directing to the folder and ts3.

and enjoy the resulting netcdf which includes streamflow, flags, area of everygages. the code put NaN values for the missing date between the stargint and ending point so it makes ut easier to find the result. sorting 400 gauges took less than hour.

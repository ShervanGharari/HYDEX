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

Run the ts3_to_nc.py by directing to the folder that the ts3 files are saved, also indicate the locaiton and name of the NetCDF file.

Enjoy!

## For use on Plato or Graham

Load the desirable python version:

```$>module load python/3.5```

Then make the packages by [virtual environment](https://docs.computecanada.ca/wiki/Python#:~:text=Creating%20and%20using%20a%20virtual%20environment,can%20easily%20install%20Python%20packages.&text=We%20recommend%20that%20you%20create,s)%20in%20your%20home%20directory.) or simply typing:

```$>pip install --user <name of the package>```

Clone the HYDEX by:

```$>git clone https://github.com/ShervanGharari/HYDEX.git```

Change the three line of ```ts3_to_nc.py``` specified for the user to change.

Add the interpreteation line. For that type:

```$>which python```

```/cvmfs/soft.computecanada.ca/easybuild/software/2017/Core/python/3.5.4/bin/python```

Copy the line, add ```#!``` in the begining of the line and copy it as the first line of the file ```ts3_to_nc.py```

Make the file executable by:

```$>chmod +x ./ts3_to_nc.py```

Run the file:

```$>./ts3_to_nc.py```

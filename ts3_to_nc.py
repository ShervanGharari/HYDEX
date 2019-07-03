'''
This code converts the ts3 data frmat from ECCCDataExplorer to NetCDF.

Authour: Shervan Gharari (https://github.com/ShervanGharari/HYDEX; sh.gharari@gmail.com)

MIT License

Copyright (c) 2019 Shervan Gharari

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# load all the necessary modules and packages
import pandas as pd
import numpy as np
import re as re
import datetime
import matplotlib.pyplot as plt # if the user want to visualize the result
import glob
import os
import netCDF4 as nc4
import time


#####################
# user specify the code
#####################
file_names = glob.glob('F:/HYDAT/data_ts3/*Daily_Flow*') # name of the streamflow
nc_name = "F:/HYDAT/data_ts3/Final.nc" # the name of the nc file to be written
discription_of_data = 'described 417 basins of HYDAT data set with starting from 05 (Station ID 05XXXXX)\
flow and length of more than 10 years and area of more than 100 km2'


#####################
# creation of some varibale
idx = pd.date_range('01-01-1850', '01-01-2020') # starting and ending time for the streamflow to be saved
t = len(idx) # number of time steps
n = np.array(len(file_names)) # number of station

#####################
# defenition of subroutines
# defenition to find the end of a header line given the line look_up text such as ":endheader"
def find_line_number_for_text(name_of_file,lookup_text):
    with open(name_of_file) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup_text in line:
                return num

            # read the content
def read_info_from_header(name_of_file,lookup_text):            
    with open(name_of_file) as myFile:
        for line in myFile:
            if line.startswith(lookup_text):
                return line.partition(lookup_text)[2].strip()

#####################
# extraction of data from ts3
#####################
lat_all = None
lon_all = None
Station_all = None
StationName_all = None
DrainageArea_all = None
DrainageAreaEff_all = None
NoDataValue_all = None

flows_all = np.array([n,t,])
flags_all = np.chararray([n,t,])


for i in np.arange(n):
    
    file_name = file_names [i]
    print(i)
    print(file_name)
    
    # first find the line the header finishes
    line_header_ends = None
    line_header_ends = find_line_number_for_text(file_name,':EndHeader')
    print(line_header_ends)
    
    # read the lat of the station
    lat = read_info_from_header(file_name,':LocationX')
    lat = float(lat)
    
    # read the lon of the station
    lon = read_info_from_header(file_name,':LocationY')
    lon = float(lon)
    
    # read the Station ID
    Station = read_info_from_header(file_name,':Station')        
    
    # read the Station name
    StationName = read_info_from_header(file_name,':StationName')
    
    # read the dranage area
    DrainageArea = read_info_from_header(file_name,':DrainageArea')
    DrainageArea = DrainageArea.strip('km²')
    DrainageArea = float(DrainageArea)
    if DrainageArea == '':
        DrainageArea = -1
    else:
        DrainageArea = float(DrainageArea)
    
    DrainageAreaEff = read_info_from_header(file_name,':DrainageAreaEff')
    DrainageAreaEff = DrainageAreaEff.strip('km²')
    if DrainageAreaEff == '':
        DrainageAreaEff = -1
    else:
        DrainageAreaEff = float(DrainageAreaEff)
        
        
    NoDataValue = read_info_from_header(file_name,':NoDataValue')
    NoDataValue = float(NoDataValue)
    
    #######################
    # NOTICE: this can be written with pd.csvread but there was issues with some of the files so here we go line by line
    # however due to some error that was happening for few of the ts3 files the manual code is used instead
    #######################
    lines = open(file_name).read().split('\n')
    lines_as_array = np.asarray(lines) # put lines in arrays
    lines_as_array=np.delete(lines_as_array, range(0,(int(line_header_ends))),axis=0) # remove the header
    
    date_vec = np.zeros((len(lines_as_array)-1,6)) #-1 because the last line of data is empty (/n)
    values = np.zeros((len(lines_as_array)-1,1)) #-1 because the last line of data is empty (/n)
    flags = np.chararray((len(lines_as_array)-1,1)) #-1 because the last line of data is empty (/n)
    
    for number in range(0,len(lines_as_array)-1,1): # -1 not to account for the last line whcih is empty (/n)
    
        lines_split = re.split('/|:| ',lines_as_array[number]) # replace the date using / and : to its numbers
        
        date_vec[number,0] = float(lines_split[0])
        date_vec[number,1] = float(lines_split[1])
        date_vec[number,2] = float(lines_split[2])
        date_vec[number,3] = float(lines_split[3])
        date_vec[number,4] = float(lines_split[4])
        date_vec[number,5] = 0
        
        values[number,0] = lines_split[5] # values
    
        flags[number,0] = lines_split[6] # flags
    
    
    data = pd.DataFrame()
    # read the data and have them in data frame
    data['year'] = np.array(date_vec[:,0])
    data['month'] = np.array(date_vec[:,1])
    data['day'] = np.array(date_vec[:,2])
    data['hour'] = np.array(date_vec[:,3])
    data['minute'] = np.array(date_vec[:,4])
    data['flow'] = values[:,0]
    data['flags'] = flags[:,0]
    #print(data)
    
    #int the above or this will work
    data ['Date'] = pd.to_datetime(data.year*10000+data.month*100+data.day,format='%Y%m%d')
    data.index = pd.DatetimeIndex(data['Date'])
    
    # for the flow values the missing values are set to -1
    data_temp = data
    data_temp = data_temp.reindex(idx, fill_value=-1)
    data_temp['flow'].replace(to_replace=[None], value=-1, inplace=True)
    data_temp['flow'].replace(to_replace=NoDataValue, value=-1, inplace=True)
    flows = np.array(data_temp ['flow'])
    
    # data['flags'].replace('None', ' ', inplace=True)
    data_temp = data
    data_temp = data_temp.reindex(idx, fill_value='')
    data_temp['flags'].replace(to_replace=[None], value=[''], inplace=True)
    flags = data_temp['flags']
    
    print(Station)
    # put the informaiton, flow, flags into a numpy array
    if i == 0:
        lat_all = np.array(lat)
        lon_all = np.array(lon)
        Station_all = list([Station])
        StationName_all = list([StationName])
        DrainageArea_all = np.array(DrainageArea)
        DrainageAreaEff_all = np.array(DrainageAreaEff)
        NoDataValue_all = np.array(NoDataValue)
        flows_all = flows
        flags_all [i,:] = flags
    else:
        lat_all = np.append(lat_all,lat)
        lon_all = np.append(lon_all,lon)
        Station_all.append(Station)
        StationName_all.append(StationName)
        DrainageArea_all = np.append(DrainageArea_all,DrainageArea)
        DrainageAreaEff_all = np.append(DrainageAreaEff_all,DrainageAreaEff)
        NoDataValue_all = np.append(NoDataValue_all,NoDataValue)
        flows_all = np.append(flows_all, flows)
        flags_all [i,:] = flags

Station_all = np.array(Station_all, dtype='object')
StationName_all = np.array(StationName_all, dtype='object')


#####################
# NetCDF creation
#####################
ncid = nc4.Dataset("HYDAT_guages.nc", "w", format="NETCDF4")

dimid_n_station = ncid.createDimension('n',n)
dimid_T = ncid.createDimension('time',t)

#####################
# Variables time
#####################
time_varid = ncid.createVariable('time','i4',('time',))

# Attributes
time_varid.long_name     = 'time'
time_varid.units         = 'days since 1850-01-01 00:00:00'
time_varid.calendar      = 'gregorian'
time_varid.standard_name = 'time'
time_varid.axis          = 'T'

# Write data
time_varid[:] = np.arange(t)

#####################
# Variables flow
#####################
Daily_flow_varid = ncid.createVariable('Flow','f8',('n','time',),fill_value=-1)

# Attributes
Daily_flow_varid.long_name     = 'Daily flow'
Daily_flow_varid.units         = 'm3 s-1'
Daily_flow_varid.coordinates    = 'lon lat Station_ID'

# Write data
Daily_flow_varid[:] = flows_all # should be transpose

#####################
## varibale falg
#####################

Flags_varid = ncid.createVariable('flags','S1',('n','time',))

# Attributes
Flags_varid.long_name     = 'flags'
Flags_varid.units         = '1'


# Write data
temp = np.array([flags_all],dtype='S1')
print(temp)
Flags_varid[:] = nc4.stringtochar(temp)


#####################
# Variables DrainageAreaEff
#####################
Effective_area_varid = ncid.createVariable('DrainageAreaEff','f8',('n',),fill_value=-1)

# Attributes
Effective_area_varid.long_name     = 'Effective Drainage Area'
Effective_area_varid.units         = 'm2'

# Write data
Effective_area_varid[:] = DrainageAreaEff_all

#####################
# Variables DrainageArea
#####################
Area_varid = ncid.createVariable('DrainageArea','f8',('n',),fill_value=-1)

# Attributes
Area_varid.long_name     = 'Drainage Area'
Area_varid.units         = 'm2'

# Write data
Area_varid[:] = DrainageArea_all

#####################
# Variables lat and lon
#####################
lat_varid = ncid.createVariable('lat','f8',('n',))
lon_varid = ncid.createVariable('lon','f8',('n',))

# Attributes
lat_varid.long_name      = 'latitude'
lon_varid.long_name      = 'longitude'
lat_varid.units          = 'degrees_north'
lon_varid.units          = 'degrees_east'
lat_varid.standard_name  = 'latitude'
lon_varid.standard_name  = 'longitude'

# Write data
lat_varid[:] = lon_all
lon_varid[:] = lat_all

#####################
# varibale station ID
#####################
Station_ID_varid = ncid.createVariable('Station_ID',str,('n',))

# Attributes
Station_ID_varid.long_name     = 'Station ID'
Station_ID_varid.units         = '1'
Station_ID_varidcf_role        = 'timeseries_id'

# Write data
Station_ID_varid[:] = Station_all 

#####################
# name of the staiton
#####################
Station_Name_varid = ncid.createVariable('Station_Name',str,('n',))

# Attributes
Station_Name_varid.long_name     = 'Station Name'
Station_Name_varid.units         = '1'

# Write data
Station_Name_varid[:] = StationName_all


#####################
# ID
#####################
# Variables
#ID_varid = ncid.createVariable('ID','i4',('n',))

# Attributes
#ID_varid.long_name     = 'an arbitrary ID'
#ID_varid.units         = '1'

# Write data
#ID_varid[:] = np.arange(n)+1

#####################
# header 
#####################
ncid.Conventions = 'CF-1.6'
ncid.License     = 'The file is created by Shervan Gharari, under GPL3, https://github.com/ShervanGharari/HYDEX'
ncid.history     = 'Created ' + time.ctime(time.time())
ncid.source      = discription_of_data

#####################
ncid.close()

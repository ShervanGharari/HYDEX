
# coding: utf-8

# In[1]:


# section 1 load all the necessary modules and packages
import pandas as pd
import numpy as np
import re as re
import datetime
import matplotlib.pyplot as plt
import glob
import os
import netCDF4 as nc4
import time


# In[2]:


# defenition of subroutines
# defenition to find the end of a header line given the line look_up text such as ":endheader"
def find_line_number_for_text(name_of_file,lookup_text):
    with open(name_of_file) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup_text in line:
                return num
            
def read_info_from_header(name_of_file,lookup_text):            
    with open(name_of_file) as myFile:
        for line in myFile:
            if line.startswith(lookup_text):
                return line.partition(lookup_text)[2].strip()


# In[3]:


file_names = glob.glob('C:/Users/shg096/Dropbox/*Daily_Flow*') # name of the streamflow
idx = pd.date_range('01-01-1850', '01-01-2020') # starting and ending time for the streamflow to be saved
t = len(idx) # number of time steps
n = np.array(len(file_names)) # number of station


# In[4]:


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
    
    # first find the line the header finishes
    line_header_ends = find_line_number_for_text(file_name,':EndHeader')
    
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
    
    
    # read the data and have them in data frame
    data = None
    data = pd.read_csv(file_name, sep=' |:|/', header=line_header_ends)
    data.columns = ["year", "month", "day", "hour", "minute","flow", "flags"]
    
    # in 0.13 the above or this will work
    data ['Date'] = pd.to_datetime(data.year*10000+data.month*100+data.day,format='%Y%m%d')
    data.index = pd.DatetimeIndex(data['Date'])
    
    # for the flow values the missing values are set to -1
    data_temp = data
    data_temp = data_temp.reindex(idx, fill_value=-1)
    data_temp['flow'].replace(to_replace=[None], value=-1, inplace=True)
    flows = np.array(data_temp ['flow'])
    
    # data['flags'].replace('None', ' ', inplace=True)
    data_temp = data
    data_temp = data_temp.reindex(idx, fill_value=' ')
    data_temp['flags'].replace(to_replace=[None], value=[' '], inplace=True)
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
        print(Station_all)
    else:
        print(Station_all)
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


# In[5]:


# creating an netCFD file given the data

ncid = nc4.Dataset("NetCDF_Python_10_test113.nc", "w", format="NETCDF4")

dimid_n_station = ncid.createDimension('n',n)
dimid_T = ncid.createDimension('time',t)


# In[6]:


# Variables
time_varid = ncid.createVariable('time','i4',('time',))

# Attributes
time_varid.long_name     = 'time'
time_varid.units         = 'days since 1850-01-01 00:00:00'
time_varid.calendar      = 'gregorian'
time_varid.standard_name = 'time'
time_varid.axis          = 'T'

# Write data
time_varid[:] = np.arange(t)


# In[7]:


# Variables
Daily_flow_varid = ncid.createVariable('Flow','f8',('n','time',),fill_value=-1)

# Attributes
Daily_flow_varid.long_name     = 'Daily flow'
Daily_flow_varid.units         = 'm3 s-1'
Daily_flow_varid.coordinates    = 'lon lat Station_ID'

# Write data
Daily_flow_varid[:] = flows_all # should be transpose


# In[8]:


## falg as string

Flags_varid = ncid.createVariable('flags','S1',('n','time',))

# Attributes
Flags_varid.long_name     = 'flags'
Flags_varid.units         = '1'


# Write data
temp = np.array([flags_all],dtype='S1')
print(temp)
Flags_varid[:] = nc4.stringtochar(temp) # manual conversion to char array
Flags_varid._Encoding = 'ascii'


# In[9]:


# Variables
Effective_area_varid = ncid.createVariable('DrainageAreaEff','f8',('n',),fill_value=-1)

# Attributes
Effective_area_varid.long_name     = 'Effective countributing area'
Effective_area_varid.units         = 'm2'

# Write data
Effective_area_varid[:] = DrainageAreaEff_all # should be transpose


# In[10]:


# Variables
Area_varid = ncid.createVariable('DrainageArea','f8',('n',),fill_value=-1)

# Attributes
Area_varid.long_name     = 'Effective countributing area'
Area_varid.units         = 'm2'

# Write data
Area_varid[:] = DrainageArea_all # should be transpose


# In[11]:


# Variables
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


# In[12]:


Station_ID_varid = ncid.createVariable('Station_ID',str,('n',))

# Attributes
Station_ID_varid.long_name     = 'Station ID'
Station_ID_varid.units         = '1'
Station_ID_varidcf_role        = 'timeseries_id'

# Write data
Station_ID_varid[:] = Station_all # should be transpose


# In[13]:


Station_Name_varid = ncid.createVariable('Station_Name',str,('n',))

# Attributes
Station_Name_varid.long_name     = 'Station Name'
Station_Name_varid.units         = '1'

# Write data
Station_Name_varid[:] = StationName_all


# In[14]:


# ID
# Variables
ID_varid = ncid.createVariable('ID','i4',('n',))

# Attributes
ID_varid.long_name     = 'ID of station in correspondant to shapefile'
ID_varid.units         = '1'

# Write data
ID_varid[:] = np.arange(n)+1


# In[15]:


ncid.Conventions = 'CF-1.6'
ncid.License     = 'The file is created by Shervan Gharari, NHRC, Saskatoon under GPL3'
ncid.history     = 'Created ' + time.ctime(time.time())
#ncid.source      = 'The file contains data from 417 stations (starts with 05 WSC). The data is converted from ts3 format generated by EC Explorer for gauges with more than 10 years of data and 100 KM2 drainagae area which have both flow and water level'
ncid.source      = 'The file contains data from many selected stations. The data is converted from ts3 format generated by EC Explorer for gauges with more than 10 years of data and 100 KM2 drainagae area'


# In[16]:


ncid.close()


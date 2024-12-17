#!/usr/bin/env python
# coding: utf-8

# In[8]:


# Import libraries
import pandas as pd
import geopandas as gpd


# In[9]:


# Read files

## api_data comes from the API
api_data = pd.read_excel('data/api_data.xlsx')

## cpc_id_names was manually created from this website: https://www.uspto.gov/web/patents/classification/cpc/html/cpc.html
cpc_id_names = pd.read_excel('data/cpc_id_names.xlsx')

## shapefile comes from FDGL catalog: https://fgdl.org/ords/r/prod/fgdl-current/catalog
shapefile = gpd.read_file('data/florida_shapefile/florida_counties.shp')


# In[10]:


# Merge both api_data and cpc_id_names on cpc_section_id
fl_patents_with_cpc_names = api_data.merge(cpc_id_names, left_on='cpc_section_id', right_on='cpc_section_id', how='left')


# In[11]:


# Extract 'NAME' and 'COUNTYFP' which will be used as the main County name field for the final dataset
shapefile_filtered = shapefile[['NAME', 'COUNTYFP']]


# In[18]:


# Convert 'assignee_county_fips' from float to string and add leading zeros so that it matches the shapefile's format
fl_patents_with_cpc_names["assignee_county_fips"] = (fl_patents_with_cpc_names["assignee_county_fips"]
                                     .fillna(0)
                                     .astype(int)
                                      .astype(str)
                                      .str.zfill(3)
                                     )


# In[23]:


# Merge the file file with cpc_section_id_names with the shape_filtered file
fl_patents_final = fl_patents_with_cpc_names.merge(shapefile_filtered, left_on='assignee_county_fips', right_on='COUNTYFP', how='left')


# In[22]:


# Remove the COUNTYFP column and instead use the assignee_county_fips
fl_patents_final.drop('COUNTYFP', axis=1, inplace=True)


# In[24]:


# Rename NAME to county_name
fl_patents_final = fl_patents_final.rename(columns={'NAME': 'county_name'})


# In[25]:


# Save excel
fl_patents_final.to_excel('data/fl_patents_final.xlsx')


# In[ ]:





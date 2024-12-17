#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import libraries
import pandas as pd
import geopandas as gpd


# In[2]:


# Read data
shapefile = gpd.read_file('data/florida_shapefile/florida_counties.shp')
api_data = pd.read_excel('data/api_data.xlsx')


# In[3]:


# Drop first column
api_data.drop('Unnamed: 0', axis=1, inplace=True)


# In[4]:


# Convert 'assignee_county_fips' from float to string and add leading zeros so that it matches the shapefile's format
api_data["assignee_county_fips"] = (api_data["assignee_county_fips"]
                                     .fillna(0)
                                     .astype(int)
                                      .astype(str)
                                      .str.zfill(3)
                                     )


# In[6]:


# Group by 'assignee_county_fips', count unique 'patent_number', and keep 'NAME'
api_data_count = api_data.groupby('assignee_county_fips').agg(
    unique_patent_count=('patent_number', 'nunique'),
    patent_number=('patent_number', 'first')
).reset_index()


# In[9]:


# Extract 'unique_patent_count' and 'assignee_county_fips'
api_data_count_filtered = api_data_count[['assignee_county_fips', 'unique_patent_count']]


# In[12]:


# Merge api filtered data with shapefile
fl_patents_map_data = api_data_count_filtered.merge(shapefile, left_on='assignee_county_fips', right_on='COUNTYFP', how='left')


# In[13]:


fl_patents_map_data.head(2)


# In[15]:


# Save
fl_patents_map_data.to_csv = 'data/fl_patents_map_data.csv'


# In[ ]:





# In[ ]:





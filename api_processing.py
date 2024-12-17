#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import libraries
import requests
import pandas as pd
import json


# In[2]:


# Get data from the US PatentsView API. The data is filtered by date, state, patent_kind B1, which is for patents issued for the first time and for US Companies or Coporations
url_one = 'https://api.patentsview.org/patents/query?q={"_and":[{"_gte":{"patent_date":"2020-01-01"}},{"assignee_state":"Fl"},{"patent_kind":"B1"},{"assignee_type":"2"}]}&f=["patent_number","patent_title","patent_date","patent_num_combined_citations","assignee_organization","assignee_county_fips","cpc_section_id"]&o={"per_page":10000,"page":1}'
response_one = requests.get(url_one)
fl_patents = response_one.json()


# In[3]:


# Parse out the json response
patent_data_one = []
for patent in fl_patents["patents"]:
    base_data = {
        "patent_number": patent["patent_number"],
        "patent_title": patent["patent_title"],
        "patent_date": patent["patent_date"],
        "patent_num_combined_citations": patent["patent_num_combined_citations"]
    }
        
    # Expand assignees
    for assignee in patent["assignees"]:
        assignee_data = base_data.copy()
        assignee_data.update({
            "assignee_county_fips": assignee["assignee_county_fips"],
            "assignee_organization": assignee["assignee_organization"],
            "assignee_key_id": assignee["assignee_key_id"]
        })
        patent_data_one.append(assignee_data)
        
    # Expand CPCs
    for cpc in patent["cpcs"]:
        cpc_data = base_data.copy()
        cpc_data["cpc_section_id"] = cpc["cpc_section_id"]
        patent_data_one.append(cpc_data)


# Create DataFrame
fl_patents = pd.DataFrame(patent_data_one)


# In[4]:


# Group by 'patent_number' and consolidate 'cpc_section_id' while keeping all columns
consolidated_fl_patents = fl_patents.groupby('patent_number', as_index=False).agg(
    {
        **{col: 'first' for col in fl_patents.columns if col != 'cpc_section_id'},  # Keep the first value for all other columns
        'cpc_section_id': lambda x: ', '.join(sorted(set(x.dropna().astype(str))))  # Combine and deduplicate 'cpc_section_id'
    }
)


# In[5]:


# Make sure values in 'cpc_section_id' are treated as lists
def convert_to_list(value):
    if pd.isna(value):  # Handle NaNs
        return []
    elif isinstance(value, list):  # If it's already a list, keep it
        return value
    elif isinstance(value, str):  # If it's a string, split by commas
        return [item.strip() for item in value.split(',')]
    else:  # If it's another type, convert it to a string and split
        return [str(value).strip()]

consolidated_fl_patents['cpc_section_id'] = consolidated_fl_patents['cpc_section_id'].apply(convert_to_list)

# Explode the 'cpc_section_id' column so each value has its own row
fl_patents_exploded = consolidated_fl_patents.explode('cpc_section_id')

# Rmove empty rows
fl_patents_exploded = fl_patents_exploded[fl_patents_exploded['cpc_section_id'] != '']


# In[6]:


fl_patents_exploded.to_excel('data/api_data.xlsx')


# In[ ]:





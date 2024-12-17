#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, request, send_file
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

# Load the patent data from Excel
patents_df = pd.read_excel("data/fl_patents_final.xlsx")

# Load the map data from CSV (for the dot density map)
map_data = pd.read_csv("data/fl_map_final.csv")

@app.route("/", methods=["GET"])
def index():
    # Get unique counties from the patent data
    counties = patents_df["county_name"].dropna().unique()

    # Create dot density map using Plotly
    fig = px.scatter_mapbox(
        map_data, lat="INTPTLAT", lon="INTPTLON", size="total_patents", 
        hover_name="NAME", hover_data={"total_patents": True, "INTPTLAT": False, "INTPTLON": False},
        color_discrete_sequence=["orange"], zoom=6, 
        center={"lat": 27.994402, "lon": -81.760254},
        title="Dot Density Map: Total Patents by County",
        labels={"total_patents": "Total New Patents"}
    )
    
    # Customize map 
    fig.update_layout(
        mapbox_style="carto-positron", margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    # Div for map to embed in HTML
    plot_div = fig.to_html(full_html=False)

    return render_template("index.html", counties=counties, plot_div=plot_div)

@app.route("/download", methods=["POST"])
def download():
    selected_county = request.form["county"]

    # Filter data based on selected county
    filtered_df = patents_df[patents_df["county_name"] == selected_county]

    # Save the filtered data to a CSV file
    output_file = f"filtered_patents_{selected_county}.csv"
    filtered_df.to_csv(output_file, index=False)

    # Send file to the user
    return send_file(output_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


# In[ ]:





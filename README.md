# florida_patents
This application provides an interactive platform for downloading and analyzing patents granted for the first time in Florida to a US company or corporation since 2020. It leverages the US Patent and Trademark Office (USPTO) API PatentView and visualization tools like Plotly and Mapbox to provide a user-friendly, and engaging visual representations of the data. It contains data from 01-01-2020 to 12-16-2024.

Core functionalities include:
1.	Patent County Data Download Tool:
- Download Florida patent data as an excel file.
- Excel file includes patent number, patent title, patent category, assignee organization, and granted date.
2.	Dot Density Map:
- Visualizes the distribution of patents across Florida counties.
- Dot sizes are dynamically scaled by the total patents per county.
- Interactive tooltips display county names and patent counts.

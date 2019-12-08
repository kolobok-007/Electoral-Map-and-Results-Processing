# Description
The goal of this project is to be able to visualize results from 2015 Canadian Federal Elections. It consists of two parts:

1. Python code to process input data into a useful format
2. [Tableau Public visualization](https://public.tableau.com/profile/mikhail.venkov#!/vizhome/CanadaFederalElectionResults2015/ResultsbyDistrict): interactive map for exploring the results.

At the start of this project, my plan was to to obtain the election results and then plot them on a map in Tableau. However, the map plotting proved to be a lot more challenging than I anticipated. Electoral districts do not directly corespond to any geographical areas that is included in Tableau. Tableau has a built in ability to plot by country, state/province, city, zip/postal code, etc but Canadian federal electoral districts were not included in this list. So I had to find my own way to draw the borders of each district. The first step was finding a data source that would include the information. The second step is to convert into a way that Tableau can use it. 

The borders of each district are provided as a part of [open source data](http://open.canada.ca/data/en/dataset/8f59e503-b267-4fd0-9d43-a03db366f11e) in a GML file which cannnot be used directly by Tableau. GML description can be found [here](https://en.wikipedia.org/wiki/Geography_Markup_Language). Essentially it's a XML-like type document containing names of districts and coordinates that define the borders of each district.

In order for Tableau to be able to draw electoral districs they needed to be formated in a certain way. It needs to be a CSV file containing lon and lat coordinates of each point as well as the order in which these points are connected. `Process_Electoral_Districts_Map.py` module extracts coordinate information from the GML file using `ElementTree` Python module and saves into a CSV file that Tableau can understand (polygon shapes).

After loading the border data into Tableau, one challange became appearant. There were too many points for Tableau to plot effectively. There were around 700K points defining the borders which had to be connected with lines. This significantly degraded the performance of the visualization. Such level of detail was also not necessary. `Polygon_Generalizer.py` module simplifies the polygon shapes which reduces the number of points to around 27K with a minimal detail loss. Tableau was now able to draw the shapes very quickly.

Processing the poll results was relatively simple compared to GML conversion. The results were provided on [Elections Canada website](http://enr.elections.ca/ElectoralDistricts.aspx?lang=e) in flat text file. The only data processing that needed to be done is to identify the winner in each ridding and slightly change the formatting.

The result is a fast interactive map visualization.

# Visualization
The visualization is hosted on Tablea Public which is a free hosting service provided by Tableau. It does not require an account or installation.

The interactive map can be found below. You can click on each electoral district (riding) to see the election results by party. Use the overlay toolbar to zoom in and out of the map.

[Tableau Public](https://public.tableau.com/profile/mikhail.venkov#!/vizhome/CanadaFederalElectionResults2015/ResultsbyDistrict)

# Python Modules
`Process_Electoral_Districts_Map.py`:
Processes GML map data and converts to a polygon CSV that can be used by visualization software such as Tableau.

`Polygon_Generalizer.py`:
Simplifies polygon map shapes which reduces the size of the shapes and improves performance at minimal detail loss.

`Process_Election_Results.py`:
Processes and summarizes election results.

# Data Sources
[Riding Borders](http://open.canada.ca/data/en/dataset/8f59e503-b267-4fd0-9d43-a03db366f11e)

[Election Results](http://enr.elections.ca/ElectoralDistricts.aspx?lang=e)

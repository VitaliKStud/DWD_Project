# Readme  still in progress
# DWD_Project

Code created with PyCharm Professional Student Version.

Interpreter: Python 3.10

# Used Packages
```
pip install os 
pip install ipyleaflet
pip install IPython.display / pip install IPython
pip install json
pip install itertools
pip install datetime
pip install bs4
pip install requests
pip install zipfile
pip install tkinter
pip install tkintermapview
pip install numpy
pip install scipy.spatial / pip install scipy
pip install matplotlib.pyplot / pip install matplotlib
pip install pandas
pip install gc
```
# Open Data sources
### Deutscher Wetterdienst
>![This is an image](https://www.dwd.de/SharedDocs/bilder/DE/logos/dwd/dwd_logo_258x69.png?__blob=normal&v=1)
> 
>https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/
### Open Streetmap 
>© OpenStreetMap-Mitwirkende siehe www.openstreetmap.org/copyright und www.opendatacommons.org

# Setup your code
## important files
>DwdMapCreater: generate a map in JupyterNotebook.
>
>DwdDict: set up your dictionaries.
>
>DwdGui: in progress. Will start a GUI in future.
>
>main: will be a compressed file for the setup.
## important setups
>add a local path for yout data @main.py ![img_1.png](img_1.png)
> 
> Create a folder named "Graphs" inside your **local_domain_** for your plots.
## important variables @main.py
>**looking_for_ = []** : Tells what type of measurement you are looking for. Check **DwdDict.py, title_dict**
> 
>**start_date_ and end_data_ = int(YYYYMMDDhhmm)**  : Tells the range of data you are looking for
> 
>**x_coordinate_ and y_coordinate_ = int(Long) and int(Lat)** : Latitude coordinates in germany
> 
>**z_coordinate_ = int(height)** : You can skip it for now
> 
>**k_factor_ = int()** : Tells how many stations you are looking for around the Latitude coordinates
> 
> **type_of_data_ = str()** : Tells what type of data you are looking for. Check **DwdDict.py, type_of_data_list**
> 
> **type_of_time_ = str()** : Tells what type of time you are looking for Check **Dwddict.py, type_of_time_list**

## important functions @main.py
>
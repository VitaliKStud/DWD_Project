
.. contents:: Table of Contents (for quick start)
    :depth: 3


Quick-Start
=======================================


=======================================
getting started with DwdMain module
=======================================


getting started: download air_temperature
*****************************************
.. warning::
   | **For windows user**: To avoid any issues with the path limit of windows, you should enable unlimited path on your machine.
   | Press Win+R -> REGEDIT -> HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\FileSystem -> LongPathEnabled -> set "1".
   | If LongPathEnabled doesn't show in your FileSystem, you can create a new REG_DWORD (DWORD (32-Bit)).

.. image:: _image/disable_windwos_path_limit.png
   :width: 1000
   :alt: test


.. code-block:: python


   from DwdMain import main_dwd
   main_dwd(local_domain="YOUR_PATH/", type_of_data="air_temperature").main_datascrapper(all=False)
   # Will download and unzip the data for air_temperature (historical, meta_data, now and recent) to YOUR_PATH/.
   main_dwd(local_domain="YOUR_PATH/", type_of_data="air_temperature").main_writer(type_of_data_list=["air_temperature"], all=False)
   # Will create some .json files inside .../extracted_files/ for faster loading times. This step is important. This .json files includes dates and paths for every station.

getting started: download all (air_temperatur, solar, wind, precipitation)
**************************************************************************

.. code-block:: python


   from DwdMain import main_dwd
   main_dwd(local_domain="YOUR_PATH/").main_datascrapper(all=True)
   # Will download and unzip all the data for air_temperatur, solar, wind, precipitation (historical, meta_data, now and recent) to YOUR_PATH/.
   main_dwd(local_domain="YOUR_PATH/").main_writer(all=True)
   # Will create some .json files inside .../extracted_files/ for faster loading times. This step is important. Inside this .json files will dates and paths for every station.

getting started: some station information
*****************************************

.. code-block:: python


   from DwdMain import main_dwd
   print(main_dwd(local_domain="YOUR_PATH/",type_of_data="air_temperature", type_of_time="historical").main_station_information("TU_00003"))
   # Let's get some information about a station.

   return:
   {'ID': 'TU_00003', 'von_datum': '1993-4-29', 'bis_datum': '2011-3-31', 'stationshoehe': 202,
   'geoBreite': 50.7827, 'geoLaenge': 6.0941, 'Stationsname': b'Aachen', 'Bundesland': b'Nordrhein-Westfalen', 'Aktivität': False}
   # Interesting... what else can we do?


   print(main_dwd(local_domain="YOUR_PATH/",type_of_data="air_temperature", type_of_time="historical").main_station_array())
   # Will return an array with all available stations for this type of data and this type of time.

   return:
   ['TU_00003' 'TU_00044' 'TU_00071' 'TU_00073' 'TU_00078' 'TU_00091' ... 'TU_15555' 'TU_15813' 'TU_19171' 'TU_19172']
   # What about active stations in my timedelta?


   start_data_ = 199401190000
   end_date = 199501010000
   print(main_dwd(local_domain="YOUR_PATH/",
                  type_of_data="air_temperature",
                  type_of_time="historical",
                  start_date=start_date_, end_date=end_date_).main_activ_stations_in_date())
   # Will return 3 arrays. Array 1: x-coordinates for active stations,
   # array 2: y-coordinates for active stations,
   # array 3: z-coordinates for active stations
   # array 4: station id's (with prefix) for active stations.

   return:
   array1: [ 6.0941, 13.9908, 13.4344,...]
   array2: [50.7827, 53.0316, 54.6791, 51.3744,...]
   array3: [ 202,   54,   42,  164,  393,    3,...]
   array4: ['TU_00003', 'TU_00164', 'TU_00183', 'TU_00198',...]

getting started: plots
***********************

.. code-block:: python


   from DwdMain import main_dwd
   main_dwd(local_domain="YOUR_PATH/", type_of_data="air_temperature", type_of_time="historical",).main_plotter_stations(projection=False)
   # Will plot two graphs. 3D and 2D as a "heatmap" for all the station of this type of data and this type of time.

.. image:: _image/german_stations_3dair_temperature.png
  :width: 500
  :alt: Alternative text

.. image:: _image/german_stations_2d_air_temperature.png
  :width: 500
  :alt: Alternative text

.. note::
   If projection == True, it will project heights in created 3D-plot on the "Stationshoehe" - axe.

getting started: maps
***********************

.. code-block:: python

   from DwdMain import main_dwd
   local_domain_ = r"YOUR_PATH/"
   looking_for_ = ["PP_10"]
   start_date_ = 199401190000
   end_date_   = 199501010000
   x_coordinate_ = 6.0941 #x-coordinates for your location
   y_coordinate_ = 50.7827 #y-coordinates for your location
   z_coordinate_ = 0 # not needed for now (maybe in future)
   k_factor_ = 10 # how many station are you looking for around your location? 10 means, it will find 10 next stations for your location
   type_of_data_ = "air_temperature"
   type_of_time_ = "historical"
   dwd = main_dwd( local_domain=local_domain_,
                   type_of_data=type_of_data_,
                   type_of_time=type_of_time_,
                   start_date=start_date_,
                   end_date=end_date_,
                   x_coordinate=x_coordinate_,
                   y_coordinate=y_coordinate_,
                   z_coordinate=z_coordinate_,
                   k_factor=k_factor_)
   dwd.main_data_map()
   # Is creating some .json files inside the .../MapCreater/
   # zip_data_activ: All the activ stations. (From "information".txt)
   # zip_data_active_in_date: All the activ stations in your date.
   # zip_data_near: Alle the activ stations around your location.
   # zip_data_not_activ: All the not activ stations. (From "information".txt)
   # zip_no_data: Alle the stations without data. (From "information".txt)
   # Is important for DwdMapCreator

   # now we saved the data. Let's show it on a map.
   from DwdMap import DwdMap
   DwdMap("NearStations").create_map()
   DwdMap("Stations").create_map()
   DwdMap("ActivInDate").create_map()
   # choose between "NearStations" , "Stations" , "ActivInDate"
   # "NearStations": Will plot all the stations (k_factor) near your location.
   # "Stations": Will plot all the available stations (for all times)
   # "ActivInDate": Will plot all the activ stations for your timedelta (end_time - start_time)

.. image:: _image/near_stations.png
  :width: 500
  :alt: Alternative text


.. image:: _image/stations.png
  :width: 500
  :alt: Alternative text


.. image:: _image/activ_in_date.png
  :width: 500
  :alt: test

© OpenStreetMap-Mitwirkende siehe www.openstreetmap.org/copyright und www.opendatacommons.org

.. note::
   You should open DwdMapCreator with Jupyter Notebooks. Otherwise it won't show the locations on a map. A lot of red locations on the second map. It means
   the data probably not up to date. You should update your data.

getting started: data-plots and calculations
********************************************
.. code-block:: python


   import os
   from DwdMain import main_dwd
   local_domain_ = r"YOUR_PATH/"
   os.chdir(local_domain_)
   looking_for_ = ["FF_10"]
   start_date_ = 199401190000
   end_date_   = 199402191020
   x_coordinate_ = 6.0941 # 7 for compare == False
   y_coordinate_ = 50.7827 # 51 for compare == False
   z_coordinate_ = 0 # not needed for now (maybe in future)
   k_factor_ = 7 # how many station are you looking for around your location? 7 means, it will find 7 next stations for your location
   compare_station_ = "wind_00003" # needed for comparing (don't forget to set the prefix (wind_)
   type_of_data_ = "wind"
   type_of_time_ = "historical"
   dwd = main_dwd(local_domain=local_domain_,
                  type_of_data=type_of_data_,
                  type_of_time=type_of_time_,
                  start_date=start_date_,
                  end_date=end_date_,
                  compare_station=compare_station_,
                  x_coordinate=x_coordinate_,
                  y_coordinate=y_coordinate_,
                  z_coordinate=z_coordinate_,
                  k_factor=k_factor_,
                  looking_for=looking_for_)

   dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=False, no_plot=False)
   dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=False, no_plot=True)
   dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=True, no_plot=True)
   #Making calculations or/and plots for your data. (available methods: qn_weight, distance_weight, average)

   # qn_weight: will use the quality of data (qn) as weight.
   # distance_weight: will use the distance as weight.
   # compare: will compare your calculation with the station you choosed.
   # If qn_weight == False, distance_weight == False, it will use standard-average calc. method.
   # If you want just to see the numbers of your calculation, you can set no_plot == True (will be faster).

.. note::
   If you are comparing your calculations, make sure, that the x_coordinate and y_coordinate are exactly the same as for the station you are comparing with.

.. image:: _image/wind_FF_10_no_compare.png
  :width: 1000
  :alt: test

.. image:: _image/dwd_copy.png
   :width: 300

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

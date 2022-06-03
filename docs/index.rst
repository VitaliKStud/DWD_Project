.. DWD Project documentation master file, created by
   sphinx-quickstart on Tue May 31 20:43:50 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DWD Project’s documentation!
=======================================

.. toctree::
   :caption: Contents:

   modules

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
   for windows user

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
*****************************************

.. code-block:: python

   #


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

DwdDataScrapper module
======================

.. automodule:: DwdDataScrapper
   :members:
   :undoc-members:
   :show-inheritance:


getting started: download all (air_temperatur, solar, wind, precipitation)
**************************************************************************

.. code-block:: python


   from DwdMain import main_dwd
   main_dwd(local_domain="YOUR_PATH/").main_datascrapper(all=True)
   # Will download and unzip all the data for air_temperatur, solar, wind, precipitation (historical, meta_data, now and recent) to YOUR_PATH/.
   main_dwd(local_domain="YOUR_PATH/").main_writer(all=True)
   # Will create some .json files inside .../extracted_files/ for faster loading times. This step is important. Inside this .json files will dates and paths for every station.

import os
from DwdMain import DwdMain, main_dwd
from DwdDataPrep import Reader
from DwdGui import DwdGui
import zipfile

local_domain_ = r"C:/Users/VID/Desktop/Betriebliche_Praxis/"
os.chdir(local_domain_)

looking_for_ = ["TM5_10"]
# choose your data you need to plot #Check DwdDict

compare_station_ = "TU_00044"
# for data to compare

start_date_ = 201201010000
end_date_ = 201301010000
# yyyymmddhhmm

x_coordinate_ = 7.2162
y_coordinate_ = 51.4818
# y_coordinate_ = 52.9336
# x_coordinate_ = 8.2370
z_coordinate_ = 0
# geoLaenge, geoBreite, height

k_factor_ = 5
# How many Stations you're looking for around your x_coordinate and y_coordinate

type_of_data_ = "precipitation"
type_of_time_ = "historical"
# what type do you have? Check type_of_data_list_ and type_of_time_list_

#for i in type_of_data_list_:

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

# dwd.main_plotter_data(compare=False)
# dwd.main_station_array():
# dwd.main_station_information("TU_00003")["geoBreite"]
dwd.main_datascrapper()
# dwd.main_writer([type_of_data_])
# dwd.main_data_map()
# dwd.main_plotter_stations(projection=False)




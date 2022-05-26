import os
from DwdMain import DwdMain, main_dwd
from DwdDataPrep import Reader
from DwdGui import DwdGui
import zipfile

local_domain_ = r"C:/Users/VID/Desktop/Betriebliche_Praxis/"
os.chdir(local_domain_)

looking_for_ = ["TT_10"]
# choose your data you need to plot #Check DwdDict

#compare_station_ = "TU_00003"
# for data to compare

start_date_ = 200001010000
end_date_ = 200002010000
# yyyymmddhhmm

x_coordinate_ = 7.2162
y_coordinate_ = 51.4818
z_coordinate_ = 0
# geoLaenge, geoBreite, height, geoLaenege immer kleiner (für DE)

k_factor_ = 5
# How many Stations you're looking for around your x_coordinate and y_coordinate
compare_station_ = None

type_of_data_ = "air_temperature"
type_of_time_ = "historical"
# what type do you have? Check type_of_data_list_ and type_of_time_list_

#for i in type_of_data_list_:


# a = main_dwd(local_domain=local_domain_, type_of_data=type_of_data_, type_of_time=type_of_time_, start_date=start_date_, end_date=end_date_)
# x_coordinate, y_coordinate, z_coordinate, compare_station = a.main_activ_stations_in_date()
# avg_diff_list = []
# max_diff = []
#for i in range(len(compare_station)):
# x_coordinate_ = x_coordinate[1]
# y_coordinate_ = y_coordinate[1]
# z_coordinate_ = z_coordinate[1]
# compare_station_ = compare_station[1]

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
dwd.main_plotter_data(compare="False")
# avg_diff_list.append(avg_diff)
# max_diff.append(maximum)
# print(avg_diff_list)
# print(max_diff)
# dwd.main_station_array():
# dwd.main_station_information("TU_00003")["geoBreite"]
# dwd.main_datascrapper(all=True)
# dwd.main_writer(all=True)
dwd.main_data_map()
# dwd.main_plotter_stations(projection=False)




from DwdMain import DwdMain
from DwdDict import get_dwd_dict
import os
from DwdDataPrep import Reader
from DwdGui import DwdGui

os.chdir(r"C:/Users/VID/Desktop/Betriebliche Praxis/")
local_domain_ = "C:/Users/VID/Desktop/Betriebliche Praxis/"
type_dict_, load_txt_dict_, rest_dict_, title_dict_, unit_dict_, type_of_time_list_, type_of_data_list_, external_domain_, external_path_global_, ending_ = get_dwd_dict()

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

type_of_data_ = "air_temperature"
type_of_time_ = "historical"
# what type do you have? Check type_of_data_list_ and type_of_time_list_

#for i in type_of_data_list_:
dwd = DwdMain(external_domain=external_domain_,
              external_path_global=external_path_global_,
              local_domain=local_domain_,
              type_of_data=type_of_data_,
              type_of_time=type_of_time_,
              type_dict=type_dict_,
              load_txt_dict=load_txt_dict_,
              rest_dict=rest_dict_,
              ending=ending_,
              start_date=start_date_,
              end_date=end_date_,
              compare_station=compare_station_,
              x_coordinate=x_coordinate_,
              y_coordinate=y_coordinate_,
              z_coordinate=z_coordinate_,
              k_factor=k_factor_,
              looking_for=looking_for_,
              type_of_time_list=type_of_time_list_,
              type_of_data_list=type_of_data_list_,
              unit_dict=unit_dict_,
              title_dict=title_dict_)
dwd.main_plotter_data(compare=False)




# for i in dwd.main_station_array():
#     print(dwd.main_station_information(i)["geoBreite"])

# dwd.main_datascrapper()
# dwd.main_writer()
#dwd.main_data_map()
# dwd.main_plotter_stations(projection=False)


#DwdGui.main()

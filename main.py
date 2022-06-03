import os
from DwdMain import main_dwd
from DwdDataScrapper import DataScrapper
from DwdDataPrep import Reader

local_domain_ = r"C:/Users/VID/Desktop/Betriebliche_Praxis/"
os.chdir(local_domain_)

looking_for_ = ["TT_10"]
# choose your data you need to plot #Check DwdDict

start_date_ = 199401190000
end_date_   = 199402191020
# yyyymmddhhmm

x_coordinate_ = 6.0941
y_coordinate_ = 50.7827
z_coordinate_ = 0


# geoLaenge, geoBreite, height, geoLaenege immer kleiner (für DE)

k_factor_ = 5
# How many Stations you're looking for around your x_coordinate and y_coordinate

compare_station_ = "TU_00003"
# only needed if compare="pltcompare" or compare="justcompare"

type_of_data_ = "air_temperature"
type_of_time_ = "historical"
# what type do you have? Check DwdDict type_of_data_list and type_of_time_list

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

# Download your data first
# dwd.main_datascrapper(all=True)

# Prepare some stuff first
# dwd.main_writer(type_of_data_list=["air_temperature"], type_of_time_list=["recent"], all=False)

# Get some information about any station
# print(main_dwd(local_domain=local_domain_,type_of_data=type_of_data_, type_of_time=type_of_time_, start_date=start_date_, end_date=end_date_).main_activ_stations_in_date())
# dwd.main_station_array()

# print(dwd.main_activ_stations_in_date())

# Plot your data
# dwd.main_plotter_data(qn_weight=True, distance_weight=False, compare=True, no_plot=False)
dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=True, no_plot=False)
# dwd.main_plotter_data(qn_weight=False, distance_weight=False, compare=True, no_plot=False)
# main_dwd(local_domain=local_domain_, type_of_data=type_of_data_, type_of_time=type_of_time_,).main_plotter_stations(projection=False)


main_dwd(local_domain=local_domain_,
         type_of_data=type_of_data_,
         type_of_time=type_of_time_,
         start_date=start_date_,
         end_date=end_date_,
         x_coordinate=x_coordinate_,
         y_coordinate=y_coordinate_,
         z_coordinate=z_coordinate_,
         k_factor=k_factor_).main_data_map()

# Generate some data for DwdMapCreator
# dwd.main_data_map()


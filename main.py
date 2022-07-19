import os
# from DwdMain import main_dwd
# import json
# import numpy as np
# from DwdDataScrapper import DataScrapper
# from DwdDataPrep import Reader
#
#test
#
# looking_for_ = ["FF_10"]
# # choose your data you need to plot #Check DwdDict
#
# start_date_ = 199401190000
# end_date_   = 199402191020
# # yyyymmddhhmm
#
# x_coordinate_ = 6.0941
# y_coordinate_ = 50.7827
# z_coordinate_ = 0
#
#
# # geoLaenge, geoBreite, height, geoLaenege immer kleiner (für DE)
#
# k_factor_ = 7
# # How many Stations you're looking for around your x_coordinate and y_coordinate
#
# compare_station_ = "wind_00003"
# # only needed if compare="pltcompare" or compare="justcompare"
#
# type_of_data_ = "wind"
# type_of_time_ = "historical"
# # what type do you have? Check DwdDict type_of_data_list and type_of_time_list
#
# dwd = main_dwd(local_domain=local_domain_,
#                type_of_data=type_of_data_,
#                type_of_time=type_of_time_,
#                start_date=start_date_,
#                end_date=end_date_,
#                compare_station=compare_station_,
#                x_coordinate=x_coordinate_,
#                y_coordinate=y_coordinate_,
#                z_coordinate=z_coordinate_,
#                k_factor=k_factor_,
#                looking_for=looking_for_)
#
# dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=True, no_plot=True)

# x, y, z, id = main_dwd(local_domain=local_domain_,
#                type_of_data=type_of_data_,
#                type_of_time=type_of_time_,
#                start_date=start_date_, end_date=end_date_).main_activ_stations_in_date()


# avg_list = []
# maximum_list = []
# for i in range(len(x)):
#     dwd = main_dwd(local_domain=local_domain_,
#                    type_of_data=type_of_data_,
#                    type_of_time=type_of_time_,
#                    start_date=start_date_,
#                    end_date=end_date_,
#                    compare_station=id[i],
#                    x_coordinate=x[i],
#                    y_coordinate=y[i],
#                    z_coordinate=z[i],
#                    k_factor=5,
#                    looking_for=looking_for_)
#     my_array = dwd.main_plotter_data(qn_weight=False, distance_weight=False, compare=True, no_plot=True)
#     print(my_array)
#     avg_list.append(my_array)
#     print(avg_list)
#     with open(r"C:/Users/VID/Desktop/Betriebliche_Praxis/DWD_Project/avg_max.json", "w") as f:
#         json.dump(avg_list, f, indent=2)
#
# avg_list = []
# maximum_list = []
# for i in range(len(x)):
#     dwd = main_dwd(local_domain=local_domain_,
#                    type_of_data=type_of_data_,
#                    type_of_time=type_of_time_,
#                    start_date=start_date_,
#                    end_date=end_date_,
#                    compare_station=id[i],
#                    x_coordinate=x[i],
#                    y_coordinate=y[i],
#                    z_coordinate=z[i],
#                    k_factor=20,
#                    looking_for=looking_for_)
#     my_array = dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=True, no_plot=True)
#     print(my_array)
#     avg_list.append(my_array)
#     print(avg_list)
#     with open(r"C:/Users/VID/Desktop/Betriebliche_Praxis/DWD_Project/avg_max_distance.json", "w") as f:
#         json.dump(avg_list, f, indent=2)

# with open(r"C:/Users/VID/Desktop/Betriebliche_Praxis/DWD_Project/avg_max.json", "r") as f:
#     data_durchschnitt = json.load(f)
#
# with open(r"C:/Users/VID/Desktop/Betriebliche_Praxis/DWD_Project/avg_max_distance.json", "r") as f:
#     data_weighted = json.load(f)
#
# max_list = np.array([])
# avg_list = np.array([])
# for i in range(len(data_durchschnitt)):
#     max_list = np.append(max_list, [data_durchschnitt[i][0]])
#     avg_list = np.append(avg_list, [data_durchschnitt[i][1]])
# print(np.nansum(max_list)/(len(max_list)-np.isnan(max_list).sum()))
# print(np.nansum(avg_list)/(len(avg_list)-np.isnan(avg_list).sum()))
# print(np.isnan(max_list).sum())
#
# max_list_2 = np.array([])
# avg_list_2 = np.array([])
# for i in range(len(data_weighted)):
#     max_list_2 = np.append(max_list_2, [data_weighted[i][0]])
#     avg_list_2 = np.append(avg_list_2, [data_weighted[i][1]])
# print(np.nansum(max_list_2/(len(max_list_2)-np.isnan(max_list_2).sum())))
# print(np.nansum(avg_list_2)/(len(avg_list_2)-np.isnan(avg_list_2).sum()))




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

# dwd.main_plotter_data(qn_weight=False, distance_weight=False, compare=True, no_plot=False)
# main_dwd(local_domain=local_domain_, type_of_data=type_of_data_, type_of_time=type_of_time_,).main_plotter_stations(projection=False)


# main_dwd(local_domain=local_domain_,
#          type_of_data=type_of_data_,
#          type_of_time=type_of_time_,
#          start_date=start_date_,
#          end_date=end_date_,
#          x_coordinate=x_coordinate_,
#          y_coordinate=y_coordinate_,
#          z_coordinate=z_coordinate_,
#          k_factor=k_factor_).main_data_map()

# Generate some data for DwdMapCreator
# dwd.main_data_map()

from DwdMain import main_dwd
main_dwd(local_domain=local_domain_).main_datascrapper(all=True)
# Will download and unzip all the data for air_temperatur, solar, wind, precipitation (historical, meta_data, now and recent) to YOUR_PATH/.
main_dwd(local_domain=local_domain_).main_writer(all=True)
# Will create some .json files inside .../extracted_files/ for faster loading times. This step is important. Inside this .json files will dates and paths for every station.

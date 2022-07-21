import os
from DwdMain import main_dwd
from DwdDict import get_dwd_dict
import json
import csv

local_domain_ = r"C:\Users\VID\Desktop\Betriebliche_Praxis/"
os.chdir(local_domain_)
print(os.getcwd())

type_dict, load_txt_dict, rest_dict, title_dict, unit_dict, type_of_time_list, type_of_data_list, external_domain, external_path_global, ending = get_dwd_dict()

print(type_of_data_list)
print(unit_dict)

# for i in type_of_time_list:
#     for j in type_of_data_list:
#         main_dwd(local_domain=local_domain_, type_of_data=j, type_of_time=i,).main_plotter_stations(projection=True)

data = []
for i in type_of_data_list:
    keys = unit_dict[i].keys()
    start_date_ = 199001010000
    end_date_ = 199001010000
    x = main_dwd(local_domain=local_domain_,
                 type_of_data=i,
                 type_of_time="historical",
                 start_date=start_date_, end_date=end_date_).main_activ_stations_in_date()
    for j in keys:
        my_list = []
        for z in range(4, 50, 1):
            print(j)
            looking_for_ = [j]
            start_date_ = 199001010000
            end_date_   = 199001020000
            x_coordinate_ = x[0][0] # 7 for compare == False
            y_coordinate_ = x[1][0] # 51 for compare == False
            z_coordinate_ = 0 # not needed for now (maybe in future)
            print(z)
            k_factor_ = z # how many station are you looking for around your location? 7 means, it will find 7 next stations for your location
            compare_station_ = x[3][0] # needed for comparing (don't forget to set the prefix (wind_)
            type_of_data_ = i
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
            dwd_list = dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=True, no_plot=True)
            maximum, avg_diff, rmse, data_density = dwd_list[0], dwd_list[1], dwd_list[2], dwd_list[3]
            my_list.append([j, z, start_date_, end_date_, avg_diff, maximum, rmse, data_density])
            print(my_list)
    data.extend(my_list)
    print(data)

header = ["paramter", "k-faktor", "von_datum", "bis_datum", "avg_diff", "max_diff", "rmse"]
with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/ergebnisse_gewichtet.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)

# print(my_list_outside)
import os
from DwdMain import main_dwd
from DwdDict import get_dwd_dict
import json
import csv
from random import seed
from random import randint

local_domain_ = r"C:\Users\VID\Desktop\Betriebliche_Praxis/"
os.chdir(local_domain_)

type_dict, load_txt_dict, rest_dict, title_dict, unit_dict, type_of_time_list, type_of_data_list, external_domain, external_path_global, ending = get_dwd_dict()


# for i in type_of_time_list:
#     for j in type_of_data_list:
#         main_dwd(local_domain=local_domain_, type_of_data=j, type_of_time=i,).main_plotter_stations(projection=True)

data = []

def month_step():
    month_list = []
    for y in range (0,1,1):
        for m in range(1,13,1):
            start_date_ = int(str(1991+y)+str(f"{m:02d}")+str(0)+str(1))*10000
            if m == 12:
                end_date_ = int(str(1991 + y+1) + str(f"{1:02d}") + str(0) + str(1)) * 10000
            else:
                end_date_ = int(str(1991+y)+str(f"{m+1:02d}")+str(0)+str(1))*10000
            month_list.append([start_date_,end_date_])
    return month_list





for i in type_of_data_list:
    keys = unit_dict[i].keys()
    for date in range(0,len(month_step())):
        start_date_ = month_step()[date][0]
        end_date_ = month_step()[date][1]
        x = main_dwd(local_domain=local_domain_,
                     type_of_data=i,
                     type_of_time="historical",
                     start_date=start_date_, end_date=end_date_).main_activ_stations_in_date()
        for j in keys:
            my_list = []
            if len(x) < 50:
                for z in range(3, len(x[0])-2, 1):
                    print(j)
                    seed(z)
                    random = randint(0, len(x[0])-1)
                    looking_for_ = [j]
                    start_date_ = month_step()[date][0]
                    end_date_ = month_step()[date][1]
                    x_coordinate_ = x[0][random] # 7 for compare == False
                    y_coordinate_ = x[1][random] # 51 for compare == False
                    z_coordinate_ = 0 # not needed for now (maybe in future)
                    print(z)
                    k_factor_ = z # how many station are you looking for around your location? 7 means, it will find 7 next stations for your location
                    compare_station_ = x[3][random] # needed for comparing (don't forget to set the prefix (wind_)
                    print(compare_station_)
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
                    my_list.append([compare_station_, j, z, start_date_, end_date_, avg_diff, maximum, rmse, data_density])
                    #header = ["paramter", "k-faktor", "von_datum", "bis_datum", "avg_diff", "max_diff", "rmse", "data_density"]
                    print(my_list)
                with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/ergebnisse_gewichtet_"+ j + ".csv", "a+", newline="") as file:
                    writer = csv.writer(file)
                    #writer.writerow(header)
                    writer.writerows(my_list)
            else:
                for z in range(3, 51, 1):
                    print(j)
                    seed(z)
                    random = randint(0, len(x[0]) - 1)
                    looking_for_ = [j]
                    start_date_ = month_step()[date][0]
                    end_date_ = month_step()[date][1]
                    x_coordinate_ = x[0][random]  # 7 for compare == False
                    y_coordinate_ = x[1][random]  # 51 for compare == False
                    z_coordinate_ = 0  # not needed for now (maybe in future)
                    print(z)
                    k_factor_ = z  # how many station are you looking for around your location? 7 means, it will find 7 next stations for your location
                    compare_station_ = x[3][random]  # needed for comparing (don't forget to set the prefix (wind_)
                    print(compare_station_)
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
                    my_list.append([compare_station_, j, z, start_date_, end_date_, avg_diff, maximum, rmse, data_density])
                    # header = ["paramter", "k-faktor", "von_datum", "bis_datum", "avg_diff", "max_diff", "rmse", "data_density"]
                    print(my_list)
                with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/ergebnisse_gewichtet_" + j + ".csv", "a+", newline="") as file:
                    writer = csv.writer(file)
                    # writer.writerow(header)
                    writer.writerows(my_list)


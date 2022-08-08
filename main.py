import os
from DwdMain import main_dwd
from DwdDict import get_dwd_dict
import json
import csv
from random import seed
from random import randint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

local_domain_ = r"C:\Users\VID\Desktop\Betriebliche_Praxis/"
os.chdir(local_domain_)

type_dict, load_txt_dict, rest_dict, title_dict, unit_dict, type_of_time_list, type_of_data_list, external_domain, external_path_global, ending = get_dwd_dict()

# looking_for_ = ["PP_10"]
# start_date_ = 199908010000
# end_date_   = 199909010000
# x_coordinate_ = 7.1077 # 7 for compare == False
# y_coordinate_ = 49.2128 # 51 for compare == False
# z_coordinate_ = 0 # not needed for now (maybe in future)
# k_factor_ = 20 # how many station are you looking for around your location? 7 means, it will find 7 next stations for your location
# compare_station_ = "TU_04336" # needed for comparing (don't forget to set the prefix (wind_)
# type_of_data_ = "air_temperature"
# type_of_time_ = "historical"
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

# for i in type_of_time_list:
#     for j in type_of_data_list:
#         main_dwd(local_domain=local_domain_, type_of_data=j, type_of_time=i,).main_plotter_stations(projection=True)

data = []

def month_step():
    month_list = []
    for y in range (0,31,1):
        for m in range(1,13,1):
            start_date_ = int(str(2001+y)+str(f"{m:02d}")+str(0)+str(1))*10000
            if m == 12:
                end_date_ = int(str(2001 + y+1) + str(f"{1:02d}") + str(0) + str(1)) * 10000
            else:
                end_date_ = int(str(2001+y)+str(f"{m+1:02d}")+str(0)+str(1))*10000
            month_list.append([start_date_,end_date_])
    return month_list

def calculations():
    for i in type_of_data_list:
        try:
            keys = unit_dict[i].keys()
            for date in range(0,len(month_step())):
                try:
                    start_date_ = month_step()[date][0]
                    end_date_ = month_step()[date][1]
                    x = main_dwd(local_domain=local_domain_,
                                 type_of_data=i,
                                 type_of_time="historical",
                                 start_date=start_date_, end_date=end_date_).main_activ_stations_in_date()
                    for j in keys:
                        try:
                            my_list = []
                            if len(x[0]) < 20:
                                for z in range(3, len(x[0])-2, 1):
                                    try:
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
                                        dwd_list = dwd.main_plotter_data(qn_weight=False, distance_weight=False, compare=True, no_plot=True)
                                        maximum, avg_diff, rmse, data_density = dwd_list[0], dwd_list[1], dwd_list[2], dwd_list[3]
                                        my_list.append([compare_station_, x_coordinate_, y_coordinate_, j, type_of_data_, z, start_date_, end_date_, avg_diff, maximum, rmse, data_density])
                                        #header = ["paramter", "k-faktor", "von_datum", "bis_datum", "avg_diff", "max_diff", "rmse", "data_density"]
                                        print(my_list)
                                    except:
                                        print("error1")
                                        pass
                                    with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/ergebnisse_gewichtet_" + j + "standard" +".csv") as file:
                                        writer = csv.writer(file)
                                        #writer.writerow(header)
                                        writer.writerows(my_list)

                            else:
                                for z in range(3, 21, 1):
                                    try:
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
                                        dwd_list = dwd.main_plotter_data(qn_weight=False, distance_weight=False, compare=True, no_plot=True)
                                        maximum, avg_diff, rmse, data_density = dwd_list[0], dwd_list[1], dwd_list[2], dwd_list[3]
                                        my_list.append([compare_station_, x_coordinate_, y_coordinate_, j, type_of_data_, z, start_date_, end_date_, avg_diff, maximum, rmse, data_density])
                                        # header = [0compare_station_, 1x_coordinate_, 2y_coordinate_, 3j, 4type_of_data_, 5z, 6start_date_, 7end_date_, 8avg_diff, 9maximum, 10rmse, 11data_density]
                                        print(my_list)
                                    except:
                                        print("error2")
                                        pass
                                    with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/ergebnisse_gewichtet_" + j + "_standard" +".csv", "a+", newline="") as file:
                                        writer = csv.writer(file)
                                        # writer.writerow(header)
                                        writer.writerows(my_list)
                        except:
                            print("error3")
                            pass
                except:
                    print("error4")
                    pass
        except:
            print("error5")
            pass


# looking_for_ = ["PP_10"]
# start_date_ = 200001010000
# end_date_   = 200001010020
# x_coordinate_ = 9.7377 # 7 for compare == False
# y_coordinate_ = 50.852 # 51 for compare == False
# z_coordinate_ = 0 # not needed for now (maybe in future)
# k_factor_ = 3 # how many station are you looking for around your location? 7 means, it will find 7 next stations for your location
# compare_station_ = "TU_02171" # needed for comparing (don't forget to set the prefix (wind_)
# type_of_data_ = "air_temperature"
# type_of_time_ = "historical"
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
# dwd.main_plotter_data(qn_weight=False, distance_weight=False, compare=True, no_plot=True)

# for i in type_of_data_list:
#     keys = unit_dict[i].keys()
#     for j in keys:
#         my_list = []
#         with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/ergebnisse_gewichtet_" + j + ".csv") as file:
#             counter = 0
#             for i in file:
#                 if [i] in my_list:
#                     counter = counter + 1
#                 else:
#                     my_list.append([i])
#
#         print(counter)
#         with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/ergebnisse_gewichtet_" + j + "_" + ".csv", "a+", newline="") as file:
#             writer = csv.writer(file)
#             # writer.writerow(header)
#             writer.writerows(my_list)


def std_from_list (my_list):
    avg = sum(my_list)/len(my_list)
    a = 0
    for i in my_list:
        a = a + (i - avg)**2
    std = np.sqrt(a/len(my_list))
    return 2*std

def check(num):
    if num % 2 == 0:
        return True
    else:
        return False
#
#

def analyze():
    counter = 0
    counter_2 = 0
    counter_3 = 0
    fig, ax = plt.subplots(5,2, figsize=(10, 20))
    for i in type_of_data_list:
        keys = unit_dict[i].keys()
        for j in keys:
            if j == "RWS_DAU_10" or j == "DS_10" or j == "GS_10":
                pass
            else:
                my_list = []
                with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/weighted/ergebnisse_gewichtet_" + j + "_" + ".csv") as file:
                    for i in file:
                        if len(i.strip("\n").split(",")) == 1:
                            pass
                        else:
                            my_list.append(i.strip("\n").split(","))
                avg = []
                std_list = []
                for k in range(3,21,1):
                        n = 10
                        y = []
                        try:
                            for i in my_list:
                                if int(i[5]) == k:
                                    if float(i[11]) > 0.1:
                                        if i[n] == "nan":
                                            pass
                                        else:
                                            y.append(float(i[n]))
                            print(len(y))
                            print(j)
                            avg.append(sum(y)/len(y))
                            std_list.append(std_from_list(y))
                        except:
                            pass
                if counter == 0:
                    pass
                else:
                    if check(counter):
                        counter_2 = 0
                        counter_3 = counter_3 + 1
                    else:
                        counter_2 = 1
                counter = counter + 1
                ax[counter_3,counter_2].bar(np.arange(3, len(avg) + 3), avg, yerr=std_list, capsize=4)
                # plt.grid()
                # plt.ylim(0,max(avg)+max(std))
                ax[counter_3,counter_2].set_title(j)
                ax[counter_3,counter_2].set_ylim(0,max(avg)+max(std_list)*1.1)
                fig.savefig("Graphs/german_stations_2d_weighted" + ".png")
                plt.close("all")


def write_csv():
    for i in type_of_data_list:
        keys = unit_dict[i].keys()
        for j in keys:
            my_list = []
            with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/ergebnisse_gewichtet_" + j + "_standard" ".csv") as file:
                counter = 0
                for i in file:
                    if [i] in my_list:
                        counter = counter + 1
                    else:
                        my_list.append([i])

            print(counter)
            with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/ergebnisse_gewichtet_" + j + "_standard_" + ".csv", "a+", newline="") as file:
                writer = csv.writer(file)
                # writer.writerow(header)
                writer.writerows(my_list)


analyze()
# write_csv()
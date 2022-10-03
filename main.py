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
import seaborn as sns
from matplotlib.patches import Rectangle
np.set_printoptions(precision=3, suppress=True)
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


local_domain_ = r"C:\Users\VID\Desktop\Betriebliche_Praxis/"
os.chdir(local_domain_)

type_dict, load_txt_dict, rest_dict, title_dict, unit_dict, type_of_time_list, type_of_data_list, external_domain, external_path_global, ending = get_dwd_dict()

looking_for_ = ["TT_10"]
start_date_ = 199908010000
end_date_   = 199909010000
x_coordinate_ = 7.1077 # 7 for compare == False
y_coordinate_ = 49.2128 # 51 for compare == False
z_coordinate_ = 0 # not needed for now (maybe in future)
k_factor_ = 7 # how many station are you looking for around your location? 7 means, it will find 7 next stations for your location
compare_station_ = "TU_04336" # needed for comparing (don't forget to set the prefix (wind_)
type_of_data_ = "air_temperature"
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

dwd.main_plotter_data(qn_weight=False, distance_weight=True, compare=True, no_plot=True)



# main_dwd(local_domain=local_domain_, type_of_data="wind", type_of_time="historical").main_plotter_stations(projection=False)

def month_step():
    month_list = []
    for y in range (0,21,1):
        for m in range(1,13,1):
            start_date_ = int(str(2000+y)+str(f"{m:02d}")+str(0)+str(1))*10000
            if m == 12:
                end_date_ = int(str(2000 + y+1) + str(f"{1:02d}") + str(0) + str(1)) * 10000
            else:
                end_date_ = int(str(2000+y)+str(f"{m+1:02d}")+str(0)+str(1))*10000
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
                                        dwd_list = dwd.main_plotter_data(qn_weight=False, distance_weight=False, direction=True, compare=True, no_plot=True)
                                        maximum, avg_diff, rmse, data_density = dwd_list[0], dwd_list[1], dwd_list[2], dwd_list[3]
                                        my_list.append([compare_station_, x_coordinate_, y_coordinate_, j, type_of_data_, z, start_date_, end_date_, avg_diff, maximum, rmse, data_density])
                                        #header = ["paramter", "k-faktor", "von_datum", "bis_datum", "avg_diff", "max_diff", "rmse", "data_density"]
                                        print(my_list)
                                    except:
                                        print("error1")
                                        pass
                                    with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/avg_" + j + "_direction" +".csv") as file:
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
                                        dwd_list = dwd.main_plotter_data(qn_weight=False, distance_weight=False, direction=True, compare=True, no_plot=True)
                                        maximum, avg_diff, rmse, data_density = dwd_list[0], dwd_list[1], dwd_list[2], dwd_list[3]
                                        my_list.append([compare_station_, x_coordinate_, y_coordinate_, j, type_of_data_, z, start_date_, end_date_, avg_diff, maximum, rmse, data_density])
                                        # header = [0compare_station_, 1x_coordinate_, 2y_coordinate_, 3j, 4type_of_data_, 5z, 6start_date_, 7end_date_, 8avg_diff, 9maximum, 10rmse, 11data_density]
                                        print(my_list)
                                    except:
                                        print("error2")
                                        pass
                                    with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/avg_" + j + "_direction" +".csv", "a+", newline="") as file:
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


# looking_for_ = ["TT_10"]
# start_date_ = 200001010000
# end_date_   = 200002010020
# x_coordinate_ = 10.3771 # 7 for compare == False
# y_coordinate_ = 50.5611 # 51 for compare == False
# z_coordinate_ = 0 # not needed for now (maybe in future)
# k_factor_ = 6 # how many station are you looking for around your location? 7 means, it will find 7 next stations for your location
# compare_station_ = "TU_03231" # needed for comparing (don't forget to set the prefix (wind_)
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
# dwd.main_plotter_data(qn_weight=False, distance_weight=False, direction=True, compare=True, no_plot=False)
# dwd.main_data_map(direction=True)

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

def check(num,n=2):
    if num % n == 0:
        return True
    else:
        return False
#
#

def analyze(method="standard", density=0.9):
    dict_avg = {}
    dict_std = {}
    dict_density = {}
    dict_datapoints = {}
    for i in type_of_data_list:
        keys = unit_dict[i].keys()
        for j in keys:
            if j == "RWS_DAU_10":
                pass
            else:
                my_list = []
                if method == "standard":
                    path = r"C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/standard/ergebnisse_gewichtet_" + j + "_standard_" + ".csv"
                elif method == "weighted":
                    path = r"C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/weighted/ergebnisse_gewichtet_" + j + "_" + ".csv"
                elif method == "direction":
                    path = r"C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/direction/avg_" + j + "_direction_" + ".csv"
                with open(path) as file:
                    for i in file:
                        if len(i.strip("\n").split(",")) == 1:
                            pass
                        else:
                            my_list.append(i.strip("\n").split(","))
                density_list = []
                avg = []
                std_list = []
                count_datapoints = []
                count_data_list = []
                for k in range(3,21,1):
                        count_data = 0
                        n = 10
                        y = []
                        den_list = []
                        try:
                            for i in my_list:
                                if int(i[5]) == k:
                                    if int(i[7]) > 200000000000:
                                        if float(i[11]) > density:
                                            if i[n] == "nan":
                                                pass
                                            else:
                                                y.append(float(i[n]))
                                                count_data = count_data + 1
                                                den_list.append(float(i[11]))
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    pass
                            count_data_list.append(count_data)
                            avg.append(sum(y)/len(y))
                            density_list.append(sum(den_list)/len(den_list))
                            std_list.append(std_from_list(y))
                        except:
                            pass

                dict_avg.update({j: avg})
                dict_std.update({j: std_list})
                dict_density.update({j: density_list})
                dict_datapoints.update({j: sum(count_data_list)/len(count_data_list)})
    return dict_avg, dict_std, dict_density, dict_datapoints

def write_csv():
    for i in type_of_data_list:
        keys = unit_dict[i].keys()
        for j in keys:
            my_list = []
            with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/direction_roh/avg_" + j + "_direction" ".csv") as file:
                counter = 0
                for i in file:
                    if [i] in my_list:
                        counter = counter + 1
                    else:
                        my_list.append([i])

            print(counter)
            with open("C:/Users/VID/Desktop/Betriebliche_Praxis/Ergebnisse/direction/avg_" + j + "_direction_" + ".csv", "a+", newline="") as file:
                writer = csv.writer(file)
                # writer.writerow(header)
                writer.writerows(my_list)



def plot_compare_method_bar(dict_avg, dict_std, dict_names, name="test", std=True, plt_name="test"):
    keys = dict_avg.keys()
    counter_0 = 0
    counter_1 = 0
    counter_2 = 0
    fig, ax = plt.subplots(3, 4, figsize=(30, 10))
    for i in keys:
        if counter_0 == 0:
            pass
        else:
            if check(counter_0,4):
                counter_1 = counter_1 + 1
                counter_2 = 0
            else:
                counter_2 = counter_2 + 1
        counter_0 = counter_0 + 1
        avg = dict_avg[i]
        counter_for_number = 0
        for r in avg:
            if r == min(avg):
                my_index = counter_for_number
            else:
                pass
            counter_for_number += 1
        print(avg)
        print(min(avg))
        std_list = dict_std[i]
        print(std_list[my_index])
        if len(avg) == 0:
            pass
        else:
            if std:
                bar = ax[counter_1, counter_2].bar(np.arange(3, len(avg) + 3), avg)
                bar_error = ax[counter_1, counter_2].errorbar(np.arange(3, len(avg) + 3), avg, yerr=std_list, capsize=4, fmt="o", color="grey", ms=4.0)
                counter_for_min = 0
                for j in range(0,len(bar),1):
                    if dict_names[i][j] == "a":
                        bar[j].set_color("red")
                        bar[j].set_label("test")
                        if counter_for_min == my_index:
                            bar[j].set_edgecolor("black")
                            bar[j].set_linewidth(2)
                        counter_for_min += 1
                    elif dict_names[i][j] == "b":
                        bar[j].set_color("orange")
                        bar[j].set_label("test1")
                        if counter_for_min == my_index:
                            bar[j].set_edgecolor("black")
                            bar[j].set_linewidth(2)
                        counter_for_min += 1
                    elif dict_names[i][j] == "c":
                        bar[j].set_color("green")
                        bar[j].set_label("test2")
                        if counter_for_min == my_index:
                            bar[j].set_edgecolor("black")
                            bar[j].set_linewidth(2)
                        counter_for_min += 1
            else:
                bar = ax[counter_1, counter_2].bar(np.arange(3, len(avg) + 3), avg)
            ax[counter_1, counter_2].set_title(i)
            ax[counter_1, counter_2].grid()
            colors = {'Modell 1: Durchschnitt': 'red', 'Modell 3: Gewichtete Distanz': 'orange', "Modell 2: Himmelsrichtungen": "green"}
            labels = list(colors.keys())
            handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
            plt.legend(handles, labels, loc="best", bbox_to_anchor=(1.0, 0.5))
            ax[counter_1, counter_2].set_ylim(0, max(avg) + max(std_list) * 1.1)
            ax[counter_1, counter_2].set_xticks(np.arange(3, 21, 2))
            fig.savefig(r"C:\Users\VID\Desktop\Betriebliche_Praxis\Graphs/" + plt_name + ".png")
            plt.close("all")

def compare_methods(dict_1, dict_2, dict_3, dict_std_1, dict_std_2, dict_std_3):
    keys = dict_1.keys()
    dict_erg = {}
    dict_std = {}
    dict_erg_g = {}
    dict_std_g = {}
    dict_names = {}
    for i in keys:
        array_1 = np.array(dict_1[i]) #standard
        array_2 = np.array(dict_2[i]) #weighted
        array_3 = np.array(dict_3[i]) #direction
        array_4 = np.array(dict_std_1[i])
        array_5 = np.array(dict_std_2[i])
        array_6 = np.array(dict_std_3[i])
        a = array_1
        b = array_2
        c = array_3
        d = array_4
        e = array_5
        f = array_6
        list_erg = []
        list_erg_names = []
        list_std = []
        if len(a) == len(b) == len(c):
            for j in range(0,len(a),1):
                if abs(a[j]) < abs(b[j]) and abs(a[j]) < abs(c[j]):
                    list_erg_names.append("a")
                    list_erg.append(a[j])
                    list_std.append(d[j])
                elif abs(b[j]) < abs(a[j]) and abs(b[j]) < abs(c[j]):
                    list_erg_names.append("b")
                    list_erg.append(b[j])
                    list_std.append(e[j])
                elif abs(c[j]) < abs(a[j]) and abs(c[j]) < abs(b[j]):
                    list_erg_names.append("c")
                    list_erg.append(c[j])
                    list_std.append(f[j])
            dict_erg.update({i:list_erg})
            dict_std.update({i:list_std})
            dict_names.update({i:list_erg_names})
            dict_erg_g.update(dict_erg)
            dict_std_g.update(dict_std)
        else:
            pass
    return dict_erg_g, dict_names, dict_std_g

# write_csv()

def analyze_density(dict_density, dict_datapoints):
    keys = dict_density.keys()
    dict_avg_density = {}
    for i in keys:
        a = dict_density[i]
        dict_avg_density.update({i:sum(a)/len(a)})
    return dict_avg_density, dict_datapoints

def plot_density(dict_avg_density, dict_datapoints, density_list, plt_name):
    keys = dict_avg_density[0].keys()
    my_name = []
    my_avg_density = []
    my_data_points = []
    my_density_list = []
    for i in range(0,len(dict_avg_density),1):
        for j in keys:
            my_name.append(j)
            my_avg_density.append(dict_avg_density[i][j])
            my_data_points.append((dict_datapoints[i][j]))
            my_density_list.append((density_list[i]))
    df = pd.DataFrame(list(zip(my_name, my_data_points, my_avg_density, my_density_list)))
    df = df.rename(columns={0:"Parameter",1:"data_points",2:"density", 3:"Gesetzte Grenze für die Dichte"})
    print(df)
    heatmap1_data = pd.pivot_table(df, values='density',
                                   index=['Parameter'],
                                   columns='Gesetzte Grenze für die Dichte')
    print(heatmap1_data)
    fig = plt.figure(figsize=(10, 5))
    sns.heatmap(heatmap1_data, cmap="YlGnBu", cbar_kws={'label': 'Erreichte Datendichte'})
    fig.savefig(r"C:\Users\VID\Desktop\Betriebliche_Praxis\Graphs/" + plt_name + ".png")


def my_main():
    density_1_list = []
    den_1_list = []
    data_p_1_list = []
    density_2_list = []
    den_2_list = []
    data_p_2_list = []
    density_3_list = []
    den_3_list = []
    data_p_3_list = []
    for i in range(0,100,10):
        d = i/100
        print(d)
        dict_avg_1, dict_std_1, dict_density_1, dict_datapoints_1 = analyze(method="standard", density=d)
        dict_avg_2, dict_std_2, dict_density_2, dict_datapoints_2 = analyze(method="weighted", density=d)
        dict_avg_3, dict_std_3, dict_density_3, dict_datapoints_3 = analyze(method="direction", density=d)
        dict_erg_g, dict_names, dict_std_g = compare_methods(dict_avg_1, dict_avg_2, dict_avg_3, dict_std_1, dict_std_2, dict_std_3)
        plot_compare_method_bar(dict_erg_g, dict_std_g, dict_names, name="_test", std=True, plt_name="test_"+str(d))
        den_1, data_p_1 = analyze_density(dict_density_1, dict_datapoints_1)
        den_2, data_p_2 = analyze_density(dict_density_2, dict_datapoints_2)
        den_3, data_p_3 = analyze_density(dict_density_3, dict_datapoints_3)
        den_1_list.append(den_1)
        data_p_1_list.append(data_p_1)
        density_1_list.append(d)
        den_2_list.append(den_2)
        data_p_2_list.append(data_p_2)
        density_2_list.append(d)
        den_3_list.append(den_3)
        data_p_3_list.append(data_p_3)
        density_3_list.append(d)
    plot_density(den_1_list, data_p_1_list, density_1_list, "standard")
    plot_density(den_2_list, data_p_2_list, density_2_list, "weighted")
    plot_density(den_3_list, data_p_3_list, density_3_list, "direction")
my_main()
#hier komm
def delete_double_values(my_list):
    clean_list = []
    for i in my_list:
        if i in clean_list:
            pass
        else:
            clean_list.append(i)
    return clean_list

def correlation():
    for date in range(0, len(month_step())):
        start_date_ = month_step()[date][0]
        end_date_ = month_step()[date][1]
        stations_names_in_date = []

        for i in type_of_data_list:
            x = main_dwd(local_domain=local_domain_,
                         type_of_data=i,
                         type_of_time="historical",
                         start_date=start_date_, end_date=end_date_).main_activ_stations_in_date()

            for j in range(0, len(x[3]), 1):
                stations_names_in_date.append(x[3][j].split("_")[1])

        stations_with_all_data = []
        for n in stations_names_in_date:
            if stations_names_in_date.count(n) == 4:
                stations_with_all_data.append(n)
        stations_with_all_data = delete_double_values(stations_with_all_data)

        names_type_of_data = type_dict.keys()
        print(stations_with_all_data)

        if len(stations_with_all_data) < 20:
            for stations in stations_with_all_data:
                my_df = pd.DataFrame([])
                my_density = []
                try:
                    for names_type in names_type_of_data:
                        prefix = f"{type_dict[names_type]}_"
                        information = main_dwd(local_domain=local_domain_,
                                               type_of_data=names_type,
                                               type_of_time="historical",
                                               start_date=start_date_, end_date=end_date_).main_station_information(f"{prefix}{stations}")
                        y_coordinate_ = information["geoBreite"]
                        x_coordinate_ = information["geoLaenge"]
                        z_coordinate_ = 0  # not needed for now (maybe in future)
                        compare_station_ = stations

                        for parameter in title_dict[names_type]:
                            print(parameter)
                            looking_for_ = [parameter]
                            dwd = main_dwd(local_domain=local_domain_,
                                           type_of_data=names_type,
                                           type_of_time="historical",
                                           start_date=start_date_,
                                           end_date=end_date_,
                                           compare_station=compare_station_,
                                           x_coordinate=x_coordinate_,
                                           y_coordinate=y_coordinate_,
                                           z_coordinate=z_coordinate_,
                                           looking_for=looking_for_)
                            new_df, names, density = dwd.main_analyze_data()
                            my_df = pd.concat([my_df, new_df], axis=1)
                            my_density.append(density)
                            print(my_density)
                except:
                    print("error1")
                    pass
                plt.figure(figsize=(16, 6))
                correlation_pearson_df = my_df.corr(method="pearson")
                correlation_kendall_df = my_df.corr(method="kendall")
                correlation_spearman_df = my_df.corr(method="spearman")
                link_pearson = r"C:\Users\VID\Desktop\Betriebliche_Praxis\Ergebnisse\correlation\pearson" + "/" + str(compare_station_) + "_" + str(start_date_) + ".csv"
                link_density = r"C:\Users\VID\Desktop\Betriebliche_Praxis\Ergebnisse\correlation" + "/" + str(compare_station_) + "_" + str(start_date_) + "_density.json"
                link_kendall = r"C:\Users\VID\Desktop\Betriebliche_Praxis\Ergebnisse\correlation\kendall" + "/" + str(compare_station_) + "_" + str(start_date_) +".csv"
                link_spearman = r"C:\Users\VID\Desktop\Betriebliche_Praxis\Ergebnisse\correlation\spearman" + "/" + str(compare_station_) + "_" + str(start_date_) + ".csv"
                correlation_pearson_df.to_csv(link_pearson)
                correlation_kendall_df.to_csv(link_kendall)
                correlation_spearman_df.to_csv(link_spearman)
                with open(link_density, "w") as fp:
                    json.dump(my_density, fp)
        else:
            for stations in range(0,21,1):
                my_df = pd.DataFrame([])
                my_density = []
                random = randint(0, len(stations_with_all_data) - 1)
                try:
                    for names_type in names_type_of_data:
                        prefix = f"{type_dict[names_type]}_"
                        information = main_dwd(local_domain=local_domain_,
                                               type_of_data=names_type,
                                               type_of_time="historical",
                                               start_date=start_date_, end_date=end_date_).main_station_information(f"{prefix}{stations_with_all_data[random]}")
                        y_coordinate_ = information["geoBreite"]
                        x_coordinate_ = information["geoLaenge"]
                        z_coordinate_ = 0  # not needed for now (maybe in future)
                        compare_station_ = stations_with_all_data[random]

                        for parameter in title_dict[names_type]:
                            print(parameter)
                            looking_for_ = [parameter]
                            dwd = main_dwd(local_domain=local_domain_,
                                           type_of_data=names_type,
                                           type_of_time="historical",
                                           start_date=start_date_,
                                           end_date=end_date_,
                                           compare_station=compare_station_,
                                           x_coordinate=x_coordinate_,
                                           y_coordinate=y_coordinate_,
                                           z_coordinate=z_coordinate_,
                                           looking_for=looking_for_)
                            new_df, names, density = dwd.main_analyze_data()
                            my_df = pd.concat([my_df, new_df], axis=1)
                            my_density.append(density)
                            # print(my_density)
                except:
                    print("error1")
                    pass

                correlation_pearson_df = my_df.corr(method="pearson")
                correlation_kendall_df = my_df.corr(method="kendall")
                correlation_spearman_df = my_df.corr(method="spearman")
                link_pearson = r"C:\Users\VID\Desktop\Betriebliche_Praxis\Ergebnisse\correlation\pearson" + "/" + str(compare_station_) + "_" + str(start_date_) + ".csv"
                link_density = r"C:\Users\VID\Desktop\Betriebliche_Praxis\Ergebnisse\correlation" + "/" + str(compare_station_) + "_" + str(start_date_) + "_density.json"
                link_kendall = r"C:\Users\VID\Desktop\Betriebliche_Praxis\Ergebnisse\correlation\kendall" + "/" + str(compare_station_) + "_" + str(start_date_) +".csv"
                link_spearman = r"C:\Users\VID\Desktop\Betriebliche_Praxis\Ergebnisse\correlation\spearman" + "/" + str(compare_station_) + "_" + str(start_date_) + ".csv"
                correlation_pearson_df.to_csv(link_pearson)
                correlation_kendall_df.to_csv(link_kendall)
                correlation_spearman_df.to_csv(link_spearman)
                with open(link_density, "w") as fp:
                    json.dump(my_density, fp)


# correlation()


def dataframe_tolist(df):
    my_dflist = []
    for i in range(0, df.shape[1], 1):
        my_dflist.append(df.iloc[:, i].tolist())
    return my_dflist


def avg_of_one_element(data, zeile, spalte):
    summe = 0
    counter = 0
    for i in data:
        if np.isnan(i[zeile][spalte]):
            pass
        else:
            counter = counter + 1
            summe = summe + i[zeile][spalte]
    if counter == 0:
        avg = np.nan
    else:
        avg = summe / counter
    return avg


def avg_density(my_list):
    avg_list = []
    for i in range(0, 13, 1):
        avg = 0
        counter = 0
        for j in my_list:
            avg = avg + j[i]
            counter = counter + 1
        avg_list.append(avg / counter)
    return avg_list


def avg_all_corr(data):
    my_avg_list = []
    for zeile in range(0, 13, 1):
        my_avg_mini_list = []
        for spalte in range(0, 13, 1):
            avg = avg_of_one_element(data, zeile, spalte)
            my_avg_mini_list.append(avg)
        my_avg_list.append(my_avg_mini_list)
    return my_avg_list


def analyze_correlation():
    my_list = os.listdir(r"C:\Users\VID\Desktop\Betriebliche_Praxis\Ergebnisse\correlation\pearson")
    all_data = []
    my_density = []
    for i in my_list:
        my_file = r'C:\Users\VID\Desktop\Betriebliche_Praxis\Ergebnisse\correlation\pearson/' + str(i)
        my_density_file = r'C:\Users\VID\Desktop\Betriebliche_Praxis\Ergebnisse\correlation/' + str(i.strip(".csv")) + "_density.json"
        my_df = pd.read_csv(my_file, index_col=0)
        with open(my_density_file) as file:
            density = json.load(file)
        my_new_list = dataframe_tolist(my_df)
        all_data.append(my_new_list)
        my_density.append(density)
    return all_data, my_density


def corr_main(plt_name):
    all_data, my_density = analyze_correlation()
    den_avg = avg_density(my_density)
    my_list = avg_all_corr(all_data)
    df = pd.DataFrame(my_list)
    counter = 0
    for i in title_dict.keys():
        for j in title_dict[i]:
            df = df.rename(columns={counter: j})
            df = df.rename(index={counter: j})
            counter = counter + 1
    fig = plt.figure(figsize=(15, 12))
    mask = np.triu(np.ones_like(df, dtype=np.bool_))
    heatmap = sns.heatmap(df, mask=mask, vmin=-1, vmax=1, annot=True, cmap='coolwarm',linewidths=3.0,cbar_kws={'label': 'Korrelationskoeffizient'}, annot_kws={"fontsize":13})
    heatmap.xaxis.set_tick_params(labelsize=15)
    heatmap.yaxis.set_tick_params(labelsize=15)
    heatmap.figure.axes[-1].yaxis.label.set_size(20)
    cbar = heatmap.collections[0].colorbar
    cbar.ax.tick_params(labelsize=15)
    plt.xticks(rotation=45)
    # plt.title("Korrelationskoeffizienten für verschiedene Parameter", pad=20, weight='bold', size=30)
    fig.savefig(r"C:\Users\VID\Desktop\Betriebliche_Praxis\Graphs/" + plt_name + ".png")

# corr_main("pearson")


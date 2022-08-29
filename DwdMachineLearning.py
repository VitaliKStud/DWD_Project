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

def delete_double_values(my_list):
    clean_list = []
    for i in my_list:
        if i in clean_list:
            pass
        else:
            clean_list.append(i)
    return clean_list

def regression():
    # for date in range(0, len(month_step())):
    #     start_date_ = month_step()[date][0]
    #     end_date_ = month_step()[date][1]

    stations_names_in_date = []
    start_date_ = 200001010000
    end_date_ = 200002010000

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
                    new_df, names, density = dwd.main_analyze_data(correlation=False)
                    my_df = pd.concat([my_df, new_df], axis=1)
                    my_density.append(density)
                    print(my_density)
            column_names = list(my_df.columns)
            dataset = my_df.copy()
            dataset.tail()
            train_dataset = dataset.sample(frac=0.8, random_state=0)
            test_dataset = dataset.drop(train_dataset.index)
            sns.pairplot(train_dataset[column_names], diag_kind='kde')
            plt.show()
            print(dataset.isna().sum())
            print(dataset)
            print(my_df)
        except:
            print("error1")
            pass

regression()




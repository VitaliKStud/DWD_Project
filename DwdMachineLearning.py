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

def build_and_compile_model(norm):
  model = keras.Sequential([
      norm,
      layers.Dense(64, activation='relu'),
      layers.Dense(64, activation='relu'),
      layers.Dense(1)
  ])

  model.compile(loss='mean_absolute_error',
                optimizer=tf.keras.optimizers.Adam(0.001))
  return model

def plot_loss(history):
  plt.plot(history.history['loss'], label='loss')
  plt.plot(history.history['val_loss'], label='val_loss')
  plt.xlabel('Epoch')
  plt.ylabel('Error [MPG]')
  plt.legend()
  plt.grid(True)
  plt.show()

def prep_data_for_ml(k_factor_g=3):
    # for date in range(0, len(month_step())):
    #     start_date_ = month_step()[date][0]
    #     end_date_ = month_step()[date][1]

    start_date_ = 200001010000
    end_date_ = 200002010000

    air_list = []
    air = main_dwd(local_domain=local_domain_,
                 type_of_data=type_of_data_list[0],
                 type_of_time="historical",
                 start_date=start_date_, end_date=end_date_).main_activ_stations_in_date()
    for a in range(0, len(air[3]),1):
        air_list.append(air[3][a].split("_")[1])

    perc_list = []
    perc = main_dwd(local_domain=local_domain_,
                 type_of_data=type_of_data_list[1],
                 type_of_time="historical",
                 start_date=start_date_, end_date=end_date_).main_activ_stations_in_date()
    for p in range(0, len(perc[3]),1):
        perc_list.append(perc[3][p].split("_")[1])

    solar_list = []
    solar = main_dwd(local_domain=local_domain_,
                 type_of_data=type_of_data_list[2],
                 type_of_time="historical",
                 start_date=start_date_, end_date=end_date_).main_activ_stations_in_date()
    for s in range(0, len(solar[3]),1):
        solar_list.append(solar[3][s].split("_")[1])

    wind_list = []
    wind = main_dwd(local_domain=local_domain_,
                 type_of_data=type_of_data_list[3],
                 type_of_time="historical",
                 start_date=start_date_, end_date=end_date_).main_activ_stations_in_date()
    for w in range(0, len(wind[3]),1):
        wind_list.append(wind[3][w].split("_")[1])


    for stations in air_list:
        my_df = pd.DataFrame([])
        my_density = []
        names_type = "air_temperature"
        prefix = f"{type_dict[names_type]}_"
        information = main_dwd(local_domain=local_domain_,
                               type_of_data=names_type,
                               type_of_time="historical",
                               start_date=start_date_, end_date=end_date_).main_station_information(f"{prefix}{stations}")
        y_coordinate_ = information["geoBreite"]
        x_coordinate_ = information["geoLaenge"]
        z_coordinate_ = 0  # not needed for now (maybe in future)
        compare_station_ = f"{prefix}{stations}"

        parameter = "TT_10"
        print(parameter)
        looking_for_ = [parameter]
        dwd = main_dwd(local_domain=local_domain_,
                       type_of_data=names_type,
                       type_of_time="historical",
                       start_date=start_date_,
                       end_date=end_date_,
                       k_factor=k_factor_g+2,
                       compare_station=compare_station_,
                       x_coordinate=x_coordinate_,
                       y_coordinate=y_coordinate_,
                       z_coordinate=z_coordinate_,
                       looking_for=looking_for_)
        new_df, index_for_plot, column_name_list, data_density = dwd.main_analyze_data(correlation=False, compare_station=f"{prefix}{stations}")
        new_df.pop("DATA_SUMM")
        column_names = list(new_df.columns)
        is_nan_list = new_df.isna().sum()
        counter = 0
        for i in is_nan_list:
            if i > len(new_df)/2:
                new_df.pop(column_names[counter])
                counter += 1
            else:
                counter += 1

        dnn_model = tf.keras.models.load_model('dnn_model')
        # print(dnn_model.shape())

        dataset = new_df.copy()
        dataset.tail()
        dataset = dataset.dropna()

        # train_dataset = dataset.sample(frac=0.8, random_state=0)
        # test_dataset = dataset.drop(train_dataset.index)
        test_dataset = dataset

        # train_features = train_dataset.copy()
        test_features = test_dataset.copy()

        # train_labels = train_features.pop(column_names[0])
        test_labels = test_features.pop(column_names[0])

        # normalizer = tf.keras.layers.Normalization(axis=-1)
        # normalizer.adapt(np.array(train_features))

        # dnn_model = build_and_compile_model(normalizer)

        # history = dnn_model.fit(
        #     train_features,
        #     train_labels,
        #     validation_split=0.2,
        #     verbose=0, epochs=100)

        print(dnn_model.evaluate(test_features, test_labels, verbose=0))

        test_predictions = dnn_model.predict(test_features).flatten()

        a = plt.axes(aspect='equal')
        plt.scatter(test_labels, test_predictions)
        plt.xlabel('True Values [MPG]')
        plt.ylabel('Predictions [MPG]')
        lims = [-10, 15]
        plt.xlim(lims)
        plt.ylim(lims)
        _ = plt.plot(lims, lims)
        plt.show()

        error = test_predictions - test_labels
        plt.hist(error, bins=25)
        plt.xlabel('Prediction Error [MPG]')
        _ = plt.ylabel('Count')
        plt.show()

        # dnn_model.save('dnn_model')



        # sns.pairplot(train_dataset[column_names], diag_kind='kde')
        # plt.show()

prep_data_for_ml(k_factor_g=50)




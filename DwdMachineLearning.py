import os
import math
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
import visualkeras

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

def prep_data_for_ml(k_factor_g=3, parameter_n=1, stations_per_month=1, start_date=0, end_date=0, type="PP_10"):
    if type == "PP_10" or type == "TT_10" or type == "TD_10" or type == "RF_10":
        names_type_new = "air_temperature"
    elif type == "RWS_10" or type == "RWS_IND_10":
        names_type_new = "precipitation"
    elif type == "DS_10" or type == "GS_10" or type == "SD_10":
        names_type_new = "solar"
    elif type == "FF_10" or type == "DD_10":
        names_type_new = "wind"

    start_date_ = start_date
    end_date_ = end_date
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

    count_norm = 0
    names_type = names_type_new
    prefix = f"{type_dict[names_type]}_"
    if type == "PP_10" or type == "TT_10" or type == "TD_10" or type == "RF_10":
        random = randint(0, len(air_list) - 1)
        information = main_dwd(local_domain=local_domain_,
                               type_of_data=names_type,
                               type_of_time="historical",
                               start_date=start_date_, end_date=end_date_).main_station_information(f"{prefix}{air_list[random]}")
    elif type == "RWS_10" or type == "RWS_IND_10":
        random = randint(0, len(perc_list) - 1)
        information = main_dwd(local_domain=local_domain_,
                               type_of_data=names_type,
                               type_of_time="historical",
                               start_date=start_date_, end_date=end_date_).main_station_information(f"{prefix}{perc_list[random]}")
    elif type == "DS_10" or type == "GS_10" or type == "SD_10":
        random = randint(0, len(solar_list) - 1)
        information = main_dwd(local_domain=local_domain_,
                               type_of_data=names_type,
                               type_of_time="historical",
                               start_date=start_date_, end_date=end_date_).main_station_information(f"{prefix}{solar_list[random]}")
    elif type == "FF_10" or type == "DD_10":
        random = randint(0, len(wind_list) - 1)
        information = main_dwd(local_domain=local_domain_,
                               type_of_data=names_type,
                               type_of_time="historical",
                               start_date=start_date_, end_date=end_date_).main_station_information(f"{prefix}{wind_list[random]}")
    my_df = pd.DataFrame([])
    my_density = []

    y_coordinate_ = information["geoBreite"]
    x_coordinate_ = information["geoLaenge"]
    z_coordinate_ = 0  # not needed for now (maybe in future)

    if type == "PP_10" or type == "TT_10" or type == "TD_10" or type == "RF_10":
        compare_station_ = f"{prefix}{air_list[random]}"
    elif type == "RWS_10" or type == "RWS_IND_10":
        compare_station_ = f"{prefix}{perc_list[random]}"
    elif type == "DS_10" or type == "GS_10" or type == "SD_10":
        compare_station_ = f"{prefix}{solar_list[random]}"
    elif type == "FF_10" or type == "DD_10":
        compare_station_ = f"{prefix}{wind_list[random]}"
    print(compare_station_)

    parameter = type
    print(parameter)
    looking_for_ = [parameter]
    dwd = main_dwd(local_domain=local_domain_,
                   type_of_data=names_type,
                   type_of_time="historical",
                   start_date=start_date_,
                   end_date=end_date_,
                   k_factor=k_factor_g+1,
                   compare_station=compare_station_,
                   x_coordinate=x_coordinate_,
                   y_coordinate=y_coordinate_,
                   z_coordinate=z_coordinate_,
                   looking_for=looking_for_)


    if type == "PP_10" or type == "TT_10" or type == "TD_10" or type == "RF_10":
        new_df_1, index_for_plot, column_name_list, data_density, dist, height, my_bool = dwd.main_analyze_data(correlation=False, compare_station=f"{prefix}{air_list[random]}")
    elif type == "RWS_10" or type == "RWS_IND_10":
        new_df_1, index_for_plot, column_name_list, data_density, dist, height, my_bool = dwd.main_analyze_data(correlation=False, compare_station=f"{prefix}{perc_list[random]}")
    elif type == "DS_10" or type == "GS_10" or type == "SD_10":
        new_df_1, index_for_plot, column_name_list, data_density, dist, height, my_bool = dwd.main_analyze_data(correlation=False, compare_station=f"{prefix}{solar_list[random]}")
    elif type == "FF_10" or type == "DD_10":
        new_df_1, index_for_plot, column_name_list, data_density, dist, height, my_bool = dwd.main_analyze_data(correlation=False, compare_station=f"{prefix}{wind_list[random]}")

    if parameter_n == 2:
        parameter_2 = type
        print(parameter_2)
        looking_for_2 = [parameter_2]
        dwd = main_dwd(local_domain=local_domain_,
                       type_of_data=names_type,
                       type_of_time="historical",
                       start_date=start_date_,
                       end_date=end_date_,
                       k_factor=k_factor_g+1,
                       compare_station=compare_station_,
                       x_coordinate=x_coordinate_,
                       y_coordinate=y_coordinate_,
                       z_coordinate=z_coordinate_,
                       looking_for=looking_for_2)

        if type == "PP_10" or type == "TT_10" or type == "TD_10" or type == "RF_10":
            new_df_2, index_for_plot_2, column_name_list_2, data_density_2, dist_2, height_2, my_bool_2 = dwd.main_analyze_data(correlation=False, compare_station=f"{prefix}{air_list[random]}")
        elif type == "RWS_10" or type == "RWS_IND_10":
            new_df_2, index_for_plot_2, column_name_list_2, data_density_2, dist_2, height_2, my_bool_2 = dwd.main_analyze_data(correlation=False, compare_station=f"{prefix}{perc_list[random]}")
        elif type == "DS_10" or type == "GS_10" or type == "SD_10":
            new_df_2, index_for_plot_2, column_name_list_2, data_density_2, dist_2, height_2, my_bool_2 = dwd.main_analyze_data(correlation=False, compare_station=f"{prefix}{solar_list[random]}")
        elif type == "FF_10" or type == "DD_10":
            new_df_2, index_for_plot_2, column_name_list_2, data_density_2, dist_2, height_2, my_bool_2 = dwd.main_analyze_data(correlation=False, compare_station=f"{prefix}{wind_list[random]}")



        new_df = pd.concat([new_df_1, new_df_2], axis=1)
        if my_bool == False or my_bool_2 == False:
            print("no")
            column_names = []
        else:
            new_df.pop("DATA_SUMM")
            if type == "PP_10" or type == "TT_10" or type == "TD_10" or type == "RF_10":
                new_df.pop(f"{prefix}{air_list[random]}_{parameter_2}")
            elif type == "RWS_10" or type == "RWS_IND_10":
                new_df.pop(f"{prefix}{perc_list[random]}_{parameter_2}")
            elif type == "DS_10" or type == "GS_10" or type == "SD_10":
                new_df.pop(f"{prefix}{solar_list[random]}_{parameter_2}")
            elif type == "FF_10" or type == "DD_10":
                new_df.pop(f"{prefix}{wind_list[random]}_{parameter_2}")

            column_names = list(new_df.columns)
            is_nan_list = new_df.isna().sum()
            counter = 0
            for i in is_nan_list:
                if i > len(new_df)/2:
                    new_df.pop(column_names[counter])
                    counter += 1
                else:
                    counter += 1
        return new_df, index_for_plot, column_names, data_density, dist, height, my_bool, index_for_plot_2, column_name_list_2, data_density_2, dist_2, height_2, my_bool_2
    else:
        new_df = new_df_1
        if my_bool == False:
            print("no")
            column_names = []
        else:
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
        return new_df, index_for_plot, column_names, data_density, dist, height, my_bool, False, False, False, False, False, False





        #     if test_modell:
        #         if my_bool and my_bool_2:
        #             machine_learning(new_df, column_names, dist, height, shape=k_factor_g, parameter=2)
        #         else:
        #             pass
        #     else:
        #         if my_bool and my_bool_2:
        #             if count_norm == 0:
        #                 machine_learning_modelling(new_df, column_names, dist, height, shape=k_factor_g, parameter=2)
        #                 count_norm += 1
        #                 print(count_norm)
        #             else:
        #                 print("im here")
        #                 machine_learning_modelling(new_df, column_names, dist, height, shape=k_factor_g, normalize=False, parameter=2)
        #         else:
        #             pass
        # else:
        #     new_df = new_df_1
        #     if my_bool == False:
        #         print("no")
        #         column_names = []
        #     else:
        #         new_df.pop("DATA_SUMM")
        #         column_names = list(new_df.columns)
        #         # is_nan_list = new_df.isna().sum()
        #         # counter = 0
        #         # for i in is_nan_list:
        #         #     if i > len(new_df)/2:
        #         #         new_df.pop(column_names[counter])
        #         #         counter += 1
        #         #     else:
        #         #         counter += 1
        #         # print(new_df)
        #     if test_modell:
        #         if my_bool:
        #             machine_learning(new_df, column_names, dist, height, shape=k_factor_g, parameter=1)
        #         else:
        #             pass
        #     else:
        #         if my_bool:
        #             if count_norm == 0:
        #                 machine_learning_modelling(new_df, column_names, dist, height, shape=k_factor_g, parameter=1)
        #                 count_norm += 1
        #                 print(count_norm)
        #             else:
        #                 print("im here")
        #                 machine_learning_modelling(new_df, column_names, dist, height, shape=k_factor_g, normalize=False, parameter=1)
        #         else:
        #             pass




        # print(dnn_model.shape())



        # sns.pairplot(train_dataset[column_names], diag_kind='kde')
        # plt.show()



def plot_loss(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.legend()
    plt.show()

def plot_horsepower(x, y):
    plt.scatter(train_features['Horsepower'], train_labels, label='Data')
    plt.plot(x, y, color='k', label='Predictions')
    plt.xlabel('Horsepower')
    plt.ylabel('MPG')
    plt.legend()

def build_and_compile_model(shape=5, parameter=1, height=True):
    inputs = keras.Input(shape=(shape,), name="InputsData1")
    input_2 = keras.Input(shape=(shape,), name="InputsDistance")
    # input_3 = keras.Input(shape=(shape,), name="InputsHeight")

    # dense = layers.Dense(8, activation="relu", name="HiddenLayer1ForData1")
    # x = dense(inputs)
    norm = layers.Normalization()
    x = norm(inputs)
    x = layers.Dense(16, activation="relu", name="HiddenLayer2ForData1")(x)
    x = layers.Dense(32, activation="relu", name="HiddenLayer3ForData1")(x)
    x = layers.Dense(64, activation="relu", name="HiddenLayer4ForData1")(x)
    x = layers.Dense(128, activation="relu", name="HiddenLayer5ForData1")(x)
    # x = layers.Embedding(shape, 16)(x)
    # x = layers.LSTM(16, activation="relu")(x)

    # dense_2 = layers.Dense(128, activation="relu", name="HiddenLayer1ForDistance")
    # x_2 = dense_2(input_2)
    norm_2 = layers.Normalization()
    x_2 = norm_2(input_2)
    x_2 = layers.Dense(16, activation="relu", name="HiddenLayer2ForDistance")(x_2)
    x_2 = layers.Dense(32, activation="relu", name="HiddenLayer3ForDistance")(x_2)
    x_2 = layers.Dense(64, activation="relu", name="HiddenLayer4ForDistance")(x_2)
    x_2 = layers.Dense(128, activation="relu", name="HiddenLayer5ForDistance")(x_2)
    # x_2 = layers.Embedding(shape, 16)(x_2)
    # x_2 = layers.LSTM(16, activation="relu")(x_2)

    dense_3 = layers.Dense(32, activation="relu", name="HiddenLayer1ForHeight")
    x_3 = dense_3(input_3)
    x_3 = layers.Dense(64, activation="relu", name="HiddenLayer2ForHeight")(x_3)

    if parameter == 2:
        input_4 = keras.Input(shape=(shape,), name="InputsData2")

        dense_4 = layers.Dense(32, activation="relu", name="HiddenLayer1ForData2")
        x_4 = dense_4(input_4)
        x_4 = layers.Dense(16, activation="relu", name="HiddenLayer2ForData2")(x_4)

        combo = layers.concatenate([x_4, x_3, x_2, x], name="ConnectHiddenLayers")
        y = layers.Dense(8, activation="relu", name="HiddenLayerForConnection")(combo)
        outputs = layers.Dense(1, name="OutputsDataForMyLocation")(y)

        model = keras.Model(inputs=[inputs, input_2, input_3, input_4], outputs=outputs, name="dnn_model")
    else:
        # combo_0 = layers.concatenate([x_2, x_3], name="ConnectHiddenLayersZero")
        # y_0 = layers.Dense(128, activation="relu", name="HiddenLayerForConnectionZero")(combo_0)

        combo = layers.concatenate([x, x_2], name="ConnectHiddenLayers")
        y = layers.Dense(512, activation="relu", name="HiddenLayerForConnection")(combo)
        outputs = layers.Dense(1, name="OutputsDataForMyLocation")(y)

        model = keras.Model(inputs=[inputs, input_2], outputs=outputs, name="dnn_model_pp_10")
    # huber_loss
    # mean_absolute_error
    # "mse"
    model.compile(loss="huber_loss",
                optimizer=tf.keras.optimizers.Adam(0.001))
    model.summary()
    tf.keras.utils.plot_model(model, "multi_input_and_output_model.png", show_shapes=True, show_layer_activations=True,
                              expand_nested=True, show_dtype=True)
    return model

def data_generator(station_steps, shape, parameter, start_date_, end_date_, data=True, val=False):
    i = station_steps+1
    if parameter == 1:
        my_df, index_for_plot, column_names, data_density, dist, height, my_bool, index_for_plot_2, column_name_list_2, data_density_2, dist_2, height_2, my_bool_2 = prep_data_for_ml(k_factor_g=shape,
                                                                                                                                                                                       parameter_n=parameter,
                                                                                                                                                                                       stations_per_month=i,
                                                                                                                                                                                       start_date=start_date_,
                                                                                                                                                                                       end_date=end_date_,)
        print(my_df)
        if my_bool == False:
            return False
        else:
            my_data = my_df.copy()
            my_data.tail()
            my_data = my_data.dropna()

            train_features = my_data.sample(frac=0.8, random_state=0)

            dist_1 = pd.DataFrame([dist[1:]])
            dist_1 = pd.concat([dist_1] * (len(train_features)), ignore_index=True)

            height_1 = pd.DataFrame([height[1:]])
            height_1 = pd.concat([height_1] * (len(train_features)), ignore_index=True)

            test_features = my_data.drop(train_features.index)

            real_data = test_features[column_names[0]]

            dist_2 = pd.DataFrame([dist[1:]])
            dist_2 = pd.concat([dist_2] * (len(test_features)), ignore_index=True)

            height_2 = pd.DataFrame([height[1:]])
            height_2 = pd.concat([height_2] * (len(test_features)), ignore_index=True)

            train_labels = train_features.pop(column_names[0])
            test_labels = test_features.pop(column_names[0])

            train_features = tf.convert_to_tensor(train_features)
            dist_1 = tf.convert_to_tensor(dist_1)
            height_1 = tf.convert_to_tensor(height_1)
            train_labels = tf.convert_to_tensor(train_labels)

            val_features = tf.convert_to_tensor(test_features)
            val_dist = tf.convert_to_tensor(dist_2)
            val_height = tf.convert_to_tensor(height_2)
            val_labels = tf.convert_to_tensor(test_labels)

            # print(train_features[0])
            # print(dist_1[0])
            # print(train_labels)

            if data == True:
                return {"InputsData1": train_features, "InputsDistance": dist_1, "InputsHeight": height_1}, train_labels
                # return {"InputsData1": train_features, "InputsDistance": dist_1}, train_labels
                # return {"InputsData1": train_features, "InputsHeight": height_1}, train_labels

            if val == True:
                return {"InputsData1": val_features, "InputsDistance": val_dist, "InputsHeight": val_height}, val_labels





def machine_learning_modelling(shape=5, parameter=1, epochs=100, batch_size=1, station_steps=10):
    dnn_model = build_and_compile_model(shape=shape, parameter=parameter)
    my_epoch = 0
    for date in range(0, 1):
        start_date_ = month_step()[date][0]
        end_date_ = month_step()[date][1]
        print(end_date_)
        for i in range(0, station_steps, 1):
            if parameter == 2:
                pass
            #     train_features_1 = train_features.iloc[:,1:shape+1]
            #     train_features_2 = train_features.iloc[:,shape+1:]
            #     test_features_1 = test_features.iloc[:,1:shape+1]
            #     test_features_2 = test_features.iloc[:,shape+1:]
            #     history = dnn_model.fit(
            #         [train_features_1, train_features_2, dist_1, height_1],
            #         train_labels,
            #         validation_split=0.2, batch_size=batch_size,
            #         verbose=0, epochs=epochs)
            #     print(dnn_model.evaluate([train_features_1, test_features_2, dist_2, height_2], test_labels, verbose=0))
            #     test_predictions = dnn_model.predict([test_features_1, test_features_2, dist_2, height_2]).flatten()
            #     y = dnn_model.predict([test_features_1, test_features_2, dist_2, height_2])
            else:
                # history = dnn_model.fit([test_features, dist_2, height_2], test_labels,
                #                         batch_size=batch_size,
                #                         validation_split=0.2,
                #                         verbose=0,
                #                         epochs=epochs)
                gen_data = data_generator(i, shape, parameter, start_date_=start_date_, end_date_=end_date_, data=True, val=False)
                if gen_data == False:
                    pass
                else:
                # if gen_data[0] == False:
                #     pass
                # else:
                    batch_size_0 = int(len(gen_data[1]) * 0.8)
                    # batch_size_0 = 30
                    len_data = len(gen_data[1]) // batch_size_0
                    print(len(gen_data[1]))

                    # val_data = data_generator(station_steps, shape, parameter, data=False, val=True)
                    history = dnn_model.fit(gen_data[0], gen_data[1], gen_data[2],
                                            # validation_data=val_data,
                                            validation_split=0.2,
                                            # batch_size=batch_size_0,
                                            verbose=1,
                                            epochs = my_epoch + 200,
                                            steps_per_epoch=len_data,
                                            initial_epoch=my_epoch)
                    my_epoch = my_epoch + 200
                    print(history)
                    # plot_loss(history)
                    print(dnn_model.evaluate(gen_data[0], gen_data[1], verbose=0))
                    # test_predictions = dnn_model.predict(gen_data[0]).flatten()
                    # y = dnn_model.predict(gen_data[0])
                    # print(dnn_model)
                    # tf.keras.backend.clear_session()
                    # plot_loss(history)

                    # x = tf.linspace(0.0, len(y)-1, len(y))
                    #
                    # plt.plot(x, real_data)
                    # plt.plot(x,y)
                    # plt.show()
                    #
                    # a = plt.axes(aspect='equal')
                    # plt.scatter(test_labels, test_predictions)
                    # plt.xlabel('True Values [MPG]')
                    # plt.ylabel('Predictions [MPG]')
                    # lims = [-10, 15]
                    # plt.xlim(lims)
                    # plt.ylim(lims)
                    # _ = plt.plot(lims, lims)
                    # plt.show()
                    #
                    # error = test_predictions - test_labels
                    # plt.hist(error, bins=25)
                    # plt.xlabel('Prediction Error [MPG]')
                    # _ = plt.ylabel('Count')
                    # plt.show()

    dnn_model.save('dnn_model_pp_10')

def std_from_list (my_list):
    avg = sum(my_list)/len(my_list)
    a = 0
    for i in my_list:
        a = a + (i - avg)**2
    std = np.sqrt(a/len(my_list))
    return 2*std

def machine_learning(shape=5, parameter=1, type="PP_10"):
    absolute_abweichung = []
    error = []
    type_new = type.lower()

    for date in range(0, len(month_step())):
        start_date_ = month_step()[date][0]
        end_date_ = month_step()[date][1]
        if start_date_ == 200407010000:
            pass
        else:
            print(start_date_)
            print(end_date_)
            for i in range(0,1,1):
                if parameter == 1:
                    my_df, index_for_plot, column_names, data_density, dist, height, my_bool, index_for_plot_2, column_name_list_2, data_density_2, dist_2, height_2, my_bool_2 = prep_data_for_ml(k_factor_g=shape,
                                                                                                                                                                                                   parameter_n=parameter,
                                                                                                                                                                                                   start_date=start_date_,
                                                                                                                                                                                                   end_date=end_date_,
                                                                                                                                                                                                   stations_per_month=i,
                                                                                                                                                                                                   type=type)
                    if my_bool == False:
                        pass
                    else:
                        dnn_model = tf.keras.models.load_model('dnn_model_'+type_new)
                        tf.keras.utils.plot_model(dnn_model, "multi_input_and_output_model.png", show_shapes=True)
                        # dnn_model.summary()
                        dataset = my_df.copy()
                        dataset.tail()
                        dataset = dataset.dropna()
                        real_data = dataset[column_names[0]]

                        test_dataset = dataset.pop(column_names[0])

                        # dist_1 = tf.convert_to_tensor(dist[1:])
                        # dist_1 = pd.DataFrame([dist[1:]])
                        # dist_1 = dist_1.append([dist_1]*(len(test_dataset)-1), ignore_index=True)

                        # dist_2 = tf.convert_to_tensor(dist[1:])
                        dist_2 = pd.DataFrame([dist[1:]])
                        # dist_2 = dist_2.append([dist_2]*(len(test_dataset)-1), ignore_index=True)
                        dist_2 = pd.concat([dist_2] * (len(test_dataset)), ignore_index=True)

                        test_features = test_dataset.copy()
                        test_features_1 = dataset.iloc[:,0:shape]
                        test_features_2 = dataset.iloc[:,shape:]

                        height_2 = pd.DataFrame([height[1:]])
                        # height_2 = height_2.append([height_2]*(len(test_features)-1), ignore_index=True)
                        height_2 = pd.concat([height_2] * (len(test_features)), ignore_index=True)


                        if parameter == 2:
                            print(dnn_model.evaluate([test_features_1, test_features_2, dist_2, height_2], real_data, verbose=0))
                            y = dnn_model.predict([test_features_1, test_features_2, dist_2, height_2])
                        else:
                            if type == "PP_10":
                                abs = dnn_model.evaluate([dataset, dist_2, height_2], real_data, verbose=0)
                                print(abs)
                                absolute_abweichung.append(abs)
                                y = dnn_model.predict([dataset, dist_2,height_2])
                            else:
                                abs = dnn_model.evaluate([dataset, dist_2], real_data, verbose=0)
                                print(abs)
                                absolute_abweichung.append(abs)
                                y = dnn_model.predict([dataset, dist_2])


                        my_new_list = []
                        for i in y:
                            for j in i:
                                my_new_list.append(j)
                        y = tf.convert_to_tensor(my_new_list)
                        data = tf.convert_to_tensor(real_data)
                        mae = tf.keras.losses.MeanAbsoluteError()
                        # err = tf.keras.losses.MeanAbsoluteError(data, y)
                        err = mae(data,y).numpy()
                        error.append(err)
                        print(err)



                        # x = tf.linspace(0.0, len(y)-1, len(y))
                        # plt.plot(x, real_data)
                        # plt.plot(x,y, lw=0.5)
                        # plt.show()

    return absolute_abweichung, error



    # error = y - real_data
    # plt.hist(error, bins=25)
    # plt.xlabel('Prediction Error [MPG]')
    # _ = plt.ylabel('Count')
    # plt.show()


machine_learning_modelling(shape=12, parameter=1, epochs=20, batch_size=1, station_steps=10)


my_types = ["PP_10"]
for i in my_types:
    my_error_list = []
    my_std_list = []
    if my_types == "PP_10" or my_types == "RF_10":
        shape=12
    else:
        shape=12
    absolute_abweichung, error = machine_learning(shape=shape, parameter=1, type=i)
    print(sum(error)/len(error))
    print(std_from_list((error)))
    my_error_list.append(sum(error)/len(error))
    my_std_list.append(std_from_list((error)))

    with open("C://Users//VID//Desktop//Betriebliche_Praxis//Ergebnisse//machine_learning//machine_learning_errors_2.txt", "w") as fp:
        json.dump(my_error_list, fp)
    with open("C://Users//VID//Desktop//Betriebliche_Praxis//Ergebnisse//machine_learning//machine_learning_std.txt_2", "w") as fp:
        json.dump(my_std_list, fp)



# prep_data_for_ml(k_factor_g=5, test_modell=True, parameter=1)
# prep_data_for_ml(k_factor_g=5, test_modell=True)






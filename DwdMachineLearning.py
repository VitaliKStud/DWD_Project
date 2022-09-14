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

def prep_data_for_ml(k_factor_g=3, test_modell=False):
    # for date in range(0, len(month_step())):
    #     start_date_ = month_step()[date][0]
    #     end_date_ = month_step()[date][1]

    start_date_ = 200001010000
    end_date_ = 200002020000

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
    for stations in range(0, len(air_list),1):
        random = randint(0, len(air_list) - 1)
        random = 0
        my_df = pd.DataFrame([])
        my_density = []
        names_type = "air_temperature"
        prefix = f"{type_dict[names_type]}_"
        information = main_dwd(local_domain=local_domain_,
                               type_of_data=names_type,
                               type_of_time="historical",
                               start_date=start_date_, end_date=end_date_).main_station_information(f"{prefix}{air_list[random]}")
        y_coordinate_ = information["geoBreite"]
        x_coordinate_ = information["geoLaenge"]
        z_coordinate_ = 0  # not needed for now (maybe in future)
        compare_station_ = f"{prefix}{air_list[random]}"
        print(compare_station_)

        parameter = "TT_10"
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
        new_df_1, index_for_plot, column_name_list, data_density, dist, height, my_bool = dwd.main_analyze_data(correlation=False, compare_station=f"{prefix}{air_list[random]}")
        parameter_2 = "TM5_10"
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
        new_df_2, index_for_plot_2, column_name_list_2, data_density_2, dist_2, height_2, my_bool_2 = dwd.main_analyze_data(correlation=False, compare_station=f"{prefix}{air_list[random]}")
        new_df = pd.concat([new_df_1, new_df_2], axis=1)
        if my_bool == False or my_bool_2 == False:
            print("no")
            column_names = []
        else:
            new_df.pop("DATA_SUMM")
            new_df.pop(f"{prefix}{air_list[random]}_{parameter_2}")
            column_names = list(new_df.columns)
            # is_nan_list = new_df.isna().sum()
            # counter = 0
            # for i in is_nan_list:
            #     if i > len(new_df)/2:
            #         new_df.pop(column_names[counter])
            #         counter += 1
            #     else:
            #         counter += 1
            # print(new_df)
        if test_modell:
            if my_bool and my_bool_2:
                machine_learning(new_df, column_names, dist, height)
            else:
                pass
        else:
            if my_bool and my_bool_2:
                if count_norm == 0:
                    machine_learning_modelling(new_df, column_names, dist, height, shape=k_factor_g)
                    count_norm += 1
                    print(count_norm)
                else:
                    print("im here")
                    machine_learning_modelling(new_df, column_names, dist, height, shape=k_factor_g, normalize=False)
            else:
                pass



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

def build_and_compile_model(shape=5):
    # model = keras.Sequential([
    #     norm,
    #     layers.Dense(128, activation='relu'),
    #     layers.Dense(128, activation='relu'),
    #     layers.Dense(1)
    # ])

    inputs = keras.Input(shape=(shape,), name="InputsData1")
    input_2 = keras.Input(shape=(shape,), name="InputsDistance")
    input_3 = keras.Input(shape=(shape,), name="InputsHeight")
    input_4 = keras.Input(shape=(shape,), name="InputsData2")

    dense = layers.Dense(64, activation="relu", name="HiddenLayer1ForData1")
    x = dense(inputs)
    x = layers.Dense(64, activation="relu", name="HiddenLayer2ForData1")(x)

    dense_2 = layers.Dense(64, activation="relu", name="HiddenLayer1ForDistance")
    x_2 = dense_2(input_2)
    x_2 = layers.Dense(64, activation="relu", name="HiddenLayer2ForDistance")(x_2)

    dense_3 = layers.Dense(64, activation="relu", name="HiddenLayer1ForHeight")
    x_3 = dense_3(input_3)
    x_3 = layers.Dense(64, activation="relu", name="HiddenLayer2ForHeight")(x_3)

    dense_4 = layers.Dense(64, activation="relu", name="HiddenLayer1ForData2")
    x_4 = dense_4(input_4)
    x_4 = layers.Dense(64, activation="relu", name="HiddenLayer2ForData2")(x_4)

    combo = layers.concatenate([x_4, x_3, x_2, x], name="ConnectHiddenLayers")
    y = layers.Dense(64, activation="relu", name="HiddenLayerForConnection")(combo)
    outputs = layers.Dense(1, name="OutputsDataForMyLocation")(y)

    model = keras.Model(inputs=[inputs, input_2, input_3, input_4], outputs=outputs, name="dnn_model")
    model.compile(loss='mean_absolute_error',
                optimizer=tf.keras.optimizers.Adam(0.001))
    model.summary()
    tf.keras.utils.plot_model(model, "multi_input_and_output_model.png", show_shapes=True, show_layer_activations=True,
                              expand_nested=True, show_dtype=True)
    return model

def machine_learning_modelling(my_df, column_names, dist, height, normalize = True, shape=5):
    #PREP DATA FOR DNN
    my_data = my_df.copy()
    my_data.tail()
    my_data = my_data.dropna()

    #SPLIT DATA
    train_features = my_data.sample(frac=0.8, random_state=0)
    train_features_1 = train_features.iloc[:,1:shape+1]
    train_features_2 = train_features.iloc[:,shape+1:]
    # dist_1 = tf.convert_to_tensor(dist[1:])
    dist_1 = pd.DataFrame([dist[1:]])
    dist_1 = dist_1.append([dist_1]*(len(train_features)-1), ignore_index=True)

    # height_1 = tf.convert_to_tensor(height[1:])
    height_1 = pd.DataFrame([height[1:]])
    height_1 = height_1.append([height_1]*(len(train_features)-1), ignore_index=True)

    # train_dist_features = dist_1.sample(frac=0.8, random_state=0)
    test_features = my_data.drop(train_features.index)
    test_features_1 = test_features.iloc[:,1:shape+1]
    test_features_2 = test_features.iloc[:,shape+1:]
    real_data = test_features[column_names[0]]

    # dist_2 = tf.convert_to_tensor(dist[1:])
    dist_2 = pd.DataFrame([dist[1:]])
    dist_2 = dist_2.append([dist_2]*(len(test_features)-1), ignore_index=True)

    # height_2 = tf.convert_to_tensor(height[1:])
    height_2 = pd.DataFrame([height[1:]])
    height_2 = height_2.append([height_2]*(len(test_features)-1), ignore_index=True)

    #GET LABELS
    train_labels = train_features.pop(column_names[0])
    test_labels = test_features.pop(column_names[0])

    #NORMALIZE
    if normalize:
        # normalizer = tf.keras.layers.Normalization(axis=-1)
        # normalizer.adapt(np.array(train_features))
        # CREATE MODELL
        dnn_model = build_and_compile_model(shape=shape)
        # inputs = tf.keras.Input(shape=(28,28))
    else:
        dnn_model = tf.keras.models.load_model('dnn_model')
    #FIT MODELL

    optimizer = keras.optimizers.SGD(learning_rate=1e-3)
    loss_fn = keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    print(train_features_1)
    print(train_features_2)
    print(test_features_1)
    print(test_features_2)

    history = dnn_model.fit(
        [train_features_1, train_features_2, dist_1, height_1],
        train_labels,
        validation_split=0.2, batch_size=100,
        verbose=0, epochs=100)
    plot_loss(history)

    print(dnn_model.evaluate([test_features_1, test_features_2, dist_2, height_2], test_labels, verbose=0))

    test_predictions = dnn_model.predict([test_features_1, test_features_2, dist_2, height_2]).flatten()

    y = dnn_model.predict([test_features_1,test_features_2, dist_2, height_2])
    x = tf.linspace(0.0, len(y)-1, len(y))

    plt.plot(x, real_data)
    plt.plot(x,y)
    plt.show()

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

    dnn_model.save('dnn_model')


def machine_learning(my_df, column_names, dist, height):
    dnn_model = tf.keras.models.load_model('dnn_model')
    dnn_model.summary()
    dataset = my_df.copy()
    dataset.tail()
    dataset = dataset.dropna()
    real_data = dataset[column_names[0]]
    test_dataset = dataset.pop(column_names[0])

    dist_1 = tf.convert_to_tensor(dist[1:])
    dist_1 = pd.DataFrame([dist[1:]])
    dist_1 = dist_1.append([dist_1]*(len(test_dataset)-1), ignore_index=True)

    dist_2 = tf.convert_to_tensor(dist[1:])
    dist_2 = pd.DataFrame([dist[1:]])
    dist_2 = dist_2.append([dist_2]*(len(test_dataset)-1), ignore_index=True)

    test_features = test_dataset.copy()
    print(dnn_model.evaluate([dataset, dist_2], real_data, verbose=0))
    y = dnn_model.predict([dataset, dist_2])
    my_new_list = []
    for i in y:
        for j in i:
            my_new_list.append(j)
    y = tf.convert_to_tensor(my_new_list)
    data = tf.convert_to_tensor(real_data)
    err = tf.keras.losses.mean_squared_error(data, y)
    print(err)


    x = tf.linspace(0.0, len(y)-1, len(y))
    plt.plot(x, real_data)
    plt.plot(x,y, lw=0.5)
    plt.show()

    tf.keras.utils.plot_model(dnn_model, "multi_input_and_output_model.png", show_shapes=True)



    # error = y - real_data
    # plt.hist(error, bins=25)
    # plt.xlabel('Prediction Error [MPG]')
    # _ = plt.ylabel('Count')
    # plt.show()



prep_data_for_ml(k_factor_g=5, test_modell=False)
# prep_data_for_ml(k_factor_g=5, test_modell=True)



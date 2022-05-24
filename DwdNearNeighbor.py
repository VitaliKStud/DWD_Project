from scipy.spatial import distance
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

os.chdir(r"C:/Users/VID/Desktop/Betriebliche Praxis/")
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 1000)
plt.style.use('dark_background')


# plt.style.use('default')

class NearNeighbor:
    def __init__(self, x_active, y_active, z_active, zip_data_active, k_factor, start_date, end_date, activ_id, station_list):
        self.zip_data_active = zip_data_active
        self.x_active = x_active
        self.y_active = y_active
        self.z_active = z_active
        self.k_factor = k_factor
        self.start_date = start_date
        self.end_date = end_date
        self.distance = distance.squareform(distance.pdist(self.zip_data_active, "euclidean"))
        self.closest = np.argsort(self.distance, axis=1)
        self.activ_id = activ_id
        self.station_list = station_list

    def get_start_date(self):
        return self.start_date

    def find_near(self):
        x_near = np.array([])
        y_near = np.array([])
        z_near = np.array([])
        activ_near_id = []
        for i in self.closest[:, 1:self.k_factor + 1][0]:
            x_i = self.x_active[i:i + 1]
            y_i = self.y_active[i:i + 1]
            z_i = self.z_active[i:i + 1]
            x_near = np.append(x_near, x_i)
            y_near = np.append(y_near, y_i)
            z_near = np.append(z_near, z_i)
            activ_near_id.append(self.activ_id[i])
        return x_near, y_near, z_near, activ_near_id

    def datapath_near(self):
        datapath_near_list = []
        column_names_list = []
        column_name_list = []
        counter = 0
        for i in self.closest[:, 1:self.k_factor + 1][0]:
            datapath_near_list.append(self.station_list[self.activ_id[i]].generate_tu_data_path_date(self.start_date, self.end_date))
            column_name_list.append(self.activ_id[i])
            for j in range(len(datapath_near_list[counter])):
                column_names_list.append(self.activ_id[i])
            counter = counter + 1
        return datapath_near_list, column_names_list, column_name_list

    def dataframe_near_from_to(self):
        df_from = pd.DataFrame([])
        df_to = pd.DataFrame([])
        datapath_near_list, column_names_list, column_name_list = self.datapath_near()
        for i in range(len(datapath_near_list)):
            for j in datapath_near_list[i]:
                data = pd.read_csv(j, sep=";", usecols=["MESS_DATUM"])
                df_from = pd.concat([df_from, data.iloc[[0]]], ignore_index=True)
                df_to = pd.concat([df_to, data.iloc[[-1]]], ignore_index=True)
        df_from = df_from.rename(columns={"MESS_DATUM": "FROM_DATE"})
        df_to = df_to.rename(columns={"MESS_DATUM": "TO_DATE"})
        df_from_to = df_from.join(df_to)
        del df_from
        del df_to
        return df_from_to, datapath_near_list, column_names_list, column_name_list

    def dataframe_near_from_to_path(self):
        df_from_to, datapath_near_list, column_names_list, column_name_list = self.dataframe_near_from_to()
        free_list = []
        for i in range(len(datapath_near_list)):
            for j in datapath_near_list[i]:
                free_list.append(j)
        df_data_path = pd.DataFrame(free_list, columns=["DATA_PATH"])
        df_from_to = df_from_to.join(df_data_path["DATA_PATH"])
        return df_from_to, column_names_list, column_name_list

    def date_range_df(self):
        start_date = datetime.strptime(str(self.start_date), "%Y%m%d%H%M")
        end_date = datetime.strptime(str(self.end_date), "%Y%m%d%H%M")
        date_range_df = pd.DataFrame([])
        delta = end_date - start_date
        date_range_df = pd.concat([date_range_df, pd.DataFrame([int((start_date + timedelta(minutes=i * 10)).strftime("%Y%m%d%H%M")) for i in range(int(delta / timedelta(minutes=10)) + 1)])], ignore_index=True)
        date_range_df.columns = ['MESS_DATUM_GENERATED']
        date_range_df.loc[:, 'DATA_SUMM_TT_10'] = np.nan
        return date_range_df

    def average_for_coordinate(self, data_looking_for="TT_10"):
        date_range_df = self.date_range_df().set_index('MESS_DATUM_GENERATED')
        df_from_to, column_names_list, column_name_list = self.dataframe_near_from_to_path()
        counter = 0
        for i in column_name_list:
            date_range_df.loc[:, str(i)] = np.nan
        for i in df_from_to["DATA_PATH"]:
            df_tt_10 = pd.read_csv(i, sep=";", usecols=["MESS_DATUM", data_looking_for], index_col=["MESS_DATUM"])
            mask = df_tt_10[data_looking_for] > -999
            df_tt_10 = df_tt_10[mask]
            df_tt_10 = df_tt_10.rename(columns={data_looking_for: column_names_list[counter]})
            #             date_range_df[str(column_name_list[counter])] = df_tt_10["TT_10"]
            #             date_range_df = pd.concat([date_range_df, df_tt_10], ignore_index=False)
            date_range_df.update(df_tt_10)
            counter = counter + 1
        data_all = date_range_df
        data_mean = date_range_df.mean(axis=1)
        index_for_plot = data_all.index
        index_for_plot = pd.to_datetime(index_for_plot, format='%Y%m%d%H%M')
        #         mask = data_mean.notnull()
        #         index_for_plot = index_for_plot[mask]
        #         data_mean = data_mean[mask]
        return data_all, data_mean, index_for_plot, column_name_list

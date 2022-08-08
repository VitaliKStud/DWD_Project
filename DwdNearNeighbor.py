from scipy.spatial import distance
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import os

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 1000)


class NearNeighbor:
    """
    :Description: This class is finding near neighbors for the location you choosed and creates all the needed data as a DataFrame
    """
    def __init__(self, x_active, y_active, z_active, zip_data_active, k_factor, start_date, end_date, activ_id, station_list):
        """
        :param x_active: x-coordinates (geoLaenge): **as array**. Should be set from DwdDataPrep.data_prep_for_new_location()
        :param y_active: y-coordinates (geoBreite): **as array**. Should be set from DwdDataPrep.data_prep_for_new_location()
        :param z_active: z-coordinates (Stationshoehe): **as array**. Should be set from DwdDataPrep.data_prep_for_new_location()
        :param zip_data_active: **as array**. Zipped x-coordinates and y-coordinates.
        :param k_factor: **as int**. How many stations you want to find around your coordinates?
        :param start_date: **as int**. --> YYYYMMDDHHMM
        :param end_date: **as int**. --> YYYYMMDDHHMM
        :param activ_id: **as list**. All the activ stations in timedelta
        :param station_list: **as dict**. All the stations as an object in a dictionary
        """
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

    def find_near(self):
        """
        :Description: Will find all the near stations around your location.

        :return: x_near, y_near, z_near, activ_near_id: **as array - activ_near_id as list**
        """
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
        """
        :Description: Is getting all the paths for data of all the near stations in timedelta. Also creating a list with the columnnames for your DataFrame

        :return: datapath_near_list, column_names_list, column_name_list: **all as list**
        """
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
        """
        :Description: Is generating a DataFrame with alle the dates inside your files (timedelta for every file) inside your timedelta. Also returning same lists from self.datapath_near()

        :return: df_from_to, datapath_near_list, column_names_list, column_name_list: **as list, df_from_to as DataFrame**
        """
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
        """
        :Description: Is connecting df_from_to with datapah_near_list for easier handling.

        :return: df_from_to, column_names_list, column_name_list: **as list, df_from_to as DataFrame**
        """
        df_from_to, datapath_near_list, column_names_list, column_name_list = self.dataframe_near_from_to()
        free_list = []
        for i in range(len(datapath_near_list)):
            for j in datapath_near_list[i]:
                free_list.append(j)
        df_data_path = pd.DataFrame(free_list, columns=["DATA_PATH"])
        df_from_to = df_from_to.join(df_data_path["DATA_PATH"])
        return df_from_to, column_names_list, column_name_list

    def date_range_df(self):
        """
        :Description: Is generating an empty DataFrame for timedelta. If you want to change the resolution to 1 minute, you should make some changes here

        :return: date_range_df: **as DataFrame**
        """
        start_date = datetime.strptime(str(self.start_date), "%Y%m%d%H%M")
        end_date = datetime.strptime(str(self.end_date), "%Y%m%d%H%M")
        date_range_df = pd.DataFrame([])
        delta = end_date - start_date
        date_range_df = pd.concat([date_range_df, pd.DataFrame([int((start_date + timedelta(minutes=i * 10)).strftime("%Y%m%d%H%M")) for i in range(int(delta / timedelta(minutes=10)) + 1)])], ignore_index=True)
        date_range_df.columns = ['MESS_DATUM_GENERATED']
        date_range_df.loc[:, 'DATA_SUMM'] = np.nan
        return date_range_df

    def average_for_coordinate(self, data_looking_for="TT_10", qn_weight_n_avg=False, distance_weight_n_avg=False, qn_distance_weight_n_avg=False, compare_n_avg=False, compare_station=None):
        """
        :Description: Is calculation different variants.

        :param: data_looking_for="TT_10": **as string**. Check Dwd.Dict title_dict or unit_dict.
        :param: qn_weight_n_avg=False: **as Boolean**. If True weight the quality of data.
        :param: distance_weight_n_avg=False: **as Boolean**. If True weight the distance of data.
        :param: qn_distance_weight_n_avg=False (not needed for now, maybe in future): **as Boolean**.
        :param: compare_n_avg=False: **as Boolean**. If you want to compare, how accurate your methods are, set True and choose coordinates for a station.
        :param: compare_station=None: **as string**. If compare_n_avg==True set this as the name of a station with the right prefix
        :return: if compare_n_avg==True: data_all (**as DataFrame**), data_mean (**as DataFrame**), index_for_plot (**as list**), column_name_list (**as list**), data_to_compare (**as DataFrame**), diff (**as DataFrame**), maximum (**as int**), avg_diff (**as array**)
        :return: if compare_n_avg==False: data_all (**as DataFrame**), data_mean (**as DataFrame**), index_for_plot (**as list**), column_name_list (**as list**)
        """

        if qn_weight_n_avg:
            print("qn_weight")
            date_range_df = self.date_range_df().set_index('MESS_DATUM_GENERATED')
            date_range_q_df = self.date_range_df().set_index('MESS_DATUM_GENERATED')
            df_from_to, column_names_list, column_name_list = self.dataframe_near_from_to_path()
            counter = 0
            for i in column_name_list:
                date_range_df.loc[:, str(i)] = np.nan
                date_range_q_df.loc[:, str(i)] = np.nan
            for i in df_from_to["DATA_PATH"]:
                df_tt_10 = pd.read_csv(i, sep=";", usecols=["MESS_DATUM", data_looking_for], index_col=["MESS_DATUM"])
                df_qn = pd.read_csv(i, sep=";", usecols=[1, 2], index_col=["MESS_DATUM"])
                mask = df_tt_10[data_looking_for] > -999
                df_tt_10 = df_tt_10[mask]
                df_qn = df_qn[mask]
                df_tt_10 = df_tt_10.rename(columns={data_looking_for: column_names_list[counter]})
                df_qn.columns = [column_names_list[counter]]
                date_range_df.update(df_tt_10)
                date_range_q_df.update(df_qn)
                counter = counter + 1
            if compare_n_avg:
                data_all = date_range_df
                data_to_compare = data_all[compare_station]
                data_quality = date_range_q_df.iloc[:, 2:].div(date_range_q_df.iloc[:, 2:].sum(axis=1, min_count=1), axis=0)
                data_all_qn = data_all.iloc[:, 2:].mul(data_quality)
                data_mean = data_all_qn.sum(axis=1, min_count=1)
                diff = (data_mean - data_to_compare).abs()
                maximum = diff.max()
                avg_diff = np.full((len(diff)), diff.sum()/(len(diff)-diff.isna().sum()))
                index_for_plot = data_all.index
                index_for_plot = pd.to_datetime(index_for_plot, format='%Y%m%d%H%M')
                print(data_quality)
                print(data_all_qn)
                print(f"Data All: \n{data_all}\n")
                print(f"Data mean: \n{data_mean}\n")
                print(f"maximum: \n{maximum}\n")
                print(f"avg_diff: \n{avg_diff[0]}\n")
                return data_all, data_mean, index_for_plot, column_name_list, data_to_compare, diff, maximum, avg_diff
            else:
                data_all = date_range_df
                data_quality = date_range_q_df.iloc[:, 1:].div(date_range_q_df.iloc[:, 1:].sum(axis=1, min_count=1), axis=0)
                data_all_qn = data_all.iloc[:, 1:].mul(data_quality)
                data_mean = data_all_qn.sum(axis=1, min_count=1)
                index_for_plot = data_all.index
                index_for_plot = pd.to_datetime(index_for_plot, format='%Y%m%d%H%M')
                print(f"Data All: \n{data_all}\n")
                print(f"Data mean: \n{data_mean}\n")
                return data_all, data_mean, index_for_plot, column_name_list
        elif distance_weight_n_avg:
            print("distance weight")
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
                date_range_df.update(df_tt_10)
                counter = counter + 1
            if compare_n_avg:
                sorted_distance = np.sort(self.distance[0], axis=0)[2:self.k_factor + 1]
                distance_quality = (1 - sorted_distance / np.sum(sorted_distance)) / (self.k_factor - 2)
                mask_for_quality = date_range_df.iloc[:,2:].notnull()
                quality_mask = mask_for_quality.multiply(distance_quality, fill_value=np.nan).replace({0: np.nan})
                data_quality = quality_mask.div(quality_mask.sum(axis=1, min_count=1), axis=0)
                data_number = mask_for_quality.multiply(1, fill_value=np.nan).replace({0: np.nan})
                data_factor = (data_number.sum(axis=1, min_count=1))/(self.k_factor-1)
                data_density = data_factor.sum()/(len(data_factor) - data_factor.isna().sum())
                data_all = date_range_df
                data_all_distance = data_all.iloc[:, 2:].mul(data_quality)
                data_mean = data_all_distance.sum(axis=1, min_count=1)
                data_to_compare = data_all[compare_station]
                diff = (data_mean - data_to_compare).abs()
                diff_sqr = (data_mean - data_to_compare)**2
                rmse = np.sqrt(np.full((len(diff_sqr)), diff_sqr.sum()/(len(diff_sqr)-diff_sqr.isna().sum())))
                maximum = diff.max()
                avg_diff = np.full((len(diff)), diff.sum()/(len(diff)-diff.isna().sum()))
                index_for_plot = data_all.index
                index_for_plot = pd.to_datetime(index_for_plot, format='%Y%m%d%H%M')
                print(f"data density: {data_density:.8f}")
                print(f"max of data-quality (approx. 1 is correct): {data_quality.sum(axis=1, min_count=1).max()}")
                print(f"min of data-quality (approx. 1 is correct): {data_quality.sum(axis=1, min_count=1).min()}")
                print(f"sum of distance_quality: {np.sum(distance_quality)}\n")
                print(f"sorted distance: {sorted_distance}\n")
                print(f"distance_quality: {distance_quality}\n")
                print(f"Data All: \n{data_all}\n")
                print(f"Data mean: \n{data_mean}\n")
                print(f"maximum: \n{maximum}\n")
                print(f"avg_diff: \n{avg_diff[0]}\n")
                print(f"rmse: \n{rmse[0]}\n")
                return data_all, data_mean, index_for_plot, column_name_list, data_to_compare, diff, maximum, avg_diff, rmse[0], data_density
            else:
                sorted_distance = np.sort(self.distance[0], axis=0)[1:self.k_factor + 1]
                print(sorted_distance)
                distance_quality = (1 - sorted_distance / np.sum(sorted_distance)) / (self.k_factor - 1)
                print(distance_quality)
                mask_for_quality = date_range_df.iloc[:, 1:].notnull()
                print(mask_for_quality)
                quality_mask = mask_for_quality.multiply(distance_quality, fill_value=np.nan).replace({0: np.nan})
                print(quality_mask)
                data_quality = quality_mask.div(quality_mask.sum(axis=1, min_count=1), axis=0)
                print(data_quality)
                data_all = date_range_df
                data_all_distance = data_all.iloc[:, 1:].mul(data_quality)
                data_mean = data_all_distance.sum(axis=1, min_count=1)
                index_for_plot = data_all.index
                index_for_plot = pd.to_datetime(index_for_plot, format='%Y%m%d%H%M')
                print(f"max of data-quality (approx. 1 is correct): {data_quality.sum(axis=1, min_count=1).max()}")
                print(f"max of data-quality (approx. 1 is correct): {data_quality.sum(axis=1, min_count=1).min()}")
                print(f"sum of distance_quality: {np.sum(distance_quality)}\n")
                print(f"distance_quality: {distance_quality}\n")
                print(f"Data All: \n{data_all}\n")
                print(f"Data Mean: \n{data_mean}\n")
                return data_all, data_mean, index_for_plot, column_name_list
        else:
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
                date_range_df.update(df_tt_10)
                counter = counter + 1
            if compare_n_avg:
                data_all = date_range_df
                data_to_compare = data_all[compare_station]
                data_all = data_all.drop([compare_station], axis=1)
                data_mean = data_all.mean(axis=1)
                diff = (data_mean - data_to_compare).abs()
                diff_sqr = (data_mean - data_to_compare)**2
                rmse = np.sqrt(np.full((len(diff_sqr)), diff_sqr.sum()/(len(diff_sqr)-diff_sqr.isna().sum())))
                maximum = diff.max()
                avg_diff = np.full((len(diff)), diff.sum()/(len(diff)-diff.isna().sum()))
                mask_for_quality = date_range_df.iloc[:, 2:].notnull()
                data_number = mask_for_quality.multiply(1, fill_value=np.nan).replace({0: np.nan})
                data_factor = (data_number.sum(axis=1, min_count=1))/(self.k_factor-1)
                data_density = data_factor.sum()/(len(data_factor) - data_factor.isna().sum())
                print(compare_station)
                # print("here", diff.isna().sum())
                # print(avg_diff)
                index_for_plot = data_all.index
                index_for_plot = pd.to_datetime(index_for_plot, format='%Y%m%d%H%M')
                # print(f"Data All: \n{data_all}\n")
                # print(f"Data mean: \n{data_mean}\n")
                # print(f"maximum: \n{maximum}\n")
                # print(f"avg_diff: \n{avg_diff[0]}\n")
                # print(f"rmse: \n{rmse[0]}\n")
                # print(f"density: \n{data_density}\n")
                return data_all, data_mean, index_for_plot, column_name_list, data_to_compare, diff, maximum, avg_diff, rmse[0], data_density
            else:
                data_all = date_range_df
                data_mean = date_range_df.mean(axis=1)
                index_for_plot = data_all.index
                index_for_plot = pd.to_datetime(index_for_plot, format='%Y%m%d%H%M')
                print(f"Data All: \n{data_all}\n")
                print(f"Data mean: \n{data_mean}\n")
            return data_all, data_mean, index_for_plot, column_name_list

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

    def find_near(self, direction=False):
        """
        :Description: Will find all the near stations around your location.

        :return: x_near, y_near, z_near, activ_near_id: **as array - activ_near_id as list**
        """
        if direction:
            looking_for_gebreite = self.station_list[self.activ_id[self.closest[:, 1:self.k_factor + 1][0][0]]].get_geobreite()
            looking_for_geolaenge = self.station_list[self.activ_id[self.closest[:, 1:self.k_factor + 1][0][0]]].get_geolaenge()
            q_1 = []
            q_2 = []
            q_3 = []
            q_4 = []
            q_ges = []
            for i in self.closest[:, 1:][0]:
                station_geolaenge = self.station_list[self.activ_id[i]].get_geolaenge()
                station_geobreite = self.station_list[self.activ_id[i]].get_geobreite()
                if station_geolaenge > looking_for_geolaenge and station_geobreite > looking_for_gebreite:
                    q_1.append(i)
                elif station_geolaenge < looking_for_geolaenge and station_geobreite > looking_for_gebreite:
                    q_2.append(i)
                elif station_geolaenge < looking_for_geolaenge and station_geobreite < looking_for_gebreite:
                    q_3.append(i)
                elif station_geolaenge > looking_for_geolaenge and station_geobreite < looking_for_gebreite:
                    q_4.append(i)
                else:
                    pass
            for m in range(0,len(self.closest[:, 1:][0]),1):
                if m >= len(q_1):
                    pass
                else:
                    q_ges.append(q_1[m])
                if m >= len(q_2):
                    pass
                else:
                    q_ges.append(q_2[m])
                if m >= len(q_3):
                    pass
                else:
                    q_ges.append(q_3[m])
                if m >= len(q_4):
                    pass
                else:
                    q_ges.append(q_4[m])
            x_near = np.array([])
            y_near = np.array([])
            z_near = np.array([])
            activ_near_id = []
            for i in range(0,self.k_factor,1):
                x_i = self.x_active[q_ges[i]:q_ges[i] + 1]
                y_i = self.y_active[q_ges[i]:q_ges[i]  + 1]
                z_i = self.z_active[q_ges[i]:q_ges[i]  + 1]
                x_near = np.append(x_near, x_i)
                y_near = np.append(y_near, y_i)
                z_near = np.append(z_near, z_i)
                activ_near_id.append(self.activ_id[q_ges[i]])
            return x_near, y_near, z_near, activ_near_id
        else:
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

    def datapath_near(self, direction=False, analyze=False, machine_learning=False, looking_for="TT_10"):
        """
        :Description: Is getting all the paths for data of all the near stations in timedelta. Also creating a list with the columnnames for your DataFrame

        :return: datapath_near_list, column_names_list, column_name_list: **all as list**
        """
        datapath_near_list = []
        column_names_list = []
        column_name_list = []
        counter = 0
        my_bool = True
        if direction:
            looking_for_gebreite = self.station_list[self.activ_id[self.closest[:, 1:self.k_factor + 1][0][0]]].get_geobreite()
            looking_for_geolaenge = self.station_list[self.activ_id[self.closest[:, 1:self.k_factor + 1][0][0]]].get_geolaenge()
            q_1 = []
            q_2 = []
            q_3 = []
            q_4 = []
            q_ges = []
            for i in self.closest[:, 1:][0]:
                station_geolaenge = self.station_list[self.activ_id[i]].get_geolaenge()
                station_geobreite = self.station_list[self.activ_id[i]].get_geobreite()
                if station_geolaenge > looking_for_geolaenge and station_geobreite > looking_for_gebreite:
                    q_1.append(i)
                elif station_geolaenge < looking_for_geolaenge and station_geobreite > looking_for_gebreite:
                    q_2.append(i)
                elif station_geolaenge < looking_for_geolaenge and station_geobreite < looking_for_gebreite:
                    q_3.append(i)
                elif station_geolaenge > looking_for_geolaenge and station_geobreite < looking_for_gebreite:
                    q_4.append(i)
                else:
                    pass
            for m in range(0,len(self.closest[:, 1:][0]),1):
                if m >= len(q_1):
                    pass
                else:
                    q_ges.append(q_1[m])
                if m >= len(q_2):
                    pass
                else:
                    q_ges.append(q_2[m])
                if m >= len(q_3):
                    pass
                else:
                    q_ges.append(q_3[m])
                if m >= len(q_4):
                    pass
                else:
                    q_ges.append(q_4[m])
            datapath_near_list.append(self.station_list[self.activ_id[self.closest[:, 1:][0][0]]].generate_tu_data_path_date(self.start_date, self.end_date))
            column_name_list.append(self.activ_id[self.closest[:, 1:][0][0]])
            for s in range(len(datapath_near_list[counter])):
                column_names_list.append(self.activ_id[self.closest[:, 1:self.k_factor + 1][0][0]])
            for k in range(0,self.k_factor,1):
                r = q_ges[k]
                if self.activ_id[r] == "Find near TU for me":
                    pass
                else:
                    datapath_near_list.append(self.station_list[self.activ_id[r]].generate_tu_data_path_date(self.start_date, self.end_date))
                    column_name_list.append(self.activ_id[r])
                    for j in range(len(datapath_near_list[counter])):
                        column_names_list.append(self.activ_id[r])
                    counter = counter + 1
            return datapath_near_list, column_names_list, column_name_list
        elif analyze:
            datapath_near_list.append(self.station_list[self.activ_id[self.closest[:, 1:2][0][0]]].generate_tu_data_path_date(self.start_date, self.end_date))
            column_name_list.append(self.activ_id[self.closest[:, 1:2][0][0]])
            for j in range(len(datapath_near_list[counter])):
                column_names_list.append(self.activ_id[self.closest[:, 1:2][0][0]])
            return datapath_near_list, column_names_list, column_name_list

        elif machine_learning:
            looking_for_gebreite = self.station_list[self.activ_id[self.closest[:, 1:self.k_factor + 1][0][0]]].get_geobreite()
            looking_for_geolaenge = self.station_list[self.activ_id[self.closest[:, 1:self.k_factor + 1][0][0]]].get_geolaenge()
            q_1 = []
            q_2 = []
            q_3 = []
            q_4 = []
            q_ges = []
            for i in self.closest[:, 1:][0]:
                station_geolaenge = self.station_list[self.activ_id[i]].get_geolaenge()
                station_geobreite = self.station_list[self.activ_id[i]].get_geobreite()
                if station_geolaenge > looking_for_geolaenge and station_geobreite > looking_for_gebreite:
                    q_1.append(i)
                elif station_geolaenge < looking_for_geolaenge and station_geobreite > looking_for_gebreite:
                    q_2.append(i)
                elif station_geolaenge < looking_for_geolaenge and station_geobreite < looking_for_gebreite:
                    q_3.append(i)
                elif station_geolaenge > looking_for_geolaenge and station_geobreite < looking_for_gebreite:
                    q_4.append(i)
                else:
                    pass
            for m in range(0, len(self.closest[:, 1:][0]), 1):
                if m >= len(q_1):
                    pass
                else:
                    q_ges.append(q_1[m])
                if m >= len(q_2):
                    pass
                else:
                    q_ges.append(q_2[m])
                if m >= len(q_3):
                    pass
                else:
                    q_ges.append(q_3[m])
                if m >= len(q_4):
                    pass
                else:
                    q_ges.append(q_4[m])

            count_loop = 0
            count_station = 0
            while count_station < self.k_factor:
                if count_loop == 0:
                    i = self.closest[:, 1:self.k_factor + 1 + count_loop][0][count_loop]
                else:
                    i = q_ges[count_loop]
                test = self.station_list[self.activ_id[i]].generate_tu_data_path_date(self.start_date, self.end_date)
                date_range_df = pd.DataFrame([])
                date_range_df = self.date_range_df().set_index('MESS_DATUM_GENERATED')
                date_range_df.loc[:, str(self.activ_id[i])] = np.nan
                for j in test:
                    df_tt_10 = pd.read_csv(j, sep=";", usecols=["MESS_DATUM", looking_for], index_col=["MESS_DATUM"])
                    mask = df_tt_10[looking_for] > -999
                    df_tt_10 = df_tt_10[mask]
                    df_tt_10 = df_tt_10.rename(columns={looking_for: self.activ_id[i]})
                    date_range_df.update(df_tt_10)
                if date_range_df.isna().sum()[1] > len(date_range_df) * 0.5 and count_loop == 0:
                    my_bool = False
                elif date_range_df.isna().sum()[1] > len(date_range_df) * 0.5:
                    pass
                else:
                    datapath_near_list.append(self.station_list[self.activ_id[i]].generate_tu_data_path_date(self.start_date, self.end_date))
                    column_name_list.append(self.activ_id[i])
                    for j in range(len(datapath_near_list[counter])):
                        column_names_list.append(self.activ_id[i])
                    counter = counter + 1
                    count_station += 1
                count_loop += 1
            return datapath_near_list, column_names_list, column_name_list, my_bool

            # for i in self.closest[:, 1:self.k_factor + 1][0]:
            #     datapath_near_list.append(self.station_list[self.activ_id[i]].generate_tu_data_path_date(self.start_date, self.end_date))
            #     column_name_list.append(self.activ_id[i])
            #     for j in range(len(datapath_near_list[counter])):
            #         column_names_list.append(self.activ_id[i])
            #     counter = counter + 1


        else:
            my_bool = True
            for i in self.closest[:, 1:self.k_factor + 1][0]:
                datapath_near_list.append(self.station_list[self.activ_id[i]].generate_tu_data_path_date(self.start_date, self.end_date))
                column_name_list.append(self.activ_id[i])
                for j in range(len(datapath_near_list[counter])):
                    column_names_list.append(self.activ_id[i])
                counter = counter + 1
            return datapath_near_list, column_names_list, column_name_list, my_bool

    def dataframe_near_from_to(self, direction=False, analyze=False, machine_learning=False, looking_for="TT_10"):
        """
        :Description: Is generating a DataFrame with alle the dates inside your files (timedelta for every file) inside your timedelta. Also returning same lists from self.datapath_near()

        :return: df_from_to, datapath_near_list, column_names_list, column_name_list: **as list, df_from_to as DataFrame**
        """
        df_from = pd.DataFrame([])
        df_to = pd.DataFrame([])
        if direction:
            datapath_near_list, column_names_list, column_name_list, my_bool = self.datapath_near(direction=True)
        elif analyze:
            datapath_near_list, column_names_list, column_name_list, my_bool = self.datapath_near(direction=False, analyze=True)
        elif machine_learning:
            datapath_near_list, column_names_list, column_name_list, my_bool = self.datapath_near(direction=False, analyze=False, machine_learning=True, looking_for=looking_for)
        else:
            datapath_near_list, column_names_list, column_name_list, my_bool = self.datapath_near(direction=False)
        if my_bool:
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
        else:
            df_from_to = False
        return df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool

    def dataframe_near_from_to_path(self, direction=False, analyze=False, machine_learning=False, looking_for="TT_10"):
        """
        :Description: Is connecting df_from_to with datapah_near_list for easier handling.

        :return: df_from_to, column_names_list, column_name_list: **as list, df_from_to as DataFrame**
        """
        if direction:
            df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool = self.dataframe_near_from_to(direction=True)
        elif analyze:
            df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool = self.dataframe_near_from_to(direction=False, analyze=True)
        elif machine_learning:
            df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool = self.dataframe_near_from_to(direction=False, machine_learning=True, looking_for=looking_for)
        else:
            df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool = self.dataframe_near_from_to(direction=False)
        if my_bool:
            free_list = []
            for i in range(len(datapath_near_list)):
                for j in datapath_near_list[i]:
                    free_list.append(j)
            df_data_path = pd.DataFrame(free_list, columns=["DATA_PATH"])
            df_from_to = df_from_to.join(df_data_path["DATA_PATH"])
        else:
            pass
        return df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool

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

    def average_for_coordinate(self, data_looking_for="TT_10", qn_weight_n_avg=False, distance_weight_n_avg=False, qn_distance_weight_n_avg=False, direction_n_avg=False, compare_n_avg=False, compare_station=None):
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
            df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool = self.dataframe_near_from_to_path()
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
            df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool = self.dataframe_near_from_to_path()
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
                print(data_quality)
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
        elif direction_n_avg:
            print("direction_method")
            date_range_df = self.date_range_df().set_index('MESS_DATUM_GENERATED')
            df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool = self.dataframe_near_from_to_path(direction=True)
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
                print(data_all)
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
                data_factor = (data_number.sum(axis=1, min_count=1))/(self.k_factor)
                data_density = data_factor.sum()/(len(data_factor) - data_factor.isna().sum())
                print(compare_station)
                # print("here", diff.isna().sum())
                # print(avg_diff)
                index_for_plot = data_all.index
                index_for_plot = pd.to_datetime(index_for_plot, format='%Y%m%d%H%M')
                print(f"Data to compare: \n{data_to_compare}\n")
                print(f"Data All: \n{data_all}\n")
                print(f"Data mean: \n{data_mean}\n")
                print(f"maximum: \n{maximum}\n")
                print(f"avg_diff: \n{avg_diff[0]}\n")
                print(f"rmse: \n{rmse[0]}\n")
                print(f"density: \n{data_density}\n")
                return data_all, data_mean, index_for_plot, column_name_list, data_to_compare, diff, maximum, avg_diff, rmse[0], data_density
            else:
                data_all = date_range_df
                data_mean = date_range_df.mean(axis=1)
                index_for_plot = data_all.index
                index_for_plot = pd.to_datetime(index_for_plot, format='%Y%m%d%H%M')
                print(f"Data All: \n{data_all}\n")
                print(f"Data mean: \n{data_mean}\n")
            return data_all, data_mean, index_for_plot, column_name_list
        else:
            date_range_df = self.date_range_df().set_index('MESS_DATUM_GENERATED')
            df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool = self.dataframe_near_from_to_path()
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

    def analyze_data(self, data_looking_for="TT_10", correlation=True, compare_station=""):
        if correlation:
            print("correlation")
            date_range_df = self.date_range_df().set_index('MESS_DATUM_GENERATED')
            df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool = self.dataframe_near_from_to_path(direction=False, analyze=True)
            for i in column_name_list:
                date_range_df.loc[:, str(i)] = np.nan
            for i in df_from_to["DATA_PATH"]:
                df_tt_10 = pd.read_csv(i, sep=";", usecols=["MESS_DATUM", data_looking_for], index_col=["MESS_DATUM"])
                mask = df_tt_10[data_looking_for] > -999
                df_tt_10 = df_tt_10[mask]
                my_new_name = f"{column_names_list[0]}_{data_looking_for}"
                print(my_new_name)
                df_tt_10 = df_tt_10.rename(columns={data_looking_for: column_names_list[0]})
                date_range_df.update(df_tt_10)
                data_all = date_range_df
                data_all = data_all.drop(["DATA_SUMM"], axis=1)
                mask_for_quality = data_all.iloc[:, 0:].notnull()
                data_number = mask_for_quality.multiply(1, fill_value=np.nan).replace({0: np.nan})
                data_factor = (data_number.sum(axis=1, min_count=1))
                data_density = data_factor.sum() / len(data_factor)
                index_for_plot = data_all.index
                index_for_plot = pd.to_datetime(index_for_plot, format='%Y%m%d%H%M')
                data_all = data_all.rename(columns={column_names_list[0]: my_new_name})
                # print(f"Data All: \n{data_all}\n")
                print(f"density: \n{data_density}\n")
                return data_all, column_name_list[0], data_density
        else:
            print("prep data")
            date_range_df = self.date_range_df().set_index('MESS_DATUM_GENERATED')
            df_from_to, datapath_near_list, column_names_list, column_name_list, my_bool = self.dataframe_near_from_to_path(direction=False, machine_learning=True, looking_for=data_looking_for)
            column_names_list_2 = []
            for names in column_names_list:
                column_names_list_2.append(f"{names}_{data_looking_for}")
            if my_bool:
                counter = 0
                for i in column_names_list_2:
                    date_range_df.loc[:, str(i)] = np.nan
                for i in df_from_to["DATA_PATH"]:
                    df_tt_10 = pd.read_csv(i, sep=";", usecols=["MESS_DATUM", data_looking_for], index_col=["MESS_DATUM"])
                    mask = df_tt_10[data_looking_for] > -999
                    df_tt_10 = df_tt_10[mask]
                    df_tt_10 = df_tt_10.rename(columns={data_looking_for: f"{column_names_list[counter]}_{data_looking_for}"})
                    date_range_df.update(df_tt_10)
                    counter = counter + 1
                data_all = date_range_df
                mask_for_quality = date_range_df.iloc[:, 2:].notnull()
                data_number = mask_for_quality.multiply(1, fill_value=np.nan).replace({0: np.nan})
                data_factor = (data_number.sum(axis=1, min_count=1))/(self.k_factor-1)
                data_density = data_factor.sum()/(len(data_factor) - data_factor.isna().sum())
                index_for_plot = data_all.index
                index_for_plot = pd.to_datetime(index_for_plot, format='%Y%m%d%H%M')
                station_names = data_all.columns.values[1:]
                gebreite_list = []
                geolaenge_list = []
                geohoehe_list = []

                for i in station_names:
                    i = i.replace(f"_{data_looking_for}", "")
                    geobreite = self.station_list[i].get_geobreite()
                    geolaenge = self.station_list[i].get_geolaenge()
                    geohoehe = self.station_list[i].get_stationshoehe()
                    gebreite_list.append(geobreite)
                    geolaenge_list.append(geolaenge)
                    geohoehe_list.append(geohoehe)
                dist = []
                for n in range(0,len(gebreite_list),1):
                    dist_1 = (gebreite_list[0], geolaenge_list[0])
                    dist_2 = (gebreite_list[n], geolaenge_list[n])
                    dist.append(distance.euclidean(dist_1, dist_2))
                return data_all, index_for_plot, column_name_list, data_density, dist, geohoehe_list, my_bool
            else:
                return False, False, False, False, False, False, my_bool


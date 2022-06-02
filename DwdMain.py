from DwdDataScrapper import DataScrapper
from DwdDataPrep import Reader, Writer
from DwdNearNeighbor import NearNeighbor
from DwdPlotter import PlotterForStations, PlotterForData
from DwdDict import get_dwd_dict
import numpy as np
import json
from datetime import datetime


class DwdMain:
    """
    :Description: Compressing all the modules into one module for easier use.
    """
    def __init__(self, external_domain,
                 external_path_global,
                 local_domain,
                 type_of_data,
                 type_of_time,
                 type_dict,
                 load_txt_dict,
                 rest_dict,
                 ending=None,
                 start_date=None,
                 end_date=None,
                 compare_station=None,
                 x_coordinate=None,
                 y_coordinate=None,
                 z_coordinate=None,
                 k_factor=None,
                 looking_for=None,
                 type_of_time_list=None,
                 type_of_data_list=None,
                 unit_dict=None,
                 title_dict=None):
        """
        :param external_domain: **as string**. Choose the domain.
        :param external_path_global: **as string**.  Choose the path inside this domain.
        :param local_domain: **as string**. Choose your local domain.
        :param type_of_data: **as string**. Choose the type of data
        :param type_of_time: **as string**. Choose the type of time
        :param type_dict: **as dict**. Should be the dictionary from DwdDict.py type_dict.
        :param load_txt_dict: **as dict**. Should be the dictionary from DwdDict.py load_txt_dict.
        :param rest_dict: **as dict**. Should be the dictionary from DwdDict.py rest_dict.
        :param ending: **as list**. Should be the list from DwdDict.py ending.
        :param start_date: **as int**. YYYYMMDDHHMM. Your start date.
        :param end_date: **as int**. YYYYMMDDHHMM. Your end date.
        :param compare_station: **as string**. Only if you want to compare your calculation with a station.
        :param x_coordinate: **as float**. X-coordinates for your chosen location.
        :param y_coordinate: **as float**. Y-coordinates for your chosen location.
        :param z_coordinate: **as float**. Z-coordinates for your chosen location. (Can be skipped for now, maybe important in the future)
        :param k_factor: **as int**. How many station are you looking around your location?
        :param looking_for: **as list**. What data you want to plot?
        :param type_of_time_list: **as list**. Should be from DwdDict.py type_of_time_list.
        :param type_of_data_list: **as list**. Should be from DwdDict.py type_of_data_list.
        :param unit_dict: **as dict**. Should be from DwdDict.py unit_dict.
        :param title_dict: **as dict**. Should be from DwdDict.py title_dict.
        """
        self.external_domain = external_domain
        self.external_path_global = external_path_global
        self.local_domain = local_domain
        self.ending = ending
        self.type_of_data = type_of_data
        self.type_of_time = type_of_time
        self.type_dict = type_dict
        self.load_txt_dict = load_txt_dict
        self.rest_dict = rest_dict
        self.start_date = start_date
        self.end_date = end_date
        self.compare_station = compare_station
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.z_coordinate = z_coordinate
        self.k_factor = k_factor
        if start_date == None:
            pass
        else:
            self.start_date_datetime = datetime.strptime(str(self.start_date), "%Y%m%d%H%M")
            self.end_date_datetime = datetime.strptime(str(self.end_date), "%Y%m%d%H%M")
        self.load_txt, self.local_path, self.external_path, self.data_type = self.__main_path_loader(self.type_of_data, self.type_of_time)
        self.looking_for = looking_for
        self.type_of_time_list = type_of_time_list
        self.type_of_data_list = type_of_data_list
        self.unit_dict = unit_dict
        self.title_dict = title_dict
        self.reader = Reader(path_to_txt=self.load_txt,
                             local_path=self.local_path,
                             data_type=self.data_type)

    def __transfrom_compare_station(self, compare_station):
        """
        :Description: Will create a prefix for your station. Example: "00003" --> "TU_00003"

        :param compare_station: **as string**. The number of your station.
        :return: compare_station_t **as string**
        """
        compare_station_t = self.type_dict[self.type_of_data] + "_" + compare_station
        return compare_station_t

    def __main_path_loader(self, type_of_data, type_of_time=None, for_scrapping=False):
        """
        :Description: Will generate the information-txt local path, external path and the prefix (data type)

        :param type_of_data: *+as string**. Example: "air_temperature".
        :param type_of_time: **as string**.  Example: "recent".
        :param for_scrapping: **as Boolean**. If it is for DataScrapper, set True
        :return: load_txt, local_path, external_path, data_type (**all as string**)
        """
        if for_scrapping:
            external_path = self.external_path_global + type_of_data + "/"
            return external_path
        else:
            load_txt = self.local_domain + self.external_path_global + type_of_data + "/" + type_of_time + "/" + self.rest_dict[type_of_time] + self.load_txt_dict[type_of_data] + "_Beschreibung_Stationen.txt"
            local_path = self.local_domain + self.external_path_global + type_of_data + "/" + type_of_time + "/extracted_files/"
            external_path = self.external_path_global + type_of_data + "/"
            data_type = self.type_dict[type_of_data]
            return load_txt, local_path, external_path, data_type

    def main_datascrapper(self, all=False):
        """
        :Description: Is the main-methode for DataScrapper.py the data. Check the DwdDataScrapper module for more information

        :param all: **as Boolean**. If all==True, it will download all the data from DwdDict.py type_of_data_list.
        :return: None
        """
        # looking_for = ".zip"
        if all:
            for i in self.type_of_data_list:
                DataScrapper(external_domain=self.external_domain,
                             external_path=self.__main_path_loader(i, for_scrapping=True),
                             local_domain=self.local_domain,
                             ending=self.ending).main_update_data()
        else:
            DataScrapper(external_domain=self.external_domain,
                         external_path=self.external_path,
                         local_domain=self.local_domain,
                         ending=self.ending).main_update_data()

    def main_writer(self, type_of_data_list=None, type_of_time_list=None, all=False):
        """
        :Description: Is the main-methode for DwdDataPrep.py class Writer. Check the DwdDataPrep module for more information

        :param type_of_data_list: **as list**.
        :param type_of_time_list: **as list**.
        :param all: **as Boolean**. If all==True, it will write all the data from DwdDict.py type_of_data_list and type_of_time_list. Else you can give your own lists.
        :return: "data written" if succeeded.
        """
        if all:
            for i in range(len(self.type_of_data_list)):
                for j in range(len(self.type_of_time_list)):
                    print("writing..." + " " + self.type_of_data_list[i] + " " + self.type_of_time_list[j])
                    load_txt, local_path, external_path, data_type = self.__main_path_loader(self.type_of_data_list[i], self.type_of_time_list[j])
                    Writer(local_path=local_path,
                           path_to_txt=load_txt,
                           data_type=data_type).write_stations_paths()
        else:
            if type_of_data_list:
                for i in range(len(type_of_data_list)):
                    if type_of_time_list:
                        for j in range(len(type_of_time_list)):
                            print("writing..." + " " + type_of_data_list[i] + " " + type_of_time_list[j])
                            load_txt, local_path, external_path, data_type = self.__main_path_loader(type_of_data_list[i], type_of_time_list[j])
                            Writer(local_path=local_path,
                                   path_to_txt=load_txt,
                                   data_type=data_type).write_stations_paths()
                    else:
                        for j in range(len(self.type_of_time_list)):
                            print("writing... " + type_of_data_list[i] + " " + self.type_of_time_list[j])
                            load_txt, local_path, external_path, data_type = self.__main_path_loader(type_of_data_list[i], self.type_of_time_list[j])
                            Writer(local_path=local_path,
                                   path_to_txt=load_txt,
                                   data_type=data_type).write_stations_paths()
        return print("data written")

    def __main_data_prep(self):
        """
        :Description: Calling the method DataPrep.Reader(...).data_prep_for_new_location() and creating zip_data_active_in_date (zipped x_coordinates and y_coordinates in timedelta).

        :return: x_active_in_date, y_active_in_date, z_active_in_date, zip_data_active_in_date, activ_id_in_date, station_list
        """
        x_active_in_date, y_active_in_date, z_active_in_date, activ_id_in_date, station_list = self.reader.data_prep_for_new_location(start_date=self.start_date,
                                                                                                                                      end_date=self.end_date,
                                                                                                                                      x_coordinate=self.x_coordinate,
                                                                                                                                      y_coordinate=self.y_coordinate,
                                                                                                                                      z_coordinate=self.z_coordinate)

        zip_data_active_in_date = np.around(np.array(list(zip(x_active_in_date, y_active_in_date))), decimals=4)
        return x_active_in_date, y_active_in_date, z_active_in_date, zip_data_active_in_date, activ_id_in_date, station_list

    def __main_nearneighbor(self, look_for="TT_10", qn_weight_n=False, distance_weight_n=False, compare_n=False, no_plot_n=False):
        """
        :Description: Calling the method from DwdNearNeigbor.DwdNearNeighbor(...).average_for_coordinate(...) and return this.

        :param look_for: **as string**. The type of data you are looking for (Example: "TT_10".
        :param qn_weight_n: **as Boolean**. If qn_weight_n == True it will weight the quality of data for the calculations.
        :param distance_weight_n: **as Boolean**. If distance_weight_n == True it will weight the distance for the calculations.
        :param compare_n:  **as Boolean**.  If you want to compare, how accurate your methods are, set True and choose coordinates for a station.
        :param no_plot_n: **as Boolean**. If you want to see just the result, without the plot (saves a bit of time), you can set this True.
        :return: DwdNearNeigbor.DwdNearNeighbor(...).average_for_coordinate(...)
        """
        x_active_in_date, y_active_in_date, z_active_in_date, zip_data_active_in_date, activ_id_in_date, station_list = self.__main_data_prep()
        nearneighbor = NearNeighbor(zip_data_active=zip_data_active_in_date,
                                    x_active=x_active_in_date,
                                    y_active=y_active_in_date,
                                    z_active=z_active_in_date,
                                    k_factor=self.k_factor,
                                    start_date=self.start_date,
                                    end_date=self.end_date,
                                    activ_id=activ_id_in_date,
                                    station_list=station_list)
        return nearneighbor.average_for_coordinate(data_looking_for=look_for, qn_weight_n_avg=qn_weight_n, distance_weight_n_avg=distance_weight_n, compare_n_avg=compare_n, compare_station=self.compare_station)

    def __main_plotter_for_data(self, data_all, data_mean, index_for_plot, column_name_list, plot_name, compare=False, no_plot=False, data_to_compare=None, diff=None, maximum=None, avg_diff=None, type_of_method="Durchschnitt"):
        """
        :Description: Calling the method from DwdPlotter.PlotterForData(...).plotting_compare(...) or .plotting_data(...)

        :param data_all: **as DataFrame**.
        :param data_mean: **as DataFrame**. Your calculation (average for example).
        :param index_for_plot: **as list**. The timedelta for x-axes.
        :param column_name_list: as list. Names of plotted lines.
        :param plot_name: as string. Your chosen plot-title.
        :param compare: **as Boolean**. If you want to compare, how accurate your methods are, set True and choose coordinates for a station.
        :param no_plot: **as Boolean**. If you want to see just the result, without the plot (saves a bit of time), you can set this True.
        :param data_to_compare: **as DataFrame**. The real data of a station.
        :param diff: **as DataFrame**. The difference between your calculation and real data of a station.
        :param maximum: **as int**. Maximum difference.
        :param avg_diff: **as array**. Average difference. (Will plot a constant line).
        :param type_of_method: **as string**. Name of your calculation method.
        :return: “plot saved” if succeeded.
        """
        plotter = PlotterForData(data_all=data_all,
                                 data_mean=data_mean,
                                 index_for_plot=index_for_plot,
                                 column_name_list=column_name_list,
                                 start_date_datetime=self.start_date_datetime,
                                 end_date_datetime=self.end_date_datetime,
                                 plot_name=plot_name,
                                 k_factor=self.k_factor,
                                 x_coordinate=self.x_coordinate,
                                 y_coordinate=self.y_coordinate,
                                 type_of_data=self.type_of_data,
                                 unit_dict=self.unit_dict,
                                 title_dict=self.title_dict)
        if compare:
            if no_plot:
                pass
            else:
                plotter.plotting_compare(compare_station=self.compare_station, data_to_compare=data_to_compare, diff=diff, maximum=maximum, avg_diff=avg_diff, type_of_method=type_of_method)
        else:
            plotter.plotting_data(type_of_method=type_of_method)

    def main_plotter_stations(self, projection=False):
        """
        :Description: Calling the method from DwdPlotter.PlotterForStations(...).plotting_3d(...) and .plotting_height_2d()

        :param projection: **as Boolean**. If projection==True, it will project the height of the stations.
        :return: two times “plot saved” if succeeded.
        """

        x_active, y_active, z_active, active_id, x_not_active, y_not_active, z_not_active, not_activ_id, x_no_data, y_no_data, z_no_data, no_data_id = self.reader.get_active_stations()
        PlotterForStations(x_active, y_active, z_active, type_of_data=self.type_of_data).plotting_3d(projection)
        PlotterForStations(x_active, y_active, z_active, type_of_data=self.type_of_data).plotting_height_2d()

    def main_data_map(self):
        """
        :Description: Will create some json files, with active stations, not activ stations, activ stations without data and the near station for your location and your timedelta

        :return: "zipped_data_for_active_map" if succeeded.
        """
        x_active, y_active, z_active, active_id, x_not_active, y_not_active, z_not_active, not_activ_id, x_no_data, y_no_data, z_no_data, no_data_id = self.reader.get_active_stations()
        x_active_in_date, y_active_in_date, z_active_in_date, zip_data_active_in_date, activ_id_in_date, station_list = self.__main_data_prep()
        x_near, y_near, z_near, activ_near_id = NearNeighbor(zip_data_active=zip_data_active_in_date,
                                                             x_active=x_active_in_date,
                                                             y_active=y_active_in_date,
                                                             z_active=z_active_in_date,
                                                             k_factor=self.k_factor,
                                                             start_date=self.start_date,
                                                             end_date=self.end_date,
                                                             activ_id=activ_id_in_date,
                                                             station_list=station_list).find_near()
        with open(self.local_domain + r"DWD_Project/MapCreator/" + r"zip_data_near.json", "w") as f:
            json.dump(np.array(list(zip(x_near, y_near, activ_near_id))).tolist(), f, indent=2)
        with open(self.local_domain + r"DWD_Project/MapCreator/" + r"zip_data_active_in_date.json", "w") as f:
            json.dump(np.array(list(zip(x_active_in_date, y_active_in_date, activ_id_in_date))).tolist(), f, indent=2)
        with open(self.local_domain + r"DWD_Project/MapCreator/" + r"zip_data_activ.json", "w") as f:
            json.dump(np.array(list(zip(x_active, y_active, active_id))).tolist(), f, indent=2)
        with open(self.local_domain + r"DWD_Project/MapCreator/" + r"zip_data_not_activ.json", "w") as f:
            json.dump(np.array(list(zip(x_not_active, y_not_active, not_activ_id))).tolist(), f, indent=2)
        with open(self.local_domain + r"DWD_Project/MapCreator/" + r"zip_no_data.json", "w") as f:
            json.dump(np.array(list(zip(x_no_data, y_no_data, no_data_id))).tolist(), f, indent=2)
        with open(self.local_domain + r"DWD_Project/MapCreator/" + r"config.json", "w") as f:
            json.dump((self.x_coordinate, self.y_coordinate, self.local_domain), f, indent=2)
        return print("zipped_data_for_active_map")

    def main_plotter_data(self, qn_weight=False, distance_weight=False, compare=False, no_plot=False):
        """
        :Description: Compressed method for plotting. qn_weight, distance_weight are the methods. If both are False, it will make simple average method.

        :param qn_weight: **as Boolean**. If True weight the quality of data.
        :param distance_weight: **as Boolean**. If True weight the distance of data.
        :param compare: **as Boolean**. If you want to compare, how accurate your methods are, set True and choose coordinates for a station.
        :param no_plot: **as Boolean**. If you want to see just the result, without the plot (saves a bit of time), you can set this True.
        :return: calculations and graphs ("plot saved")
        """

        for i in self.looking_for:
            if qn_weight:
                if compare:
                    data_all_n, data_mean_n, index_for_plot_n, column_name_list_n, data_to_compare_n, diff_n, maximum_n, avg_diff_n = self.__main_nearneighbor(i, qn_weight_n=qn_weight, distance_weight_n=distance_weight, compare_n=compare, no_plot_n=no_plot)
                    self.__main_plotter_for_data(data_all=data_all_n,
                                                 data_mean=data_mean_n,
                                                 index_for_plot=index_for_plot_n,
                                                 column_name_list=column_name_list_n,
                                                 plot_name=i,
                                                 compare=compare,
                                                 no_plot=no_plot,
                                                 data_to_compare=data_to_compare_n,
                                                 diff=diff_n,
                                                 maximum=maximum_n,
                                                 avg_diff=avg_diff_n,
                                                 type_of_method="Gewichteter Durchschnitt (QN-Abh.)")
                else:
                    data_all_n, data_mean_n, index_for_plot_n, column_name_list_n = self.__main_nearneighbor(i,
                                                                                                             qn_weight_n=qn_weight,
                                                                                                             distance_weight_n=distance_weight,
                                                                                                             compare_n=compare,
                                                                                                             no_plot_n=no_plot)
                    self.__main_plotter_for_data(data_all=data_all_n,
                                                 data_mean=data_mean_n,
                                                 index_for_plot=index_for_plot_n,
                                                 column_name_list=column_name_list_n,
                                                 plot_name=i,
                                                 compare=compare,
                                                 no_plot=no_plot,
                                                 type_of_method="Gewichteter Durchschnitt (QN-Abh.)")
            elif distance_weight:
                if compare:
                    data_all_n, data_mean_n, index_for_plot_n, column_name_list_n, data_to_compare_n, diff_n, maximum_n, avg_diff_n = self.__main_nearneighbor(i,
                                                                                                                                                               qn_weight_n=qn_weight,
                                                                                                                                                               distance_weight_n=distance_weight,
                                                                                                                                                               compare_n=compare,
                                                                                                                                                               no_plot_n=no_plot)
                    self.__main_plotter_for_data(data_all=data_all_n,
                                                 data_mean=data_mean_n,
                                                 index_for_plot=index_for_plot_n,
                                                 column_name_list=column_name_list_n,
                                                 plot_name=i,
                                                 compare=compare,
                                                 no_plot=no_plot,
                                                 data_to_compare=data_to_compare_n,
                                                 diff=diff_n,
                                                 maximum=maximum_n,
                                                 avg_diff=avg_diff_n,
                                                 type_of_method="Gewichteter Durchschnitt (Distanzabh.)")
                else:
                    data_all_n, data_mean_n, index_for_plot_n, column_name_list_n = self.__main_nearneighbor(i,
                                                                                                             qn_weight_n=qn_weight,
                                                                                                             distance_weight_n=distance_weight,
                                                                                                             compare_n=compare,
                                                                                                             no_plot_n=no_plot)
                    self.__main_plotter_for_data(data_all=data_all_n,
                                                 data_mean=data_mean_n,
                                                 index_for_plot=index_for_plot_n,
                                                 column_name_list=column_name_list_n,
                                                 plot_name=i,
                                                 compare=compare,
                                                 no_plot=no_plot,
                                                 type_of_method="Gewichteter Durchschnitt (Distanzabh.)")
            else:
                if compare:
                    data_all_n, data_mean_n, index_for_plot_n, column_name_list_n, data_to_compare_n, diff_n, maximum_n, avg_diff_n = self.__main_nearneighbor(i,
                                                                                                                                                               qn_weight_n=qn_weight,
                                                                                                                                                               distance_weight_n=distance_weight,
                                                                                                                                                               compare_n=compare,
                                                                                                                                                               no_plot_n=no_plot)
                    self.__main_plotter_for_data(data_all=data_all_n,
                                                 data_mean=data_mean_n,
                                                 index_for_plot=index_for_plot_n,
                                                 column_name_list=column_name_list_n,
                                                 plot_name=i,
                                                 compare=compare,
                                                 no_plot=no_plot,
                                                 data_to_compare=data_to_compare_n,
                                                 diff=diff_n,
                                                 maximum=maximum_n,
                                                 avg_diff=avg_diff_n,
                                                 type_of_method="Durchschnitt")

                else:
                    data_all_n, data_mean_n, index_for_plot_n, column_name_list_n = self.__main_nearneighbor(i, qn_weight_n=qn_weight, distance_weight_n=distance_weight, compare_n=compare, no_plot_n=no_plot)
                    self.__main_plotter_for_data(data_all=data_all_n,
                                                 data_mean=data_mean_n,
                                                 index_for_plot=index_for_plot_n,
                                                 column_name_list=column_name_list_n,
                                                 plot_name=i,
                                                 compare=compare,
                                                 no_plot=no_plot,
                                                 type_of_method="Durchschnitt")

    def main_station_information(self, station_id):
        """
        :Description: Will return a dict for a station with all the important informations

        :param station_id: **as string**. The stationid with prefix.
        :return: **as dict**
        """
        return self.reader.read_station_list().get(station_id).get_station_informations()

    def main_station_array(self):
        """
        :Description: Will return all the stations for your data type and your time type.

        :return:**as array**
        """
        return self.reader.get_station_ids()

    def main_activ_stations_in_date(self):
        """
        :Description: Will return all the stations for your data type and your time type and your timedelta.

        :return: x_coordinates, y_coordinate, station_ids: **all as array, station_ids as list**
        """
        return self.reader.get_active_stations_in_date(self.start_date, self.end_date)




def main_dwd(local_domain,
             type_of_data,
             type_of_time,
             start_date=None,
             end_date=None,
             compare_station=None,
             x_coordinate=None,
             y_coordinate=None,
             z_coordinate=None,
             k_factor=None,
             looking_for=None):
    """
    :Description: To make your life easier, this grabs all the important informations from DwdDict automatically.

    :param local_domain: **as string**. Choose your local domain.
    :param type_of_data: **as string**. Choose the type of data
    :param type_of_time: **as string**. Choose the type of time
    :param start_date: **as int**. YYYYMMDDHHMM. Your start date.
    :param end_date: **as int**. YYYYMMDDHHMM. Your end date.
    :param compare_station: **as string**. Only if you want to compare your calculation with a station.
    :param x_coordinate: **as float**. X-coordinates for your chosen location.
    :param y_coordinate: **as float**. Y-coordinates for your chosen location.
    :param z_coordinate: **as float**. Z-coordinates for your chosen location. (Can be skipped for now, maybe important in the future)
    :param k_factor: **as int**. How many station are you looking around your location?
    :param looking_for: **as list**. What data you want to plot?
    :return: dwd **as object**
    """
    type_dict, load_txt_dict, rest_dict, title_dict, unit_dict, type_of_time_list, type_of_data_list, external_domain, external_path_global, ending = get_dwd_dict()
    dwd = DwdMain(external_domain=external_domain,
                  external_path_global=external_path_global,
                  local_domain=local_domain,
                  type_of_data=type_of_data,
                  type_of_time=type_of_time,
                  type_dict=type_dict,
                  load_txt_dict=load_txt_dict,
                  rest_dict=rest_dict,
                  ending=ending,
                  start_date=start_date,
                  end_date=end_date,
                  compare_station=compare_station,
                  x_coordinate=x_coordinate,
                  y_coordinate=y_coordinate,
                  z_coordinate=z_coordinate,
                  k_factor=k_factor,
                  looking_for=looking_for,
                  type_of_time_list=type_of_time_list,
                  type_of_data_list=type_of_data_list,
                  unit_dict=unit_dict,
                  title_dict=title_dict)
    return dwd

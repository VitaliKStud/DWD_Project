from DwdDataScrapper import DataScrapper
from DwdDataPrep import Reader, Writer
from DwdNearNeighbor import NearNeighbor
from DwdPlotter import PlotterForStations, PlotterForData
from DwdDict import get_dwd_dict
import numpy as np
import json
from datetime import datetime


class DwdMain:
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
        compare_station_t = self.type_dict[self.type_of_data] + "_" + compare_station
        return compare_station_t

    def __main_path_loader(self, type_of_data, type_of_time=None, for_scarpping=False):
        if for_scarpping:
            external_path = self.external_path_global + type_of_data + "/"
            return external_path
        else:
            load_txt = self.local_domain + self.external_path_global + type_of_data + "/" + type_of_time + "/" + self.rest_dict[type_of_time] + self.load_txt_dict[type_of_data] + "_Beschreibung_Stationen.txt"
            local_path = self.local_domain + self.external_path_global + type_of_data + "/" + type_of_time + "/extracted_files/"
            external_path = self.external_path_global + type_of_data + "/"
            data_type = self.type_dict[type_of_data]
            return load_txt, local_path, external_path, data_type

    def main_datascrapper(self, all=False):
        # looking_for = ".zip"
        if all:
            for i in self.type_of_data_list:
                DataScrapper(external_domain=self.external_domain,
                             external_path=self.__main_path_loader(i, for_scarpping=True),
                             local_domain=self.local_domain,
                             ending=self.ending).main_update_data()
        else:
            DataScrapper(external_domain=self.external_domain,
                         external_path=self.external_path,
                         local_domain=self.local_domain,
                         ending=self.ending).main_update_data()

    def main_writer(self, type_of_data_list=None, type_of_time_list=None, all=False):
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
        x_active_in_date, y_active_in_date, z_active_in_date, activ_id_in_date, station_list = self.reader.data_prep_for_new_location(start_date=self.start_date,
                                                                                                                                      end_date=self.end_date,
                                                                                                                                      x_coordinate=self.x_coordinate,
                                                                                                                                      y_coordinate=self.y_coordinate,
                                                                                                                                      z_coordinate=self.z_coordinate)

        zip_data_active_in_date = np.around(np.array(list(zip(x_active_in_date, y_active_in_date))), decimals=4)
        return x_active_in_date, y_active_in_date, z_active_in_date, zip_data_active_in_date, activ_id_in_date, station_list

    def __main_nearneighbor(self, look_for="TT_10"):
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
        data_all, data_mean, index_for_plot, column_name_list = nearneighbor.average_for_coordinate(data_looking_for=look_for)
        return data_all, data_mean, index_for_plot, column_name_list

    def __main_plotter_for_data(self, data_all, data_mean, index_for_plot, column_name_list, plot_name, compare=False):
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
        if compare == "pltcompare":
            plotter.plotting_compare(compare_station=self.compare_station)
        elif compare == "justcompare":
            data_to_compare, data_mean, diff, maximum, avg_diff, data_all = plotter.compare(compare_station=self.compare_station)
            return maximum, avg_diff
        else:
            plotter.plotting_data()

    def main_plotter_stations(self, projection=False):
        x_active, y_active, z_active, active_id, x_not_active, y_not_active, z_not_active, not_activ_id, x_no_data, y_no_data, z_no_data, no_data_id = self.reader.get_active_stations()
        PlotterForStations(x_active, y_active, z_active, type_of_data=self.type_of_data).plotting_3d(projection)
        PlotterForStations(x_active, y_active, z_active, type_of_data=self.type_of_data).plotting_height_2d()

    def main_data_map(self):
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
        return print("zipped_data_for_active_map")

    def main_plotter_data(self, compare=False):
        if compare == "justcompare":
            for i in self.looking_for:
                data_all, data_mean, index_for_plot, column_name_list = self.__main_nearneighbor(i)
                return self.__main_plotter_for_data(data_all=data_all,
                                                    data_mean=data_mean,
                                                    index_for_plot=index_for_plot,
                                                    column_name_list=column_name_list,
                                                    plot_name=i,
                                                    compare=compare)
        else:
            for i in self.looking_for:
                data_all, data_mean, index_for_plot, column_name_list = self.__main_nearneighbor(i)
                self.__main_plotter_for_data(data_all=data_all,
                                             data_mean=data_mean,
                                             index_for_plot=index_for_plot,
                                             column_name_list=column_name_list,
                                             plot_name=i,
                                             compare=compare)

    def main_station_information(self, station_id):
        return self.reader.read_station_list().get(station_id).get_station_informations()

    def main_station_array(self):
        return self.reader.get_station_ids()

    def main_activ_stations_in_date(self):
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

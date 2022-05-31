import numpy as np
from datetime import datetime, timedelta
import os
from itertools import compress
import json


class Station:
    def __init__(self, stations_array, local_path, data_type):
        self.__data_type = data_type
        self.__stations_id = self.__data_type + "_{:05d}".format(stations_array[0])
        self.__von_datum = self.format_number_to_date(stations_array[1])
        self.__bis_datum = self.format_number_to_date(stations_array[2])
        self.__stationshoehe = stations_array[3]
        self.__geoBreite = stations_array[4]
        self.__geoLaenge = stations_array[5]
        self.__stationsname = stations_array[6]
        self.__bundesland = stations_array[7]
        self.__local_path = local_path

    @staticmethod
    def format_number_to_date(number):
        year = number // 10000
        month = number // 100 - year * 100
        day = number - month * 100 - year * 10000
        date = str(year) + "-" + str(month) + "-" + str(day)
        return date

    def get_local_path(self):
        return self.__local_path

    def get_station_id(self):
        return self.__stations_id

    def get_von_datum(self):
        return self.__von_datum

    def get_bis_datum(self):
        return self.__bis_datum

    def get_stationshoehe(self):
        return self.__stationshoehe

    def get_geobreite(self):
        return self.__geoBreite

    def get_geolaenge(self):
        return self.__geoLaenge

    def get_stationsname(self):
        return self.__stationsname

    def get_bundesland(self):
        return self.__bundesland

    def check_activitiy(self):
        return datetime.now() - datetime.strptime(self.__bis_datum, "%Y-%m-%d") < timedelta(days=10)

    def get_station_informations(self):
        station_information_dict = {"ID": self.__stations_id, "von_datum": self.__von_datum, "bis_datum": self.__bis_datum, "stationshoehe": self.__stationshoehe, "geoBreite": self.__geoBreite,
         "geoLaenge": self.__geoLaenge, "Stationsname": self.__stationsname, "Bundesland": self.__bundesland, "Aktivität": self.check_activitiy()}
        return station_information_dict

    def generate_tu_data_path(self):
        local_list = []
        size = 0
        for i in os.listdir(self.__local_path):
            if self.__stations_id in i:
                size = size + 1
                for j in range(len(os.listdir(self.__local_path + i + "/"))):
                    if ".txt" in self.__local_path + i + "/" + os.listdir(self.__local_path + i + "/")[j]:
                        local_list.append(self.__local_path + i + "/" + os.listdir(self.__local_path + i + "/")[j])
                    else:
                        size = size - 1
            else:
                pass
        if size == 0:
            return 0
        else:
            return local_list

    def check_data(self):
        if self.generate_tu_data_path() == 0:
            return 0
        else:
            return 1

    def generate_tu_date_array(self):
        if self.check_data() == 1:
            tu_data_path = self.generate_tu_data_path()
            from_list = []
            for i in range(len(tu_data_path)):
                if i == len(tu_data_path) - 1:
                    with open(tu_data_path[i], "r") as file:
                        file.readline()
                        first_line = file.readline()
                        for last_line in file:
                            pass
                    from_date = first_line.split(";")[1]
                    to_date = last_line.split(";")[1]
                    from_list.append(int(from_date))
                    from_list.append(int(to_date) + 1)
                else:
                    with open(tu_data_path[i], "r") as file:
                        file.readline()
                        first_line = file.readline()
                    from_date = first_line.split(";")[1]
                    from_list.append(int(from_date))
                file.close()
            return from_list, tu_data_path
        else:
            return 0, 0

    def generate_tu_data_path_date(self, start_date, end_date):
        with open(self.__local_path + r"dict_from_list.json", "r") as f:
            dict_from_list = json.load(f)
        with open(self.__local_path + r"dict_tu_data_path.json", "r") as f:
            dict_tu_data_path = json.load(f)
        from_array = np.array(dict_from_list[self.__stations_id])

        if len(from_array) > 0:
            tu_data_path = dict_tu_data_path[self.__stations_id]
            mask_for_data_path = []
            if end_date < from_array[0]:
                return False
            elif start_date >= from_array[len(from_array) - 1]:
                return False
            else:
                mask_1 = start_date < from_array
                mask_2 = end_date >= from_array
                for i in range(len(from_array)):
                    if i < len(from_array) - 1:
                        mask_for_data_path.append(mask_1[i + 1] & mask_2[i])
                    else:
                        pass
                generate_tu_data_path_date = list(compress(tu_data_path, mask_for_data_path))
            return generate_tu_data_path_date
        else:
            return False

    def check_activ_in_date(self, start_date, end_date):
        with open(self.__local_path + r"dict_from_list.json", "r") as f:
            dict_from_list = json.load(f)
        from_array = np.array(dict_from_list[self.__stations_id])
        if dict_from_list[self.__stations_id] == 0:
            return False
        else:
            if end_date < from_array[0]:
                return False
            elif start_date >= from_array[len(from_array) - 1]:
                return False
            else:
                return True


class Writer:
    def __init__(self, path_to_txt, local_path, data_type):
        self.__path_to_txt = path_to_txt
        self.__local_path = local_path
        self.__data_type = data_type

    def write_stations_paths(self):
        reader = Reader(self.__path_to_txt, self.__local_path, self.__data_type)
        get_station_ids = reader.get_station_ids()
        station_list = reader.read_station_list()
        from_list = []
        tu_data_path = []
        stations_list = []
        for i in get_station_ids:
            from_list_, tu_data_path_ = station_list.get(i).generate_tu_date_array()
            stations_list.append(i)
            from_list.append(from_list_)
            tu_data_path.append(tu_data_path_)
        dict_tu_data_path = dict(zip(stations_list, tu_data_path))
        dict_from_list = dict(zip(stations_list, from_list))
        with open(self.__local_path + r"dict_from_list.json", "w") as f:
            json.dump(dict_from_list, f, sort_keys=True, indent=4)
        with open(self.__local_path + r"dict_tu_data_path.json", "w") as f:
            json.dump(dict_tu_data_path, f, sort_keys=True, indent=4)
        return print("stations_path and stations_date dicts written in: " + self.__local_path)


class Reader:
    def __init__(self, path_to_txt, local_path, data_type):
        self.__path_to_txt = path_to_txt
        self.__local_path = local_path
        self.__data_type = data_type

    def __get_station_headlines(self):
        station_headlines = np.loadtxt(self.__path_to_txt, skiprows=0, dtype='str', max_rows=1, usecols=np.arange(0, len(np.loadtxt(self.__path_to_txt, skiprows=0, dtype='str', max_rows=1))))
        return station_headlines

    def get_station_information(self):
        station_information = np.loadtxt(self.__path_to_txt, skiprows=2, dtype={"names": (self.__get_station_headlines()), "formats": ("i4", "i4", "i4", "i4", "f4", "f4", "S20", "S20")},
                                         usecols=np.arange(0, len(self.__get_station_headlines())))
        return station_information

    def read_station_list(self):
        stations = {}
        get_station_information = self.get_station_information()
        for i in range((len(get_station_information))):
            stations.update({self.__data_type + "_{:05d}".format(get_station_information[i][0]): Station(get_station_information[i], self.__local_path, data_type=self.__data_type)})
        return stations

    def get_active_stations(self):
        read_station_list = self.read_station_list()
        station_information = self.get_station_information()
        station_ids = self.get_station_ids()
        active_stations_array = np.array([])
        for active_station in read_station_list:
            if read_station_list.get(active_station).check_data() == 1:
                active_stations_array = np.append(active_stations_array, read_station_list.get(active_station).check_activitiy())
            else:
                active_stations_array = np.append(active_stations_array, 2)
        x_active = station_information[:]["geoLaenge"][active_stations_array == 1]
        y_active = station_information[:]["geoBreite"][active_stations_array == 1]
        z_active = station_information[:]["Stationshoehe"][active_stations_array == 1]
        active_id = station_ids[:][active_stations_array == 1]
        x_not_active = station_information[:]["geoLaenge"][active_stations_array == 0]
        y_not_active = station_information[:]["geoBreite"][active_stations_array == 0]
        z_not_active = station_information[:]["Stationshoehe"][active_stations_array == 0]
        not_activ_id = station_ids[:][active_stations_array == 0]
        x_no_data = station_information[:]["geoLaenge"][active_stations_array == 2]
        y_no_data = station_information[:]["geoBreite"][active_stations_array == 2]
        z_no_data = station_information[:]["Stationshoehe"][active_stations_array == 2]
        no_data_id = station_ids[:][active_stations_array == 2]
        return x_active, y_active, z_active, active_id, x_not_active, y_not_active, z_not_active, not_activ_id, x_no_data, y_no_data, z_no_data, no_data_id

    def get_active_stations_in_date(self, start_date, end_date):
        station_information = self.get_station_information()
        station_ids = self.get_station_ids()
        get_station_ids_in_date = self.get_station_ids_in_date(start_date, end_date)
        x_active = station_information[:]["geoLaenge"][get_station_ids_in_date == 1]
        y_active = station_information[:]["geoBreite"][get_station_ids_in_date == 1]
        z_active = station_information[:]["Stationshoehe"][get_station_ids_in_date == 1]
        active_id = station_ids[:][get_station_ids_in_date == 1]
        return x_active, y_active, z_active, active_id

    def get_station_ids_in_date(self, start_date, end_date):
        """
        test
        """
        activ_stations_in_date_array = np.array([])
        read_station_list = self.read_station_list()
        for station_id in read_station_list:
            activ_stations_in_date_array = np.append(activ_stations_in_date_array, read_station_list.get(station_id).check_activ_in_date(start_date, end_date))
        return activ_stations_in_date_array

    def get_station_ids(self):
        station_ids_array = np.array([])
        read_station_list = self.read_station_list()
        for station_id in read_station_list:
            station_ids_array = np.append(station_ids_array, read_station_list.get(station_id).get_station_id())
        return station_ids_array


    def data_prep_for_new_location(self, start_date, end_date, x_coordinate, y_coordinate, z_coordinate):
        new_point_name = "Find near TU for me"
        x_active_reader, y_active_reader, z_active_reader, activ_id_reader = self.get_active_stations_in_date(start_date, end_date)
        x_active_in_date = [x_coordinate]
        for i in x_active_reader:
            x_active_in_date.append(i)
        y_active_in_date = [y_coordinate]
        for i in y_active_reader:
            y_active_in_date.append(i)
        z_active_in_date = [z_coordinate]
        for i in z_active_reader:
            z_active_in_date.append(i)
        activ_id_in_date = [new_point_name]
        for i in activ_id_reader:
            activ_id_in_date.append(i)
        station_list = self.read_station_list()
        return x_active_in_date, y_active_in_date, z_active_in_date, activ_id_in_date, station_list


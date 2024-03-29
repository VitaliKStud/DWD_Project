import numpy as np
from datetime import datetime, timedelta
import os
from itertools import compress
import json


class Station:
    """
    :Description: This class will generate stations as objects with all the given informations.
    """
    def __init__(self, stations_array, local_path, data_type):
        """
        :param stations_array: **as array**. Is generated by Reader(...).read_station_list()
        :param local_path: **as string**. Is getting from Reader class
        :param data_type: **as string**. Ss getting from Reader class
        """
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
        """
        **Description:** formating the date yyymmddhhmm --> YYYY-MM-DD

        :param number: **as int**.
        :return: date: **as string**.
        """
        year = number // 10000
        month = number // 100 - year * 100
        day = number - month * 100 - year * 10000
        date = str(year) + "-" + str(month) + "-" + str(day)
        return date

    def get_local_path(self):
        """
        **Description:** Here you can get the local_path information

        :return: __local_path: **as string**
        """
        return self.__local_path

    def get_station_id(self):
        """
         **Description:** Here you can get the stations_id information

         :return: __stations_id: **as string**
         """
        return self.__stations_id

    def get_von_datum(self):
        """
         **Description:** Here you can get the von_dotum information

         :return: __von_datum: **as string**
         """
        return self.__von_datum

    def get_bis_datum(self):
        """
         **Description:** Here you can get the __bis_datum information

         :return: __bis_datum: **as string**
         """
        return self.__bis_datum

    def get_stationshoehe(self):
        """
         **Description:** Here you can get the __stationshoehe information

         :return: __stationshoehe: **as int**
         """
        return self.__stationshoehe

    def get_geobreite(self):
        """
         **Description:** Here you can get the __geoBreite information

         :return: __geoBreite: **as int**
         """
        return self.__geoBreite

    def get_geolaenge(self):
        """
         **Description:** Here you can get the __geoLaenge information

         :return: __geoLaenge: **as int**
         """
        return self.__geoLaenge

    def get_stationsname(self):
        """
         **Description:** Here you can get the __stationsname information

         :return: __stationsname: **as string**
         """
        return self.__stationsname

    def get_bundesland(self):
        """
         **Description:** Here you can get the __bundesland information

         :return: __bundesland: **as string**
         """
        return self.__bundesland

    def check_activitiy(self):
        """
        **Description:** Will check the activity of the station (was this station activ past 10 days?)

        :return: **Boolean**
        """
        return datetime.now() - datetime.strptime(self.__bis_datum, "%Y-%m-%d") < timedelta(days=365)

    def get_station_informations(self):
        """
        **Description:** Will return all the informations of the station as a dict

        :return: station_information_dict: **as dict**
        """
        station_information_dict = {"ID": self.__stations_id, "von_datum": self.__von_datum, "bis_datum": self.__bis_datum, "stationshoehe": self.__stationshoehe, "geoBreite": self.__geoBreite,
         "geoLaenge": self.__geoLaenge, "Stationsname": self.__stationsname, "Bundesland": self.__bundesland, "Aktivität": self.check_activitiy()}
        return station_information_dict

    def generate_tu_data_path(self):
        """
        **Description:** Will generate all the local paths for this station

        :return: local_list: **as list**
        """
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
        """
        **Description:** Is checking if this station got any data available (0 == no data, 1 == data available)

        :return: 0 or 1: **as int**
        """
        if self.generate_tu_data_path() == 0:
            return 0
        else:
            return 1

    def generate_tu_date_array(self):
        """
        **Description:** Will generate all the data paths and all the timedelta the station was activ in

        :return: from_list: **as list**, tu_data_path: **as list**
        """
        if self.check_data() == 1:
            tu_data_path = self.generate_tu_data_path()
            from_list = []
            for i in range(len(tu_data_path)):
                if i == len(tu_data_path) - 1:
                    with open(tu_data_path[i], "r") as file:
                        file.readline()
                        first_line = file.readline()
                        counter = 0
                        for last_line in file:
                            counter = counter + 1
                            pass
                    if counter == 0:
                        pass
                    else:
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
        """
        **Description:** Will generate all the data paths in timedelta. If no data available for this station, returns False

        :param start_date: **as int**: YYYYMMDDHHMM
        :param end_date: **as int**: YYYYMMDDHHMM
        :return: generate_tu_data_path_date: **as list** or False
        """
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
        """
        **Description:** Will check the station activity in timedelta (True: is activ in timedelta, False: not activ in timedelta)

        :param start_date: **as int**: YYYYMMDDHHMM
        :param end_date: **as int**: YYYYMMDDHHMM
        :return: Boolean
        """
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
    """
    :Description: This class write some json files. For faster loading times you should write this files after you downloaded and extracted your data.
    """
    def __init__(self, path_to_txt, local_path, data_type):
        """
        :param path_to_txt: **as string**: Is the path to the txt of station descriptions / informations
        :param local_path: **as string**: Is the path to the extracted_files
        :param data_type: **as string**: Is the type of data (Example: "TU" or "SOLAR")
        """
        self.__path_to_txt = path_to_txt
        self.__local_path = local_path
        self.__data_type = data_type

    def write_stations_paths(self):
        """
        :Description: Will write two json files in extracted_files (dict_tu_data_path and dict_from_list) with all the dates and all the paths for any station
        :return: path where the data was written
        """
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
    """
    :Description: This class will read all the descriptions / informations of all the stations and will generate needed data.
    """
    def __init__(self, path_to_txt, local_path, data_type):
        """
        :param path_to_txt: **as string**: Is the path to the txt of station descriptions / informations
        :param local_path: **as string**: Is the path to the extracted_files
        :param data_type: **as string**: Is the type of data (Example: "TU" or "SOLAR")
        """
        self.__path_to_txt = path_to_txt
        self.__local_path = local_path
        self.__data_type = data_type

    def __get_station_headlines(self):
        """
        :Description: Will get the headlines of the txt

        :return: station_headlines: **as array**
        """
        station_headlines = np.loadtxt(self.__path_to_txt, skiprows=0, dtype='str', max_rows=1, usecols=np.arange(0, len(np.loadtxt(self.__path_to_txt, skiprows=0, dtype='str', max_rows=1))))
        return station_headlines

    def get_station_information(self):
        """
        :Description: Will create an array with all the information from the informations-txt

        :return: station_information: **as array ("i4", "i4", "i4", "i4", "f4", "f4", "S20", "S20")**
        """
        station_information = np.loadtxt(self.__path_to_txt, skiprows=2, dtype={"names": (self.__get_station_headlines()), "formats": ("i4", "i4", "i4", "i4", "f4", "f4", "S20", "S20")},
                                         usecols=np.arange(0, len(self.__get_station_headlines())))
        return station_information

    def read_station_list(self):
        """
        :Description: Will create all the station objects in a dictionary

        :return: stations: **as dict**
        """
        stations = {}
        get_station_information = self.get_station_information()
        for i in range((len(get_station_information))):
            stations.update({self.__data_type + "_{:05d}".format(get_station_information[i][0]): Station(get_station_information[i], self.__local_path, data_type=self.__data_type)})
        return stations

    def get_active_stations(self):
        """
        :Description: Will create some important arrays (all active stations, not active stations and stations with no data) for past 10 days

        :return: x_active, y_active, z_active, active_id, x_not_active, y_not_active, z_not_active, not_activ_id, x_no_data, y_no_data, z_no_data, no_data_id: **all as array**
        """
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
        """
        :Description: Will create some important arrays (all active stations, not active stations and stations with no data) in timedelta

        :param: start_date: **as int**: YYYYMMDDHHMM
        :param: end_date: **as int**: YYYYMMDDHHMM
        :return: x_active, y_active, z_active, active_id: **all as array**
        """
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
        :Description: Will create a mask for active stations in timedelta

        :param: start_date: **as int**: YYYYMMDDHHMM
        :param: end_date: **as int**: YYYYMMDDHHMM
        :return: activ_stations_in_date_array: *as array** (is a mask)
        """
        activ_stations_in_date_array = np.array([])
        read_station_list = self.read_station_list()
        for station_id in read_station_list:
            activ_stations_in_date_array = np.append(activ_stations_in_date_array, read_station_list.get(station_id).check_activ_in_date(start_date, end_date))
        return activ_stations_in_date_array

    def get_station_ids(self):
        """
        :Description: Will create an array with all the station_ids with a prefix

        :return: station_ids_array: *as array**
        """
        station_ids_array = np.array([])
        read_station_list = self.read_station_list()
        for station_id in read_station_list:
            station_ids_array = np.append(station_ids_array, read_station_list.get(station_id).get_station_id())
        return station_ids_array


    def data_prep_for_new_location(self, start_date, end_date, x_coordinate, y_coordinate, z_coordinate):
        """
        :Description: Will prepare all the data that is available in timedelta for a new location

        :param: x_coordinate: **as float**: (GeoLaenge) for the new location
        :param: y_coordinate: **as float**: (GeoBreite) for the new location
        :param: z_coordinate: **as float**: 0 for now (maybe needed in future) for the new location
        :return: x_active_in_date, y_active_in_date, z_active_in_date, activ_id_in_date, station_list: **as list - station_list as dict**
        """
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


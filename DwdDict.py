"""description
:Describtion: Is a global dictionary for all data you are scraping for DWD/CDC. If you want to change from 10_minutes resolution to 1_minute resolution of your data, you might start here with few changes.

+----------------------+------+------------------------------------------------+
| Name                 | type | description                                    |
+======================+======+================================================+
| external_domain      | str  | What domain do you use for your data?          |
|                      |      | Default:"https://opendata.dwd.de/"             |
+----------------------+------+------------------------------------------------+
| external_global_path | str  | What data did you choose from external_domain? |
|                      |      | Default: "climate_environment/CDC/             |
|                      |      | observations_germany/climate/10_minutes/"      |
|                      |      |                                                |
|                      |      | Note: Here you could change for 1_minute.      |
+----------------------+------+------------------------------------------------+
| ending               | list | Is important for DwdDataScraper, for the       |
|                      |      | download. It will download all the data with   |
|                      |      | this given endings.                            |
|                      |      | Default: ".zip", ".pdf", ".txt"                |
+----------------------+------+------------------------------------------------+
| type_dict            | dict |                                                |
+----------------------+------+------------------------------------------------+
| load_txt_dict        | dict |                                                |
+----------------------+------+------------------------------------------------+
| rest_dict            | dict |                                                |
+----------------------+------+------------------------------------------------+
| title_dict           | dict |                                                |
+----------------------+------+------------------------------------------------+
| unit_dict            | dict |                                                |
+----------------------+------+------------------------------------------------+
| type_of_time_list    | list |                                                |
+----------------------+------+------------------------------------------------+
| type_of_data_list    | list |                                                |
+----------------------+------+------------------------------------------------+
"""


def get_dwd_dict():
    """
    :return: type_dict, load_txt_dict, rest_dict, title_dict, unit_dict, type_of_time_list, type_of_data_list, external_domain, external_path_global, ending
    """

    external_domain = "https://opendata.dwd.de/"
    external_path_global = "climate_environment/CDC/observations_germany/climate/10_minutes/"
    ending = [".zip", ".pdf", ".txt"]
    # choose your paths and which data you need

    type_dict = {"air_temperature": "TU", "precipitation": "nieder", "solar": "SOLAR", "wind": "wind"}
    load_txt_dict = {"air_temperature": "tu", "precipitation": "rr", "solar": "sd", "wind": "ff"}
    rest_dict = {"recent": "zehn_min_", "now": "zehn_now_", "historical": "zehn_min_"}
    # leave it (global dictionaries)

    title_dict = {"air_temperature":{"PP_10": "Luftdruck [p] auf Stationshoehe in hPa",
                                     "TT_10": "Lufttemperatur [T] auf 2m Hoehe in °C",
                                     "TM5_10": "Lufttemperatur [T] auf 5cm Hoehe in °C",
                                     "TD_10": "Taupunkttemperatur [T] auf 2m Hoehe in °C",
                                     "RF_10": "relative Feuchte [r.F] auf 2m Hoehe in %"},
                  "precipitation": {"RWS_DAU_10": "Niederschalgsdauer [t] der letzten 10-Minuten in min",
                                    "RWS_10": "Niederschalgshoehe [h] der letzten 10-Minuten in mm",
                                    "RWS_IND_10": "[0: kein Niederschlag], [1: Niederschlag gefallen], [3: Niederschlag gefallen und Heizung des Messgerätes an"},
                  "solar": {"DS_10": "10min-Summe der diffusen solaren Strahlung in J/cm^2",
                            "GS_10": "10min-Summe der Globalstrahlung in/ J/cm^2",
                            "SD_10": "10min-Summe der Sonnenscheindauer in h"},
                  "wind": {"FF_10": "10min-Mittel der Windgeschwindigkeit in m/s",
                           "DD_10": "10min-Mittel der Windrichtung in Grad"}}
    #title Dict


    unit_dict = {"air_temperature":{"PP_10": "p / hPa",
                                    "TT_10": "T / °C",
                                    "TM5_10": "T / °C",
                                    "TD_10": "T / °C",
                                    "RF_10": "r.F. / %"},
                  "precipitation": {"RWS_DAU_10": "t / min",
                                    "RWS_10": "h / mm",
                                    "RWS_IND_10": "Index"},
                  "solar": {"DS_10": "E/A / J/cm^2",
                            "GS_10": "E/A / J/cm^2",
                            "SD_10": "t / h"},
                  "wind": {"FF_10": "v / m/s",
                           "DD_10": "Winkel / Grad"}}
    # Unit Dict


    type_of_time_list = ["recent", "now", "historical"]
    type_of_data_list = ["air_temperature", "precipitation", "solar", "wind"]
    # leave it (global lists). Here you can see what data_types and time_types are available (needed for type_of_data_ and type_of_time_)

    return type_dict, load_txt_dict, rest_dict, title_dict, unit_dict, type_of_time_list, type_of_data_list, external_domain, external_path_global, ending
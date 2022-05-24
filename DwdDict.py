def get_dwd_dict():
    external_domain = "https://opendata.dwd.de/"
    local_domain = "C:/Users/VID/Desktop/Betriebliche Praxis/"
    external_path_global = "climate_environment/CDC/observations_germany/climate/10_minutes/"
    ending = [".zip", ".pdf", ".txt"]
    # choose your paths and which data you need

    type_dict = {"air_temperature": "TU", "precipitation": "nieder", "solar": "SOLAR", "wind": "wind"}
    load_txt_dict = {"air_temperature": "tu", "precipitation": "rr", "solar": "sd", "wind": "ff"}
    rest_dict = {"recent": "zehn_min_", "now": "zehn_now_", "historical": "zehn_min_"}
    # leave it (global dictionaries)

    title_dict = {"air_temperature":{"PP_10": "Luftdruck [p] auf Stationshoehe in hPa", "TT_10": "Lufttemperatur [T] in 2m Hoehe in °C", "TM5_10": "Lufttemperatur [T] 5cm Hoehe in °C", "TD_10": "Taupunkttemperatur [T] in 2m Hoehe in °C"},
                  "precipitation": {"RWS_DAU_10": "Niederschalgsdauer [t] der letzten 10-Minuten in min", "RWS_10": "Niederschalgshoehe [h] der letzten 10-Minuten in mm", "RWS_IND_10": "[0: kein Niederschlag], [1: Niederschlag gefallen], [3: "
                                                                                                                                                                               "Niederschlag gefallen und Heizung des Messgerätes an"},
                  "solar": {"DS_10": "10min-Summe der diffusen solaren Strahlung / J/cm^2", "GS_10": "10min-Summe der Globalstrahlung / J/cm^2", "SD_10": "10min-Summe der Sonnenscheindauer / h"},
                  "wind": {"FF_10": "10min-Mittel der Windgeschwindigkeit / m/s", "DD_10": "10min-Mittel der Windrichtung / Grad"}}
    # Unit Dict.

    unit_dict = {"air_temperature":{"PP_10": "p / hPa", "TT_10": "T / °C", "TM5_10": "T / °C", "TD_10": "T / °C"},
                  "precipitation": {"RWS_DAU_10": "t / min", "RWS_10": "h / mm", "RWS_IND_10": "Index"},
                  "solar": {"DS_10": "E/A / J/cm^2", "GS_10": "E/A / J/cm^2", "SD_10": "t / h"},
                  "wind": {"FF_10": "v / m/s", "DD_10": "Winkel / Grad"}}


    type_of_time_list = ["recent", "now", "historical"]
    type_of_data_list = ["air_temperature", "precipitation", "solar", "wind"]
    # leave it (global lists). Here you can see what data_types and time_types are available (needed for type_of_data_ and type_of_time_)

    return type_dict, load_txt_dict, rest_dict, title_dict, unit_dict, type_of_time_list, type_of_data_list, external_domain, local_domain, external_path_global, ending
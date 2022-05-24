from DwdMain import DwdMain
import os
import tkinter as tk
import tkintermapview

os.chdir(r"C:/Users/VID/Desktop/Betriebliche Praxis/")
external_domain_ = "https://opendata.dwd.de/"
local_domain_ = "C:/Users/VID/Desktop/Betriebliche Praxis/"
external_path_global_ = "climate_environment/CDC/observations_germany/climate/10_minutes/"
ending_ = [".zip", ".pdf", ".txt"]
# choose your paths and which data you need


type_dict_ = {"air_temperature": "TU", "precipitation": "nieder", "solar": "SOLAR", "wind": "wind"}
load_txt_dict_ = {"air_temperature": "tu", "precipitation": "rr", "solar": "sd", "wind": "ff"}
rest_dict_ = {"recent": "zehn_min_", "now": "zehn_now_", "historical": "zehn_min_"}
# leave it (global dictionaries)


type_of_time_list_ = ["recent", "now", "historical"]
type_of_data_list_ = ["air_temperature", "precipitation", "solar", "wind"]
# leave it (global lists). Here you can see what data_types and time_types are available (needed for type_of_data_ and type_of_time_)


looking_for_ = ["PP_10", "TT_10"]
# choose your data you need to plot #EXAMPLE: looking_for_ = ["TT_10", "RF_10", "PP_10"]


compare_station_ = "00164"
# for data to compare

start_date_ = 202205100000
end_date_ = 202205170000
# yyyymmddhhmm

x_coordinate_ = 13.9908
y_coordinate_ = 53.0316
z_coordinate_ = 0
# geoLaenge, geoBreite, height

k_factor_ = 6
# How many Stations you're looking for around your x_coordinate and y_coordinate

type_of_data_ = "air_temperature"
type_of_time_ = "recent"
# what type do you have? Check type_of_data_list_ and type_of_time_list_


dwd = DwdMain(external_domain=external_domain_,
              external_path_global=external_path_global_,
              local_domain=local_domain_,
              ending=ending_,
              type_of_data=type_of_data_,
              type_of_time=type_of_time_,
              type_dict=type_dict_,
              load_txt_dict=load_txt_dict_,
              rest_dict=rest_dict_,
              start_date=start_date_,
              end_date=end_date_,
              compare_station=compare_station_,
              x_coordinate=x_coordinate_,
              y_coordinate=y_coordinate_,
              z_coordinate=z_coordinate_,
              k_factor=k_factor_,
              looking_for=looking_for_,
              type_of_time_list=type_of_time_list_,
              type_of_data_list=type_of_data_list_)


# dwd.main_datascrapper()
# dwd.main_writer()
# dwd.main_data_map()
# dwd.main_plotter_stations(projection=True)
# dwd.main_plotter_data(compare=True)



class DwdGui:
    def __init__(self):
        pass

    def main():
        root = tk.Tk()
        root.geometry(f"{1820}x{980}")
        root.title("dwd.py")
        root.configure(bg="black")

        map_widget = tkintermapview.TkinterMapView(root, width=1820, height=980, corner_radius=0)
        map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        map_widget.set_position(51, 10)
        map_widget.set_zoom(6)
        map_widget.set_marker(51,10, text="test")

        root.mainloop()


#DwdGui.main()

    # def main(self):
    #     main_window = Tk()
    #     main_window.title("DWD Wetterdaten")
    #     main_window.geometry("1920x1080")
    #
    #     def on_mousewheel(event):
    #         my_canvas.yview_scroll(-1*(event.delta/120), "units")
    #
    #     graph_1frame = Frame(main_window)
    #     graph_1frame.pack()
    #
    #     graph_2frame = Frame(main_window)
    #     graph_2frame.pack()
    #
    #     entry_1 = Entry(main_window)
    #     entry_1.pack()
    #
    #     def main_click():
    #         entry_1_value = int(entry_1.get())
    #         figure, figure2 = main(entry_1_value)
    #         chart = FigureCanvasTkAgg(figure, graph_1frame)
    #         chart.get_tk_widget().pack()
    #
    #         chart2 = FigureCanvasTkAgg(figure2, graph_2frame)
    #         chart2.get_tk_widget().pack()
    #
    #     button_1 = Button(main_window, text="test", command=main_click)
    #     button_1.pack()
    #
    #     main_window.mainloop()


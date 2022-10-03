import matplotlib.pyplot as plt
import gc
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.style.use('default')
#plt.style.use('dark_background')
#plt.style.use('Solarize_Light2')


class PlotterForStations:
    """
    :Description: This class will create plots of station locations
    """

    def __init__(self, x, y, z=0, type_of_data=""):
        """
        :param x: x-coordinates: **as array**.
        :param y: y-coordinates: **as array**.
        :param z: z-coordinates: **as array**.
        :param type_of_data: **as string**. Check DwdDict.py type_of_data_list
        """
        self.__x = x
        self.__y = y
        self.__z = z
        self.type_of_data = type_of_data

    def plotting_3d(self, projection=False):
        """
        :Description: This method will plot all the stations in as a 3D-Version

        :param projection: **as Boolean**. If projection==True, it will project the height of the stations.
        :return: "plot saved" if succeeded.
        """
        fig = plt.figure()
        fig.set_size_inches(12, 14)


        ax = fig.add_subplot(111, projection="3d")
        ax.stem(self.__x, self.__y, self.__z, bottom=0, basefmt=" ", orientation="z", linefmt='orange')
        ax.view_init(20, 120)
        ax.set_xlabel("Geolaenge / °E", color='black', weight='normal', size=18, labelpad=25)
        ax.set_ylabel("Gebreite / °N", color='black', weight='normal', size=18, labelpad=25)
        ax.set_zlabel("Stationshoehe / m", color='black', weight='normal', size=18, labelpad=30)
        ax.tick_params(axis='z', which='major', pad=10)
        plt.title(f"Geolokalisierung von Stationen in Deutschland [{self.type_of_data}]", pad=0, size=20,  weight='bold')

        ax.xaxis.set_tick_params(labelsize=16)
        ax.yaxis.set_tick_params(labelsize=16)
        ax.zaxis.set_tick_params(labelsize=16)


        if projection:
            ax.plot(self.__x, self.__z, "+", zdir="y", zs=0)
            fig.savefig("Graphs/projected_german_stations_3d_" + self.type_of_data + ".png")
        else:
            fig.savefig("Graphs/german_stations_3d_" + self.type_of_data + ".png")
        plt.cla()
        plt.clf()
        plt.close('all')
        gc.collect()

        return print("plot saved")

    def plotting_height_2d(self):
        """
        :Description: This method will plot all the stations in as a 2D-Version

        :return: "plot saved" if succeeded.
        """
        fig = plt.figure(figsize=(12, 14), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        print(len(self.__x))
        plt.scatter(self.__x, self.__y, c=self.__z, cmap=plt.cm.get_cmap("seismic", 5), marker="s")
        plt.clim(0, 1000)
        plt.grid(True, linestyle='--', linewidth=0.5, color="black")
        plt.title(f"Geolokalisierung von Stationen in Deutschland [{self.type_of_data}]", pad=30, size=20,  weight='bold')

        cbar = plt.colorbar(extend="max")
        cbar.set_ticks([0, 200, 400, 600, 800, 1000])
        cbar.set_label('Stationshoehe / m', rotation=270, size=18, labelpad=18)
        cbar.ax.tick_params(labelsize=14)

        ax.set_xlabel("Geolaenge / °E", color='black', weight='normal', size=18, labelpad=20)
        ax.set_ylabel("Gebreite / °N", color='black', weight='normal', size=18, labelpad=20)
        ax.set_facecolor('lightgreen')
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

        fig.savefig("Graphs/german_stations_2d_" + self.type_of_data + ".png")
        plt.cla()
        plt.clf()
        plt.close('all')
        gc.collect()

        return print("plot saved")


class PlotterForData:
    """
    :Description: This class will create plots of the data of chosen stations.
    """

    def __init__(self, data_all, data_mean, index_for_plot, column_name_list, start_date_datetime, end_date_datetime, plot_name, k_factor, x_coordinate, y_coordinate, type_of_data, unit_dict, title_dict):
        """
        :param data_all: **as DataFrame**. All the datas in a DataFrame.
        :param data_mean:  **as DataFrame**. Your calculation (average for example).
        :param index_for_plot:  **as list**. The timedelta for x-axes.
        :param column_name_list: **as list**. Names of plotted lines.
        :param start_date_datetime: **as datetime**. Your chosen start-date (YYYY-MM-DD-HH:MM).
        :param end_date_datetime: **as datetime**. Your chosen end-date (YYYY-MM-DD-HH:MM).
        :param plot_name: **as string**.  Your chosen plot-title.
        :param k_factor: **as int**. Your chosen k_factor.
        :param x_coordinate: **as float**. Your chosen x-coordinate.
        :param y_coordinate: **as float**. Your chosen y-coordinate.
        :param type_of_data: **as string**. Check DwdDicht.py type_of_data_list
        :param unit_dict: **as string**. Will get the correct type from self.type_of_data.
        :param title_dict: **as string**. Will get the correct type from self.type_of_data.
        """
        self.column_name_list = column_name_list
        self.data_all = data_all
        self.data_mean = data_mean
        self.index_for_plot = index_for_plot
        self.start_date_datetime = start_date_datetime
        self.end_date_datetime = end_date_datetime
        self.plot_name = plot_name
        self.k_factor = k_factor
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.type_of_data = type_of_data
        self.unit_dict = unit_dict[self.type_of_data]
        self.title_dict = title_dict[self.type_of_data]


    def plotting_compare(self, compare_station, data_to_compare, diff, maximum, avg_diff, type_of_method):
        """
        :Description: Will plot your data and the data with a station you are comparing with.

        :param compare_station: **as string**. The name of the station with the right prefix.
        :param data_to_compare: **as DataFrame**. The real data of a station.
        :param diff: **as DataFrame**. The difference between your calculation and real data of a station.
        :param maximum: **as int**. Maximum difference.
        :param avg_diff: **as array**. Average difference. (Will plot a constant line)
        :param type_of_method: **as string**. Name of your calculation method.
        :return: "plot saved" if succeeded.
        """
        if np.isnan(avg_diff[0]):
            pass
        else:
            fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(20, 10), dpi=100)
            plt.subplots_adjust(left=None, bottom=0.1, right=None, top=0.85, wspace=0.5, hspace=0.5)

            for i in self.column_name_list[1:]:
                ax1.plot(self.index_for_plot, self.data_all[i], linewidth=0.5)
            ax1.set_xlim(self.start_date_datetime, self.end_date_datetime)
            lgn_1 = ax1.legend(self.column_name_list[1:], bbox_to_anchor=(0, 1.02, 1, 0.2), loc='lower left', ncol=10, prop={'size': 8})
            ax1.set_title(f"{self.title_dict[self.plot_name]}" , pad=60, weight='bold', size=18)
            ax1.grid(True, linestyle='--', linewidth=0.25, color="grey")
            ax1.set_ylabel(self.unit_dict[self.plot_name], color='black', weight='normal', size=14, labelpad=30, rotation=0)
            ax1.xaxis.set_tick_params(labelsize=10, pad=10)
            ax1.yaxis.set_tick_params(labelsize=10, pad=15)
            for i in lgn_1.legendHandles:
                i.set_linewidth(5)

            ax2.plot(self.index_for_plot, self.data_mean, label="Berechneter Durchschnitt", linestyle="--")
            ax2.plot(self.index_for_plot, data_to_compare, label="Realwerte")
            ax2.set_xlim(self.start_date_datetime, self.end_date_datetime)
            lgn_2 = ax2.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc='lower left', prop={'size': 10}, ncol=2)
            ax2.set_title(f"{type_of_method} der Stationen verglichen mit den Realwerten der Station {compare_station}", pad=10, weight='bold', loc="right")
            ax2.grid(True, linestyle='--', linewidth=0.25, color="grey")
            ax2.set_ylabel(self.unit_dict[self.plot_name], color='black', weight='normal', size=14, labelpad=30, rotation=0)
            ax2.xaxis.set_tick_params(labelsize=10, pad=10)
            ax2.yaxis.set_tick_params(labelsize=10, pad=15)
            for i in lgn_2.legendHandles:
                i.set_linewidth(5)

            ax3.bar(self.index_for_plot, diff, width=np.timedelta64(20, 'm'), label="Abweichung von Realwerten", color="darkred")
            ax3.plot(self.index_for_plot, avg_diff, label="Durchschnittliche Abweichung", color="b")
            ax3.set_xlim(self.start_date_datetime, self.end_date_datetime)
            ax3.set_ylim(0, maximum+1)
            lgn_3 = ax3.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc='lower left', prop={'size': 10}, ncol=2)
            ax3.set_title(f"Absolute Abweichung von den Realwerten", pad=10, weight='bold', loc="right")
            ax3.grid(True, linestyle='--', linewidth=0.25, color="grey")
            ax3.set_xlabel("Datum", color='black', weight='normal', size=12, labelpad=20)
            ax3.set_ylabel(self.unit_dict[self.plot_name], color='black', weight='normal', size=14, labelpad=35, rotation=0)
            ax3.xaxis.set_tick_params(labelsize=10, pad=10)
            ax3.yaxis.set_tick_params(labelsize=10, pad=15)
            for i in lgn_3.legendHandles:
                i.set_linewidth(5)

            textstr = (f"Parameter: [k-Faktor: {self.k_factor-1}], [geoLaenge: {self.x_coordinate:.4f}], "
                          f"[geoBreite: {self.y_coordinate:.4f}], [Startdatum: {self.start_date_datetime}], [Enddatum: {self.end_date_datetime}] Ergebnis: [Maximale absolute Abweichung: {maximum:.4f}], [Durchschnittliche Abweichung: {avg_diff[0]:.4f}]")
            props = dict(boxstyle='round', facecolor='salmon', alpha=0.2)
            plt.text(0.5, 0.99, textstr, transform=plt.gcf().transFigure, fontsize=10, bbox=props, ha='center', va="center")

            fig.savefig("Graphs/" + "compare_" + type_of_method + self.plot_name + ".png")
            plt.cla()
            plt.clf()
            plt.close('all')
            gc.collect()

            return print("plot saved")

    def plotting_data(self, type_of_method):
        """
        :Description: Will plot your data.

        :param type_of_method: **as string** Name of your calculation method
        :return: "plot saved" if succeeded.
        """
        print(self.data_all)
        print(self.data_mean)
        print(self.unit_dict)
        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(20, 10), dpi=100)
        plt.subplots_adjust(left=None, bottom=0.1, right=None, top=0.85, wspace=0.5, hspace=0.5)

        for i in self.column_name_list:
            ax1.plot(self.index_for_plot, self.data_all[i], linewidth=0.5)
        lgn_1 = ax1.legend(self.column_name_list, bbox_to_anchor=(0, 1.00, 1, 0.2), loc='lower left', ncol=10, prop={'size': 12})
        ax1.set_title(f"{self.title_dict[self.plot_name]}" , pad=60, weight='bold', size=18)
        ax1.set_xlim(self.start_date_datetime, self.end_date_datetime)
        ax1.set_ylabel(self.unit_dict[self.plot_name], color='black', weight='normal', size=14, labelpad=30, rotation=0)
        ax1.grid(True, linestyle='--', linewidth=0.25, color="grey")
        ax1.xaxis.set_tick_params(labelsize=12, pad=10)
        ax1.yaxis.set_tick_params(labelsize=12, pad=15)
        for i in lgn_1.legendHandles:
            i.set_linewidth(5)

        ax2.plot(self.index_for_plot, self.data_mean, linewidth=0.5)
        lgn_2 = ax2.legend(["Berechneter Durchschnitt"], bbox_to_anchor=(0, 1.00, 1, 0.2), loc='lower left', prop={'size': 12}, ncol=2)
        ax2.set_title(f"{type_of_method} der {self.k_factor} Stationen", pad=10, weight='bold', size=18)
        ax2.set_xlim(self.start_date_datetime, self.end_date_datetime)
        ax2.set_xlabel("Datum", color='black', weight='normal', size=14, labelpad=20)
        ax2.set_ylabel(self.unit_dict[self.plot_name], color='black', weight='normal', size=14, labelpad=30, rotation=0)
        ax2.grid(True, linestyle='--', linewidth=0.25, color="grey")
        ax2.xaxis.set_tick_params(labelsize=12, pad=10)
        ax2.yaxis.set_tick_params(labelsize=12, pad=15)
        for i in lgn_2.legendHandles:
            i.set_linewidth(5)

        textstr = (f"Parameter: [k-Faktor: {self.k_factor}], [geoLaenge: {self.x_coordinate:.4f}], "
                      f"[geoBreite: {self.y_coordinate:.4f}], [Startdatum: {self.start_date_datetime}], [Enddatum: {self.end_date_datetime}]")
        props = dict(boxstyle='round', facecolor='salmon', alpha=0.2)
        plt.text(0.5, 0.99, textstr, transform=plt.gcf().transFigure, fontsize=10, bbox=props, ha='center', va="center")


        fig.savefig("Graphs/" + self.type_of_data + "_" + self.plot_name + "_" + type_of_method +".png")
        plt.cla()
        plt.clf()
        plt.close('all')
        gc.collect()

        return print("plot saved")

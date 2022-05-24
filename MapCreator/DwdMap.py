from ipyleaflet import Map, basemaps, Marker, FullScreenControl, ScaleControl, AwesomeIcon, LegendControl, SplitMapControl, Heatmap, LayersControl, basemap_to_tiles
from ipywidgets import HTML, Layout
from IPython.display import display
import json


class DwdMap:
    def __init__(self, locations, location_marker_x, location_marker_y, local_domain):
        self.locations = locations
        self.location_marker_x = location_marker_x
        self.location_marker_y = location_marker_y
        self.local_domain = local_domain

    def create_map(self):
        zip_data_not_active = []
        zip_no_data = []
        if self.locations == "Stations":
            with open(self.local_domain + r"DWD_Project/MapCreator/" + r"zip_data_activ.json", "r") as f:
                zip_data_active = json.load(f)
            with open(self.local_domain + r"DWD_Project/MapCreator/" + r"zip_data_not_activ.json", "r") as f:
                zip_data_not_active = json.load(f)
            with open(self.local_domain + r"DWD_Project/MapCreator/" + r"zip_no_data.json", "r") as f:
                zip_no_data = json.load(f)
        elif self.locations == "ActivInDate":
            with open(self.local_domain + r"DWD_Project/MapCreator/" + r"zip_data_active_in_date.json", "r") as f:
                zip_data_active = json.load(f)
        elif self.locations == "NearStations":
            with open(self.local_domain + r"DWD_Project/MapCreator/" + r"zip_data_near.json", "r") as f:
                zip_data_active = json.load(f)

        full_screen_map = Map(center=(51, 10), zoom=7, layout=Layout(width='100%', height='1000px'), close_popup_on_click=False)
        icon1 = AwesomeIcon(name='gear', marker_color='green', icon_color='black', spin=False)
        icon2 = AwesomeIcon(name='gear', marker_color='red', icon_color='black', spin=False)
        icon3 = AwesomeIcon(name='gear', marker_color='orange', icon_color='black', spin=False)
        icon4 = AwesomeIcon(name='circle-o-notch', marker_color='blue', icon_color='black', spin=True)

        for i in zip_data_active:
            marker = Marker(location=(i[1], i[0]), draggable=False, icon=icon1)
            full_screen_map.add_layer(marker)
            message = HTML()
            message.value = "StationID: " + str(i[2]) + "<br>" "geoBreite: " + str(i[1]) + "<br>" + "geoLaenge: " + str(i[0]) + "<br>"
            marker.popup = message

        for i in zip_data_not_active:
            marker = Marker(location=(i[1], i[0]), draggable=False, icon=icon2)
            full_screen_map.add_layer(marker)
            message = HTML()
            message.value = "StationID: " + str(i[2]) + "<br>" "geoBreite: " + str(i[1]) + "<br>" + "geoLaenge: " + str(i[0]) + "<br>"
            marker.popup = message

        for i in zip_no_data:
            marker = Marker(location=(i[1], i[0]), draggable=False, icon=icon3)
            full_screen_map.add_layer(marker)
            message = HTML()
            message.value = "StationID: " + str(i[2]) + "<br>" "geoBreite: " + str(i[1]) + "<br>" + "geoLaenge: " + str(i[0]) + "<br>"
            marker.popup = message

        marker_search = Marker(location=(self.location_marker_x, self.location_marker_y), draggable=False, icon=icon4)
        full_screen_map.add_layer(marker_search)

        full_screen_map.add_control(SplitMapControl(left_layer=basemap_to_tiles(basemaps.OpenTopoMap), right_layer=basemap_to_tiles(basemaps.Esri.WorldImagery)))
        full_screen_map.add_control(FullScreenControl())
        full_screen_map.add_control(ScaleControl(position='bottomleft'))
        if self.locations == "Stations":
            full_screen_map.add_control(LegendControl({"green: active station": "green", "red: not active station": "red", "orange: no data available, but activ": "orange", "spinning_blue: selected location ": "blue"}, name="Legend", position="topright"))
        elif self.locations == "ActivInDate":
            full_screen_map.add_control(LegendControl({"green: active stations in date": "green", "spinning_blue: selected location ": "blue"}, name="Legend", position="topright"))
        elif self.locations == "NearStations":
            full_screen_map.add_control(LegendControl({"green: near activ stations in date": "green", "spinning_blue: selected location ": "blue"}, name="Legend", position="topright"))

        # full_screen_map.add_control(LayersControl(position="bottomright"))
        display(full_screen_map)

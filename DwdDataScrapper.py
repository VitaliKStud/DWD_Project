from bs4 import BeautifulSoup
from requests import get
import os
import requests
from datetime import datetime
import json
import zipfile

class DataScrapper:
    """
    :Description: This class will download and unzip your files. Check DwdDict module first!
    """
    def __init__(self,
                 external_domain,
                 external_path,
                 local_domain="",
                 ending=None,
                 looking_for_ending=""):
        """
        :param external_domain: **as string**. Will be set from your DwdDict.py
        :param external_path: **as string**. Will be set from your DwdDict.py
        :param local_domain: **as string**. Tells where to save your downloading and unzipping
        :param ending: **as list**. Will be set from your DwdDict.py
        :param looking_for_ending: **as string**. Skip this (not important for now, maybe in future)
        """
        self.__external_domain = external_domain
        self.__external_path = external_path
        self.__ending = ending
        self.__local_domain = local_domain
        self.__local_path = self.__local_domain + self.__external_path
        self.looking_for_ending = looking_for_ending

    def external_directory_indicator(self, pre_extend_list=""):
        """
        **Description:** Will generate a list (verzeichnis_list) of oll the "href" (links and urls) on a given page

        :param pre_extend_list: **as string**. Skip this (not important for now, maybe in future)
        :return: verzeichnis_list **as list**
        """
        soup = BeautifulSoup(requests.get(self.__external_domain + self.__external_path).text, "html.parser")
        verzeichnis_list = [pre_extend_list + self.__external_path + n.get("href") for n in soup.find_all("a") if n.get("href") != "../"]
        return verzeichnis_list

    def get_external_date(self):
        """
        **Description:** Will generate a list (text_elemnts) of all text elements on a page (here the date) (will be important in future).

        :return: text_elements **as list**
        """
        text_elements = []
        blacklist = ["a", "h1", "title"]
        external_directory_indicator = self.external_directory_indicator()
        for i in range(len(external_directory_indicator)):
            text_elements_i = []
            text_elements_i.clear()
            soup = BeautifulSoup(requests.get(self.__external_domain + external_directory_indicator[i]).text, "html.parser")
            text_elements_i = [item.strip() for item in soup.find_all(text=True) if item.parent.name not in blacklist]
            text_elements_i = [item.split() for item in text_elements_i if len(item) != 0]
            text_elements.append(text_elements_i)
        with open("last_data_update.json", "w") as f:
            json.dump(text_elements, f, indent=2)
        return text_elements

    def download(self, download_path):
        """
        **Description:** Is the main downloading method. It will download the data for you. It will also create folders of the same structure,
        that the path is in your local_domain (if not existing already). After the download it will create the needed .json file in the folder,
        where the data was saved. It will be called "last_download_date" and it will include some information about the filepath download-date and filename.

        :param download_path: **as string**. Can be generated by self.external_directory_indicator(). Or if you want to download something manually. The path would look like this: "climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/historical/"
        :return: "download finished" if succeeded.
        """
        soup = BeautifulSoup(requests.get(self.__external_domain + download_path).text, "html.parser")
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            date = []
            for download in soup.find_all("a"):
                date_i = []
                for check_ending in self.__ending:
                    if check_ending in download.get("href"):
                        print(download.get("href"))
                        date_i.append(download.get("href") + "," + datetime.now().strftime("%d-%b-%Y %H:%M") + "," + self.__external_path)
                        with open(os.getcwd() + "/" + download_path + download.get("href"), "wb") as file:
                            file.write(get(self.__external_domain + download_path + download.get("href")).content)
                    else:
                        continue
                date.append(date_i)
        else:
            date = []
            for check_ending in self.__ending:
                date_i = []
                for download in soup.find_all("a"):
                    if check_ending in download.get("href"):
                        print(download.get("href"))
                        date_i.append(download.get("href") + "," + datetime.now().strftime("%d-%b-%Y %H:%M") + "," + self.__external_path)
                        with open(os.getcwd() + "/" + download_path + download.get("href"), "wb") as file:  # saving path
                            file.write(get(self.__external_domain + download_path + download.get("href")).content)
                    else:
                        continue
                date.append(date_i)
        with open(os.getcwd() + "/" + download_path + r"last_download_date.json", "w") as f:
            json.dump(date, f, indent=2)
        return print("Download finished")

    def download_loop(self):
        """
        **Description:** Creates the download loop. Will download all the data from the self.external_directory_indicator()

        :return: None
        """
        external_directory_indicator = self.external_directory_indicator()
        for i in external_directory_indicator:
            self.download(i)

    def generate_local_list(self):
        """
        **Description:** Will generate a local_list with all filenames.

        :return: local_list **as list**
        """
        local_list = []
        for i in range(len((os.listdir(self.__local_path)))):
            local_list.append(os.listdir(self.__local_path + os.listdir(self.__local_path)[i]))
        return local_list

    def extract_zip(self, looking_for=".zip"):
        """
        **Description:** Extract all the files inside a path

        :param looking_for: **as string**. Should be ".zip".
        :return: "Extracting finished" if succeeded.
        """
        path_i = os.listdir(self.__local_path)
        for i in range(len(path_i)):
            path_j = os.listdir(self.__local_path + path_i[i] + "/")
            if not os.path.exists(self.__local_path + path_i[i] + "/" + "extracted_files"):
                os.makedirs(self.__local_path + path_i[i] + "/" + "extracted_files")
            for j in range(len(path_j)):
                my_path = self.__local_path + path_i[i] + "/" + path_j[j]
                if looking_for in my_path:
                    with zipfile.ZipFile(my_path, "r") as zip_j:
                        extract_in = self.__local_path + path_i[i] + "/" + "extracted_files/" + path_j[j].replace(".zip", "_unzipped/")
                        print("extracting: ", extract_in)
                        zip_j.extractall(extract_in)
                        zip_j.close()
                        print("extracting")
                else:
                    continue
        print("Extracting finished")

    def main_update_data(self):
        """
        **Description:** Compressed method for the download. Less complicated.

        :return: "Data updated" if succeeded.
        """
        self.download_loop()
        self.extract_zip()
        return print("Data updated")


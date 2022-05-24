#Station
# def check_date_activitiy(self, from_date, to_date):
#     if datetime.strptime(self.__bis_datum, "%Y-%m-%d") < datetime.strptime(from_date, "%Y-%m-%d"):
#         return False
#     elif datetime.strptime(self.__von_datum, "%Y-%m-%d") > datetime.strptime(to_date, "%Y-%m-%d"):
#         return False
#     else:
#         if datetime.strptime(self.__von_datum, "%Y-%m-%d") < datetime.strptime(from_date, "%Y-%m-%d"):
#             if datetime.strptime(self.__bis_datum, "%Y-%m-%d") <= datetime.strptime(to_date, "%Y-%m-%d"):
#                 return print(from_date + " bis " + self.__bis_datum)
#         elif datetime.strptime(self.__bis_datum, "%Y-%m-%d") > datetime.strptime(to_date, "%Y-%m-%d"):
#             if datetime.strptime(self.__von_datum, "%Y-%m-%d") <= datetime.strptime(to_date, "%Y-%m-%d"):
#                 return print(self.__von_datum + " bis " + to_date)
#         elif datetime.strptime(self.__von_datum, "%Y-%m-%d") >= datetime.strptime(from_date, "%Y-%m-%d"):
#             if datetime.strptime(self.__bis_datum, "%Y-%m-%d") <= datetime.strptime(to_date, "%Y-%m-%d"):
#                 return print(self.__von_datum + " bis " + self.__bis_datum)
#         else:
#             return print(from_date + " bis " + to_date)
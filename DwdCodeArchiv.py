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


# def compare(self, compare_station):
#     print(self.data_all)
#     print(compare_station)
#     data_to_compare = self.data_all[compare_station]
#     data_all = self.data_all.drop([compare_station], axis=1)
#     data_mean = data_all.mean(axis=1)
#     diff = (data_mean - data_to_compare).abs()
#     maximum = diff.max()
#     avg_diff = np.full((len(diff)), diff.sum()/len(diff))
#     print(f"Durchschnittliche Abweichung: {avg_diff[0]}")
#     print(f"Maximale Abweichung: {maximum}")
#     print(data_mean)

# return data_to_compare, data_mean, diff, maximum, avg_diff, data_all
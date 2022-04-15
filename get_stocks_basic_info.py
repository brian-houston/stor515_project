import os
import csv

def get_stocks_basic_info(folder_name):
    file_names = os.listdir(folder_name)
    basic_info = []

    for file_name in file_names:
        with open(folder_name + '/' + file_name) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            next(reader) 
            start = next(reader)

            info = {
                    'ticker': file_name.split('.')[0],
                    'start_date': start[0]
                }

            basic_info.append(info)

    return basic_info

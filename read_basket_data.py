import csv
from datetime import datetime

def read_basket_data(folder_name, basket, start_date, T):

    # true if date a is after date b
    def is_date_after(a, b):   
        a_date = datetime.strptime(a, '%d-%m-%Y')
        b_date = datetime.strptime(b, '%d-%m-%Y')
        return a_date >= b_date

    data = [[] for x in basket]

    for i in range(len(basket)):
        ticker = basket[i]

        with open(folder_name + '/' + ticker + '.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            next(reader) 

            for row in reader:
                if is_date_after(row[0], start_date):
                    data[i].append(float(row[6]))
                    break

            for j in range(T - 1):
                row = next(reader)
                data[i].append(float(row[6]))

    return data


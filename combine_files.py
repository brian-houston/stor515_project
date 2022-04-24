import csv
import os
from datetime import datetime

def combine_files(folder_name, combined_file_name, start_date, filtered_tickers):
    field_names = ['date']
    rows = []

    def is_date_after(a, b):   
        a_date = datetime.strptime(a, '%d-%m-%Y')
        b_date = datetime.strptime(b, '%d-%m-%Y')
        return a_date >= b_date

    file_names = os.listdir(folder_name)
    stock_count = 0
    for file_name in file_names:
        with open(folder_name + '/' + file_name) as io:
            ticker_name = file_name.split('.')[0]
            if ticker_name in filtered_tickers:
                continue

            io.readline()
            
            start_pos = io.tell()
            first_row = io.readline().strip().split(',')
            io.seek(start_pos)

            if is_date_after(first_row[0], start_date):
                continue

            for row in io:
                row = row.strip().split(',')
                if is_date_after(row[0], start_date):
                    break

            for date_count, row in enumerate(io):
                row = row.strip().split(',')

                if stock_count == 0:
                    rows.append([row[0]])

                if row[6] == '':
                    rows[date_count].append(rows[date_count-1][stock_count+1])
                else:
                    rows[date_count].append(row[6])

            field_names.append(ticker_name)
            stock_count += 1

    with open(combined_file_name, 'w') as io:
        io = csv.writer(io)
        io.writerow(field_names)
        io.writerows(rows)

folder_name = 'stock_market_data/sp500/csv'
start_date = '01-01-2017'
filtered_stocks = ['CTQ', 'SONC', 'CPICQ']
combine_files(folder_name, 'combined_stock_data.csv', start_date, filtered_stocks)

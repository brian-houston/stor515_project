import numpy as np
import csv
import os
from datetime import datetime

def combine_files(folder_name, combined_file_name, start_date, stocks):
    field_names = ['date']
    rows = []

    def is_date_after(a, b):   
        a_date = datetime.strptime(a, '%d-%m-%Y')
        b_date = datetime.strptime(b, '%d-%m-%Y')
        return a_date >= b_date

    for ticker_name in stocks:
        with open(folder_name + '/' + ticker_name + '.csv') as io:
            io.readline()
            
            for row in io:
                row = row.strip().split(',')
                if is_date_after(row[0], start_date):
                    break

            prev_price = 0 
            for date_count, row in enumerate(io):
                row = row.strip().split(',')
                curr_price = float(row[6])

                if date_count > 0 and ticker_name == stocks[0]:
                    rows.append([date_count])

                if date_count > 0:
                    change = np.log(curr_price/prev_price)
                    rows[date_count - 1].append(change)

                prev_price = curr_price 

            field_names.append(ticker_name)

    with open(combined_file_name, 'w') as io:
        io = csv.writer(io)
        io.writerow(field_names)
        io.writerows(rows)

valid_stocks = []
with open('valid_stocks.txt', 'r') as io:
    valid_stocks = [ticker.strip() for ticker in io.readlines()]

folder_name = 'stock_market_data/sp500/csv'
start_date = '01-01-2017'
combine_files(folder_name, 'combined_stock_data.csv', start_date, valid_stocks)

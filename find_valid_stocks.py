import csv
import os
from datetime import datetime

def find_valid_stocks(folder_name, valid_stocks_file_name, start_date):
    valid_stocks = []

    def is_date_after(a, b):   
        a_date = datetime.strptime(a, '%d-%m-%Y')
        b_date = datetime.strptime(b, '%d-%m-%Y')
        return a_date >= b_date

    file_names = os.listdir(folder_name)
    stock_count = 0
    for file_name in file_names:
        is_valid = True
        with open(folder_name + '/' + file_name) as io:
            ticker_name = file_name.split('.')[0]

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

            for row in io:
                row = row.strip().split(',')
                if row[6] == '' or row[3] == '' or row[3] == '0':
                    print(ticker_name)
                    is_valid = False
                    break
            
            if is_valid:
                valid_stocks.append(ticker_name)

    with open(valid_stocks_file_name, 'w') as io:
        for ticker in sorted(valid_stocks):
            io.write(ticker + '\n')

folder_name = 'stock_market_data/sp500/csv'
start_date = '01-01-2017'

find_valid_stocks(folder_name, 'valid_stocks.txt', start_date)

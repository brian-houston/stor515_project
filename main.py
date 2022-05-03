import json 
import numpy as np
from get_stocks_basic_info import get_stocks_basic_info
from select_random_basket import select_random_basket
from read_basket_data import read_basket_data 
from ucb import ucb
from ts import ts
from simple import simple

folder_name = 'stock_market_data/sp500/csv'
start_date = '01-01-2017'

basket = ['MSFT', 'PRU', 'DFS', 'AME', 'V', 'PH', 'PEP', 'AMP', 'BAC', 'APH', 'EMN', 'HD', 'DAL', 'EMR', 'DTE', 'DOV', 'ACN', 'ISRG', 'AMGN', 'LNC', 'CUK', 'LNT', 'COP', 'FBHS', 'MCO', 'CTXS', 'AAPL', 'AMD', 'NVDA', 'O']
data = read_basket_data(folder_name, basket, start_date, 1300)
ucb_results = ucb(data, 0.005)
ts_returns = []

for _ in range(1):
    ts_results = ts(data, 50, 0.005)
    ts_returns.append(ts_results[1])

ts_mean_return = list(np.mean(ts_returns, axis = 0))

simple_results = simple(data, 0.005)

json_wh = json.dumps(ucb_results[0]) 
with open('ucb_weights.json', 'w') as io:
    io.write(json_wh)

json_trh = json.dumps(ucb_results[1]) 
with open('ucb_returns.json', 'w') as io:
    io.write(json_trh)

json_wh = json.dumps(ts_results[0]) 
with open('ts_weights.json', 'w') as io:
    io.write(json_wh)

json_trh = json.dumps(ts_mean_return) 
with open('ts_returns.json', 'w') as io:
    io.write(json_trh)

json_wh = json.dumps(simple_results[0]) 
with open('simple_weights.json', 'w') as io:
    io.write(json_wh)

json_trh = json.dumps(simple_results[1]) 
with open('simple_returns.json', 'w') as io:
    io.write(json_trh)

from get_stocks_basic_info import get_stocks_basic_info
from select_random_basket import select_random_basket
from read_basket_data import read_basket_data 

folder_name = 'stock_market_data/sp500/csv'
start_date = '01-01-1980'

basic_info = get_stocks_basic_info(folder_name)
basket = select_random_basket(basic_info, start_date, 10)
data = read_basket_data(folder_name, basket, start_date, 10)

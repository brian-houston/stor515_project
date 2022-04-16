import random
from datetime import datetime

def select_random_basket(basic_info, start_date, K):

    # true if date a is after date b
    def is_date_after(a, b):   
        a_date = datetime.strptime(a, '%d-%m-%Y')
        b_date = datetime.strptime(b, '%d-%m-%Y')
        return a_date >= b_date

    pool = [x['ticker'] for x in basic_info if is_date_after(start_date, x['start_date'])]
    return random.choices(pool, k=K)

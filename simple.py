import numpy as np
import statistics

def simple(prices, epsilon):    
    K = len(prices)
    T = len(prices[0]) - 1

    weights = np.array([1/len(prices) for _ in range(K)])
    weights_history = [list(weights)]

    total_return = 0 
    total_return_history = [total_return]

    log_rates = [[] for _ in range(K)]
    last_period_returns = [0 for _ in range(K)]
    
    for i in range(K):
        log_rates[i] = [np.log(prices[i][t+1]/prices[i][t]) for t in range(T)]
    
    for t in range(T):
        for i in range(K):
            total_return += log_rates[i][t] * weights[i]
            last_period_returns[i] = log_rates[i][t]

        chosen_stock = np.argmax(last_period_returns)
            
        one_stock_weights = np.array([0 for w in weights])
        one_stock_weights[chosen_stock] = 1
            
        weights = epsilon * one_stock_weights + (1 - epsilon) * weights

        weights_history.append(list(weights))
        total_return_history.append(total_return)

    return [weights_history, total_return_history]

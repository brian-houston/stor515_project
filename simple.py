import numpy as np
import statistics

def simple(basket, prices, epsilon, T):    
    weights = np.array([1/len(prices) for p in prices])
    returns = [[] for p in prices]
    
    for i in range(len(prices)):
        returns[i] = [prices[i][j+1]/prices[i][j] for j in range(len(prices[i]) - 1)]
        
    for t in range(T): # change to range(T) + 1?
        last_period_returns = []
        for i in range(len(prices)):
            last_period_returns[i] = returns[i][t - 1]
        chosen_stock = np.argmax(last_period_returns)
            
        one_stock_weights = np.array([0 for w in weights])
        one_stock_weights[chosen_stock] = 1
            
        weights = epsilon * one_stock_weights + (1 - epsilon) * weights
                
    return weights
import numpy as np
import statistics

def ts(basket, prices, risk_free, epsilon, T):
    rng = np.random.default_rng(0)
    
    weights = np.array([1/len(prices) for p in prices])
    returns = [[] for p in prices]
    
    for i in range(len(prices)):
        returns[i] = [prices[i][j+1]/prices[i][j] for j in range(len(prices[i]) - 1)]
        
    phat = [0 for p in prices]
    alpha = [1 for p in prices]
    beta = [1 for p in prices]
        
    for t in range(T):
        portfolio_return = 0
        for p in range(len(prices)):
            portfolio_return += weights[p] * returns[p][t]
               
        sharpe_ratio = (portfolio_return - risk_free[t]) / statistics.stdev(portfolio_return)
            
        for p in range(len(prices)):
            phat[p] = np.random.beta(alpha[p], beta[p])
        chosen_stock = np.argmax(phat)
            
        one_stock_weights = np.array([0 for w in weights])
        one_stock_weights[chosen_stock] = 1
            
        weights = epsilon * one_stock_weights + (1 - epsilon) * weights
            
        new_portfolio_return = 0
        for p in range(len(prices)):
            new_portfolio_return += weights[p] * returns[p][t]
            
        new_sharpe_ratio = (new_portfolio_return - risk_free[t]) / statistics.stdev(new_portfolio_return)
            
        if new_sharpe_ratio > sharpe_ratio:
            alpha[chosen_stock] += 1
        else:
            beta[chosen_stock] += 1
                
    return weights
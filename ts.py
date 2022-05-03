import numpy as np

def ts(prices, window_size, epsilon):
    K = len(prices)
    T = len(prices[0]) - 1

    weights = np.array([1/len(prices) for _ in range(K)])
    weights_history = [list(weights)]

    total_return = 0 
    total_return_history = [total_return]

    log_rates = [[] for _ in range(K)]
    
    for i in range(K):
        log_rates[i] = [np.log(prices[i][t+1]/prices[i][t]) for t in range(T)]
        
    phat = [0 for _ in range(K)]
    alpha = [1 for _ in range(K)]
    beta = [1 for _ in range(K)]
    stock_returns = [0 for _ in range(K)]

    for t in range(T):
        for i in range(K):
            total_return += log_rates[i][t] * weights[i]
            phat[i] = np.random.beta(alpha[i], beta[i])
            stock_returns[i] = np.mean(log_rates[i][max(0, t - window_size):(t+1)])

        chosen_stock = np.argmax(phat)

        portfolio_return = np.sum(stock_returns * weights)
            
        one_stock_weights = np.array([0 for _ in range(K)])
        one_stock_weights[chosen_stock] = 1
            
        weights = epsilon * one_stock_weights + (1 - epsilon) * weights
            
        new_portfolio_return = np.sum(stock_returns * weights)
            
        if new_portfolio_return > portfolio_return:
            alpha[chosen_stock] += 1
        else:
            beta[chosen_stock] += 1

        weights_history.append(list(weights))
        total_return_history.append(total_return)

    return [weights_history, total_return_history]

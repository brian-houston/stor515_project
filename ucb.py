import numpy as np

def ucb(prices, epsilon):
    K = len(prices)
    T = len(prices[0]) - 1

    weights = np.array([1/len(prices) for _ in range(K)])
    weights_history = [list(weights)]

    total_return = 0
    total_return_history = [total_return]

    log_rates = [[] for _ in range(K)]
    for i in range(K):
        log_rates[i] = [np.log(prices[i][t+1]/prices[i][t]) for t in range(T)]

    rate_sums = [0 for _ in range(K)]

    for i in range(K):
        rate_sums[i] = 0 

    upper_bounds = [0 for _ in range(K)]
    number_pulls = [1 for _ in range(K)]

    for t in range(T):
        avg_rates = [np.mean(log_rates[i][:t+1]) for i in range(K)]
        avg_rate = np.mean(avg_rates)

        for i in range(K):
            total_return += log_rates[i][t] * weights[i]
            rate_sums[i] += log_rates[i][t]
            upper_bounds[i] = rate_sums[i]/(t+1) + avg_rate*np.sqrt(2*np.log(t+1)/number_pulls[i])

        chosen_arm = max(enumerate(upper_bounds), key = lambda x: x[1])[0]
        
        number_pulls[chosen_arm] += 1

        one_stock_weights = np.array([0 for _ in range(K)])
        one_stock_weights[chosen_arm] = 1

        weights = epsilon * one_stock_weights + (1 - epsilon) * weights

        weights_history.append(list(weights))
        total_return_history.append(total_return)

    return [weights_history, total_return_history]

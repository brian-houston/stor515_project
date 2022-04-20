import numpy as np
import statistics

def ucb(basket, prices, init_period, epsilon):
    weights = np.array([1/len(prices) for p in prices])
    log_rates = [[] for p in prices]

    for i in range(len(prices)):
        log_rates[i] = [np.log(prices[i][j+1]/prices[i][j]) for j in range(len(prices[i]) - 1)]

    rate_sums = [0 for p in prices]

    for i in range(len(prices)):
        rate_sums[i] = sum(log_rates[i][:init_period])

    upper_bounds = [0 for p in prices]
    number_pulls = [init_period for p in prices]
    muhat = [0 for p in prices]

    for t in range(init_period, len(log_rates[0])):
        avg_rates = [statistics.mean(log_rates[i][:t]) for i in range(len(log_rates))]
        avg_rate = statistics.mean(avg_rates)

        for j in range(len(prices)):
            upper_bounds[j] = rate_sums[j]/(t+1) + avg_rate*np.sqrt(2*np.log(t+1)/number_pulls[j])
            muhat[j] = rate_sums[j]/(t+1)

        chosen_arm = max(enumerate(upper_bounds), key = lambda x: x[1])[0]
        
        for i in range(len(rate_sums)):
            rate_sums[i] += log_rates[i][t]
        number_pulls[chosen_arm] += 1

        one_stock_weights = np.array([0 for w in weights])
        one_stock_weights[chosen_arm] = 1

        weights = epsilon * one_stock_weights + (1 - epsilon) * weights

    return weights


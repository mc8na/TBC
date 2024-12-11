# (1)
# Complete the sequence_calculator function, which should
# Return the n-th number of the sequence S_n, defined as:
# S_n = 3*S_(n-1) - S_(n-2), with S_0 = 0 and S_1 = 1.
# Your solution must use constant space (i.e., the space 
# used by the function should not grow with n).
# Your implementation should minimize the execution time.
#
# (2)
# Find the time complexity of the proposed solution, using
# the "Big O" notation, and explain in detail why such
# complexity is obtained, for n ranging from 0 to at least
# 100000. HINT: you are dealing with very large numbers!
#
# (3)
# Plot the execution time VS n (again, for n ranging from 0
# to at least 100000).
#
# (4)
# Confirm that the empirically obtained time complexity curve
# from (3) matches the claimed time complexity from (2) (e.g.
# by using curve fitting techniques).

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Complete the sequence_calulator function to return the n-th
# number of the sequence S_n.
def sequence_calculator(n):
    # input must be a positive integer, if negative return None
    if (n < 0):
        return None
    # S_0 = 0 and S_1 = 1, so simply return n if n is 0 or 1
    if (n < 2):
        return n
    # values used to calculate subsequent numbers in the sequence to
    # minimize execution time. Only store the two values required for
    # the next calculation to use constant space
    S_n_minus_2 = 0 # S_(n-2) = S_0 = 0
    S_n_minus_1 = 1 # S_(n-1) = S_1 = 1
    # calculate the numbers in the sequence, starting with S_2
    for i in range(1,n):
        S_n = 3 * S_n_minus_1 - S_n_minus_2 # formula: S_n = 3*S_(n-1) - S_(n-2)
        S_n_minus_2 = S_n_minus_1 # update S_(n-2) = S_(n-1) for next round
        S_n_minus_1 = S_n # update S_(n-1) = S_n for next round
    # return the result
    return S_n

# (2) At first glance, the solution appears to have time complexity O(n) since
# there is a single loop ranging from 1 to n, and a single calculation is performed
# at each iteration, along with two constant assignments. The calculation of S_n
# is not constant time, however, since it depends on how large S_(n-1) and S_(n-2)
# are, since the more bits those numbers have the more work is required to calculate
# the next number in the sequence. Since S_n = 3*S_(n-1) - S_(n-2), the work required
# for the calculation is proportional to the size of S_(n-1) and S_(n-2), and thus to
# n, meaning n work is required at each iteration. Since we iterate over n, our
# solution's time complexity is thus O(n^2).

# Empirically measure the execution time for n ranging from 0 to 100000
n_values = range(0, 100001, 5000)  
execution_times = []

for n in n_values: # Measure at intervals of 5000 for efficiency
    start_time = time.time()
    sequence_calculator(n)
    end_time = time.time()
    # measure the time required to calculate the n-th number in the sequence
    execution_times.append(end_time - start_time)

# Convert lists to numpy arrays to peform curve fitting
n_values_array = np.array(n_values)
execution_times_array = np.array(execution_times)

# Define models
def linear_model(n, a, b):
    return a * n + b

def quadratic_model(n, a, b, c):
    return a * n**2 + b * n + c

# Perform linear fit
linear_params, linear_covariance = curve_fit(linear_model, n_values_array, execution_times_array)
a_linear, b_linear = linear_params
fitted_linear_times = linear_model(n_values_array, a_linear, b_linear)

# Perform quadratic fit
quad_params, quad_covariance = curve_fit(quadratic_model, n_values_array, execution_times_array)
a_quad, b_quad, c_quad = quad_params
fitted_quad_times = quadratic_model(n_values_array, a_quad, b_quad, c_quad)

# Calculate R^2 values
# Linear model
residuals_linear = execution_times_array - fitted_linear_times
ss_res_linear = np.sum(residuals_linear**2)
ss_tot_linear = np.sum((execution_times_array - np.mean(execution_times_array))**2)
r_squared_linear = 1 - (ss_res_linear / ss_tot_linear)

# Quadratic model
residuals_quad = execution_times_array - fitted_quad_times
ss_res_quad = np.sum(residuals_quad**2)
ss_tot_quad = np.sum((execution_times_array - np.mean(execution_times_array))**2)
r_squared_quad = 1 - (ss_res_quad / ss_tot_quad)

# Plot Linear Fit
plt.figure(figsize=(10, 6))
plt.plot(n_values_array, execution_times_array, 'o', label='Empirical Data', markersize=6)
plt.plot(n_values_array, fitted_linear_times, '-', label=f'Linear Fit: T(n) = {a_linear:.2e} * n + {b_linear:.2e}', linewidth=2)
plt.title(f'Linear Fit (R² = {r_squared_linear:.3f})')
plt.xlabel('n')
plt.ylabel('Execution Time (seconds)')
plt.grid(True)
plt.legend()

# Plot Quadratic Fit
plt.figure(figsize=(10, 6))
plt.plot(n_values_array, execution_times_array, 'o', label='Empirical Data', markersize=6)
plt.plot(n_values_array, fitted_quad_times, '-', label=f'Quadratic Fit: T(n) = {a_quad:.2e} * n^2 + {b_quad:.2e} * n + {c_quad:.2e}', linewidth=2)
plt.title(f'Quadratic Fit (R² = {r_squared_quad:.3f})')
plt.xlabel('n')
plt.ylabel('Execution Time (seconds)')
plt.grid(True)
plt.legend()
plt.show()

# From the graphs generated above, we can see that the linear O(n) model is a fairly good
# fit for our empirical time complexity, with an R^2 value between 0.938 and 0.947. From the
# graph though, we can see that the empirical data have more of a curved aspect, so we compare
# the quadratic model to the data to see that this gives us a much better fit, with an R^2
# between 0.996 and 1. A perfect fit would give us R^2 = 1, so this tells us that the quadratic
# model is indeed the correct fit for our time complexity of O(n^2).


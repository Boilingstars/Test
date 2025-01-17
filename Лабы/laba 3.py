import numpy as np
from math import sqrt

data = {1: [0.00039, 0.00047, 0.0004, 0.00057, 0.00044],
        2: [0.00018, 0.00007, 0.00007, 0.00012, 0.00017],}

L = {1: 0.5028,
     2: 0.5038}

b = {1: 0.02,
     2: 0.01}

a = {1: 0.0014,
     2: 0.0034}

delta = {}
sum_dict = {}
error_rate = {}

k_values = {}

def calc(key):
    sum = 0
    sqr_sum = 0

    k_val = []

    for i in data[key]:
        k = (0.49 * (L[key]**3)) / (4 * i * (a[key]**3) * b[key])

        k_val.append(k)

        sum += 1/5 * k

    k_values[key] = k_val

    sum_dict[key] = sum

    for j in k_values[key]:
        sqr_sum += (j - sum)**2

    delta[key] = 2.13 * sqrt(sqr_sum/20)
    error_rate[key] = 2.13 * sqrt(sqr_sum/6) / sum * 100


for i in range(1, 3):
    calc(i)

print('\n'.join("{}: {}".format(k, v) for k, v in k_values.items()), '\n',
      'Икс с чертой', '\n', '\n'.join("{}: {}".format(k, v) for k, v in sum_dict.items()), '\n', 
      'Дельта -----------', '\n','\n'.join("{}: {}".format(k, v) for k, v in delta.items()), '\n', 
      'Относительная погрешность =', '\n','\n'.join("{}: {}".format(k, v) for k, v in error_rate.items())
      )

input()
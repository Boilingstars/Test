import numpy as np
from math import sqrt

data = {1: [63757.3, 62382.13, 63096.1, 62083.8, 64232.5],
        2: [24853.4, 23715.19, 21233.5, 22177.14, 21927.12]}

delta = {}
sum_dict = {}
error_rate = {}

def calc(key):
    sum = 0
    sqr_sum = 0

    for i in data[key]:
        sum += 1/5 * i

    sum_dict[key] = sum

    for j in data[key]:
        sqr_sum += (j - sum)**2

    delta[key] = 2.13 * sqrt(sqr_sum/20)
    error_rate[key] = 2.13 * sqrt(sqr_sum/6) / sum * 100


for i in range(1, 3):
    calc(i)

print(
      'Икс с чертой', '\n', '\n'.join("{}: {}".format(k, v) for k, v in sum_dict.items()), '\n', 
      'Дельта -----------', '\n','\n'.join("{}: {}".format(k, v) for k, v in delta.items()), '\n', 
      'Относительная погрешность =', '\n','\n'.join("{}: {}".format(k, v) for k, v in error_rate.items())
      )

input()
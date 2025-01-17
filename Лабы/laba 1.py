import numpy as np
from math import sqrt

data = {1: [9.68, 9.71, 9.63, 9.78, 9.85]}
h = 5

delta = {}
sum_dict = {}
error_rate = {}

def calc(key):
    sum = 0
    sqr_sum = 0  

    for i in data[key]:
        sum += 1/h * i

    sum_dict[key] = sum

    for j in data[key]:
        sqr_sum += (j - sum)**2

    delta[key] = 2.78 * sqrt(sqr_sum/(h*(h-1)))
    error_rate[key] = (delta[key] / sum) * 100

calc(1)

print(
      'Икс с чертой', '\n', '\n'.join("{}: {}".format(k, v) for k, v in sum_dict.items()), '\n', 
      'Дельта -----------', '\n','\n'.join("{}: {}".format(k, v) for k, v in delta.items()), '\n', 
      'Абсолютная погрешность =', '\n','\n'.join("{}: {}".format(k, v) for k, v in error_rate.items())
      )

input()
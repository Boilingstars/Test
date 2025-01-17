import numpy as np
from math import sqrt

data = {1: [57, 64, 60],
        2: [67, 65, 66],
        3: [81, 83, 78],
        4: [3, 2.9, 2.7]}

delta = {}
sum_dict = {}
error_rate = {}

lenghts = {}
angels = {}

def calc(key):
    sum = 0
    sqr_sum = 0
    lenghts_val = []
    angels_val = []

    for i in data[key]:
        angel = 4.74 * i / 12.42
        lenght = 6400 * angel / 0.006389 

        angels_val.append(angel)
        lenghts_val.append(lenght)

        sum += 1/3 * lenght

    lenghts[key] = lenghts_val
    angels[key] = angels_val

    sum_dict[key] = sum

    for j in lenghts[key]:
        sqr_sum += (j - sum)**2

    delta[key] = 2.92 * sqrt(sqr_sum/6)
    error_rate[key] = 2.92 * sqrt(sqr_sum/6) / sum * 100


for i in range(1, 5):
    calc(i)

print('\n'.join("{}: {}".format(k, v) for k, v in lenghts.items()), '\n',
      '\n'.join("{}: {}".format(k, v) for k, v in angels.items()), '\n', 
      'Икс с чертой', '\n', '\n'.join("{}: {}".format(k, v) for k, v in sum_dict.items()), '\n', 
      'Дельта -----------', '\n','\n'.join("{}: {}".format(k, v) for k, v in delta.items()), '\n', 
      'Относительная погрешность =', '\n','\n'.join("{}: {}".format(k, v) for k, v in error_rate.items())
      )

input()
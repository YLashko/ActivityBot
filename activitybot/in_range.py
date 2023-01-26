import numpy as np
from time import time

SIZE = 10000
LOW = 0
HIGH = 10000

def in_range_gpt(start, end, i):
    return i in range(start, end+1)

def in_range(start, end, i):
    return start <= i <= end

random_low = np.random.randint(LOW, HIGH, size=SIZE)
random_high = random_low + np.random.randint(LOW, HIGH, size=SIZE)
random_check = np.random.randint(LOW, HIGH * 2, size=SIZE)

t = time()
for i in range(SIZE):
    in_range(random_low[i], random_high[i], random_check[i])
a = time() - t
print(a)

t = time()
for i in range(SIZE):
    in_range_gpt(random_low[i], random_high[i], random_check[i])
b = time() - t
print(b)
print(b / a)

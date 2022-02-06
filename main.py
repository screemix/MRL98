from mrl98 import *
from streaming import Stream
import numpy as np


b = 50
k = 12
n = 5000000
q = 0.1
buffers = [Buffer(k, 0) for i in range(b)]

for i in range(b):
    new_operation(buffers[i], [0, 1, 2, 4, 7])

# print(buffers)
# new_buffers = [buffers[i] for i in range(b) if i % 2 == 0]
# collapse_operation(new_buffers)
# print(buffers)
# print(buffers[0])

# # print(buffers[1])

stream = Stream(k, n)
print(munro_paterson(b, k, q, stream))

stream = Stream(k, n)
print(mrl98_new(b, k, q, stream))

from operations import *
from streaming import Stream
from mrl98_new_algorithm import mrl98_new
from munro_paterson import munro_paterson
import numpy as np


b = 5
k = 4
n = 100
q = 0.25
# buffers = [Buffer(k, 4) for i in range(b)]
#
# for i in range(b):
#     new_operation(buffers[i], [0, 1, 2, 4, 7])

# print(buffers[0], buffers[1])
# merge_sequences([buffers[0], buffers[1]])

stream = Stream(k, n)
# print(munro_paterson(b, k, q, stream))

# stream = Stream(k, n)
print(mrl98_new(b, k, q, stream))

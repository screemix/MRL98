from streaming import Stream
from mrl98_new_algorithm import mrl98_new
from munro_paterson import munro_paterson
from tests import *
from graphs import *

# b = 5
# k = 5495
# n = 10**5
# q = 1/16
#
#
# # stream = Stream(k, n)
# # # print(munro_paterson(b, k, q, stream,  test_mode=True))
# #
# # # stream = Stream(k, n)
# # # print(mrl98_new(b, k, q, stream, test_mode=True))


plot_times([100, 1000, 100000, 100000, 1000000], [1, 2, 3, 4, 5], [0.1, 0.2, 0.5, 0.5, 0.5])

plot_memory_consumption([100, 1000, 100000, 100000, 1000000], [1, 2, 3, 4, 5], [0.1, 0.2, 0.5, 0.5, 0.5])
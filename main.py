from mrl98 import *

b = 10
k = 5
buffers = [Buffer(k, 0) for i in range(b)]

for i in range(b):
    new_operation(buffers[i], [0, 1, 2, 4, 7])

print(collapse_operation([buffers[0], buffers[1]]))
# print(buffers[0])

# print(buffers[1])
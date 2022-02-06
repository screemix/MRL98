import random
import numpy as np
random.seed(42)


class Stream:
    def __init__(self, k, n=None):
        self.n = np.inf if n is None else n
        self.k = k

    def stream_k_values(self):
        while self.n > 0:
            next_values_len = self.k if (self.n // self.k > 0 or self.n == np.inf) else self.n
            next_values = [random.randint(1, 100) for _ in range(next_values_len)]
            self.n -= next_values_len
            yield next_values


# new_stream = Stream(6, 100)
# for seq in new_stream.stream_k_values():
#     print(seq)

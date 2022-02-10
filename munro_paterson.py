from operations import Buffer, new_operation, collapse_operation,\
    output_operation, rank, calculate_error
from streaming import Stream
import numpy as np
from math import ceil
import sys


def munro_paterson(b: int, k: int, q: float, stream: Stream, test_mode=False) -> int:
    buffers = [Buffer(k, 0, False, []) for i in range(b)]
    big_seq = []
    max_mem = 0

    try:
        while True:
            empty = [i for i in range(b) if buffers[i].label is False]
            full = [i for i in range(b) if buffers[i].label is True]

            if len(empty) > 0:
                seq = next(stream.stream_k_values())
                new_operation(buffers[empty[0]], seq)
                if test_mode:
                    big_seq += seq
                    mem = sys.getsizeof(buffers)
                    max_mem = max(max_mem, mem)

            else:
                weights = [buffers[i].weight for i in full]
                seen = []
                for i, w in enumerate(weights):
                    if w in seen:
                        i1 = full[i]
                        i2 = full[seen.index(w)]
                    else:
                        seen.append(w)
                collapse_operation([buffers[i1], buffers[i2]])

    except StopIteration:
        full_buffers = [buffers[i] for i in full]
        result = output_operation(full_buffers, q)

        if test_mode:
            mem = sys.getsizeof(buffers)
            max_mem = max(max_mem, mem)
            real_quantile = big_seq[ceil(q*len(big_seq)) - 1]
            big_seq.sort()

            real_rank, N = rank(big_seq, real_quantile)
            observed_rank, N = rank(big_seq, result)
            e = calculate_error(real_rank, observed_rank, N)
            return result, e, max_mem
            # print(np.quantile(big_seq, q))

        return result
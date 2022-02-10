from operations import Buffer, new_operation, collapse_operation, output_operation, \
    rank, calculate_error
from streaming import Stream
import numpy as np
from math import ceil
import s

def mrl98_new(b: int, k: int, q: float, stream: Stream, test_mode=False) -> int:
    buffers = [Buffer(k, 0, False, []) for i in range(b)]
    big_seq = []
    max_mem = 0

    try:

        while True:
            empty = [i for i in range(b) if buffers[i].label is False]
            full = [i for i in range(b) if buffers[i].label is True]

            if len(empty) > 1:
                for i in empty:
                    seq = next(stream.stream_k_values())
                    new_operation(buffers[i], seq)
                    buffers[i].level = 0

                    if test_mode:
                        big_seq += seq
                        mem = sys.getsizeof(buffers)
                        max_mem = max(max_mem, mem)

            elif len(empty) == 1:
                seq = next(stream.stream_k_values())
                l = min([buffers[i].level for i in full])
                new_operation(buffers[empty[0]], seq)
                buffers[empty[0]].level = l

                if test_mode:
                    big_seq += seq
                    mem = sys.getsizeof(buffers)
                    max_mem = max(max_mem, mem)

            else:
                l = min([buffers[i].level for i in full])
                buf_idx_l = [i for i in range(b) if buffers[i].level == l]
                collapse_operation([buf for buf in buffers if buf.level == l])
                buffers[buf_idx_l[0]].level = l+1

    except StopIteration:
        full_buffers = [buffers[i] for i in range(b) if buffers[i].label is True]
        result = output_operation(full_buffers, q)

        if test_mode:
            mem = sys.getsizeof(buffers)
            max_mem = max(max_mem, mem)
            big_seq.sort()
            real_quantile = big_seq[ceil(q * len(big_seq)) - 1]


            real_rank, N = rank(big_seq, real_quantile)
            observed_rank, N = rank(big_seq, result)
            e = calculate_error(real_rank, observed_rank, N)
            # print(np.quantile(big_seq, q))
            # print(real_quantile)
            return result, e, max_mem


        return result
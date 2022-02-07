from operations import Buffer, new_operation, collapse_operation, output_operation
from streaming import Stream
import numpy as np


def mrl98_new(b: int, k: int, q: float, stream: Stream) -> int:
    buffers = [Buffer(k, 0, False, []) for i in range(b)]
    big_seq = []

    try:

        while True:
            empty = [i for i in range(b) if buffers[i].label is False]
            full = [i for i in range(b) if buffers[i].label is True]

            if len(empty) > 1:
                for i in empty:
                    seq = next(stream.stream_k_values())
                    new_operation(buffers[i], seq)
                    buffers[i].level = 0
                    big_seq += seq

            elif len(empty) == 1:
                seq = next(stream.stream_k_values())
                l = min([buffers[i].level for i in full])
                new_operation(buffers[empty[0]], seq)
                buffers[empty[0]].level = l
                big_seq += seq

            else:
                l = min([buffers[i].level for i in full])
                buf_idx_l = [i for i in range(b) if buffers[i].level == l]
                collapse_operation([buf for buf in buffers if buf.level == l])
                buffers[buf_idx_l[0]].level = l+1

    except StopIteration:
        full_buffers = [buffers[i] for i in range(b) if buffers[i].label is True]
        # big_seq.sort()
        print(np.quantile(big_seq, q))
        return output_operation(full_buffers, q)
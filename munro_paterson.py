from operations import Buffer, new_operation, collapse_operation, output_operation
from streaming import Stream
import numpy as np


def munro_paterson(b: int, k: int, q: float, stream: Stream) -> int:
    buffers = [Buffer(k, 0, False, []) for i in range(b)]
    big_seq = []
    try:
        while True:
            empty = [i for i in range(b) if buffers[i].label is False]
            full = [i for i in range(b) if buffers[i].label is True]

            if len(empty) > 0:
                seq = next(stream.stream_k_values())
                new_operation(buffers[empty[0]], seq)
                big_seq += seq

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
        big_seq.sort()
        # print(big_seq)
        print(np.quantile(big_seq, q))
        return output_operation(full_buffers, q)
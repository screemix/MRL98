import numpy as np
from math import ceil
from streaming import Stream


class Buffer:
    def __init__(self, k, w, label=False, seq=[]):
        self.k = k
        self.weight = w
        # whether empty or full, False in case of empty
        self.label = label
        self.seq = seq

    def __repr__(self):
        contain = "Full" if self.label else "Empty"
        return "{} buffer with k={}, weight={}, seq={}".format(contain, self.k, self.weight, self.seq)


def new_operation(b: Buffer, seq: list):
    if len(seq) < b.k:
        rem = int((b.k - len(seq) + 1) / 2)
        b.seq = seq[:] + [np.Inf] * rem + [np.NINF] * rem
    else:
        b.seq = seq[:b.k]
    b.label = True
    b.weight = 1


def collapse_operation(buffers: list[Buffer]):
    k = buffers[0].k
    w = sum([b.weight for b in buffers])

    bucket = sum([b.seq*b.weight for b in buffers], [])
    # print("bucket ", bucket)
    bucket.sort()
    # print("sorted bucket ", bucket)

    offset = int((w + 1) / 2)
    # print("offset: ", offset)
    new_seq = []
    for i in range(k):
        position = i*w + offset + (w % 2) * (i % 2)
        # print((w % 2) * (i % 2), position)
        new_seq.append(bucket[position])

    y = Buffer(k, w, label=True, seq=new_seq)
    # print(y.seq, y.k, y.weight)

    for b in buffers:
        b.weight, b.label, b.seq = 0, False, []
    buffers[0] = y


def output_operation(buffers: list[Buffer], quantile: float):
    w = sum([b.weight for b in buffers])
    k = buffers[0].k

    bucket = sum([b.seq * b.weight for b in buffers], [])
    bucket.sort()

    position = ceil(k*w*quantile)
    return bucket[position]


def munro_paterson(b: int, k: int, q: float, stream: Stream) -> int:
    buffers = [Buffer(k, 0, False, []) for i in range(b)]
    empty = [i for i in range(b)]
    full = []
    big_seq = []
    try:
        while True:

            if len(empty) > 0:
                seq = next(stream.stream_k_values())
                new_operation(buffers[empty[0]], seq)
                full.append(empty[0])
                empty.pop(0)
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
                empty.append(i2)

    except StopIteration:
        full_buffers = [buffers[i] for i in full]
        big_seq.sort()
        print(big_seq)
        print(np.quantile(big_seq, q))
        return output_operation(full_buffers, q)


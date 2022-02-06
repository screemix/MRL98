import numpy as np
from math import ceil


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
        b.weight, b.label, b.seq = 1, False, []
    buffers[0] = y
    return buffers


def output_operation(buffers: list[Buffer], quantile: float):
    w = sum([b.weight for b in buffers])
    k = buffers[0].k

    bucket = sum([b.seq * b.weight for b in buffers], [])
    bucket.sort()

    position = ceil(k*w*quantile)
    return bucket[position]


def munro_paterson():
    pass
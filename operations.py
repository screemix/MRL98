import numpy as np
from math import ceil, floor
from streaming import Stream


class Buffer:
    def __init__(self, k, w, label=False, seq=[], level=None):
        self.k = k
        self.weight = w
        # whether empty or full, False in case of empty
        self.label = label
        self.seq = seq
        self.level = level

    def __repr__(self):
        contain = "Full" if self.label else "Empty"
        repr_str = "{} buffer with k={}, weight={}, seq={}".format(contain, self.k, self.weight, self.seq)
        if self.level is not None:
            repr_str += ", level={}".format(self.level)
        return repr_str


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
    bucket.sort()

    offset = (w + 1) / 2 if w % 2 == 1 else w / 2
    new_seq = []
    for i in range(k):
        position = i*w + int(offset) + (not(w % 2)) * (i % 2) - 1
        # position = i * w + int(offset)
        # print((w % 2) * (i % 2), position)
        new_seq.append(bucket[position])

    y = Buffer(k, w, label=True, seq=new_seq)
    # print(y.seq, y.k, y.weight)

    buffers[0] = y
    for b in buffers[1:]:
        b.weight, b.label, b.seq = 0, False, []


def output_operation(buffers: list[Buffer], quantile: float):
    w = sum([b.weight for b in buffers])
    k = buffers[0].k

    bucket = sum([b.seq * b.weight for b in buffers], [])
    bucket.sort()

    position = ceil(k*w*quantile)
    return bucket[position]



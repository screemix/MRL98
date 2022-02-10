import numpy as np
from math import ceil, floor
from streaming import Stream

def rank(a, elem: int):
    elems = list(set(a))
    elems.sort()
    return elems.index(elem), len(elems)

def calculate_error(real_rank: int, observed_rank: int, N: int):
    return abs(real_rank - observed_rank) / N

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


def merge_sequences(buffers):
    w = sum([b.weight for b in buffers])
    offset = (w + 1) / 2 if w % 2 == 1 else w / 2
    buf_num = len(buffers)
    k = buffers[0].k

    sequences = []
    for buf in buffers:
        seq = buf.seq.copy()
        seq.sort()
        sequences.append(seq)
    counter = 0
    result_seq = []
    cur_ind = [0 for _ in range(buf_num)]

    cur_values = [sequences[j][cur_ind[j]] for j in range(buf_num) if cur_ind[j] < k]
    i = 0

    while i < k:
        position = i * w + int(offset) + (not (w % 2)) * (i % 2)
        # position = i * w + int(offset)
        cur_values = [sequences[j][cur_ind[j]] for j in range(buf_num) if cur_ind[j] < k]

        min_value = min(cur_values)
        min_index = cur_values.index(min_value)
        cur_ind[min_index] += 1
        counter += buffers[min_index].weight
        if counter >= position:
            result_seq.append(min_value)
            i += 1

    return result_seq, w


def collapse_operation(buffers):

    k = buffers[0].k

    bucket = sum([b.seq*b.weight for b in buffers], [])
    bucket.sort()

    # previous version, require materializing of each object
    # w = sum([b.weight for b in buffers])
    # offset = (w + 1) / 2 if w % 2 == 1 else w / 2
    # new_seq = []
    # for i in range(k):
    #     position = i*w + int(offset) + (not(w % 2)) * (i % 2) - 1
    #     # position = i * w + int(offset)
    #     # print((w % 2) * (i % 2), position)
    #     new_seq.append(bucket[position])

    new_seq, w = merge_sequences(buffers)
    y = Buffer(k, w, label=True, seq=new_seq)
    # print(y.seq, y.k, y.weight)

    buffers[0] = y
    for b in buffers[1:]:
        b.weight, b.label, b.seq = 0, False, []


def output_operation(buffers, quantile: float):
    w = sum([b.weight for b in buffers])
    k = buffers[0].k

    bucket = sum([b.seq * b.weight for b in buffers], [])
    bucket.sort()

    position = ceil(k*w*quantile) - 1
    return bucket[position]



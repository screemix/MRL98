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
    # print("bucket ", bucket)
    bucket.sort()
    # print("sorted bucket ", bucket)

    offset = (w + 1) / 2 if w % 2 == 1 else w / 2
    # print("offset: ", offset)
    new_seq = []
    for i in range(k):
        # position = i*w + int(offset) + (w % 2 == 0) * (i % 2)*2
        position = i * w + int(offset)
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
        print(big_seq)
        print(np.quantile(big_seq, q))
        return output_operation(full_buffers, q)


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
                buf_idx_l = [i for i in range(b) if buffers[i].level==l]
                collapse_operation([buf for buf in buffers if buf.level == l])
                buffers[buf_idx_l[0]].level = l+1



    except StopIteration:
        full_buffers = [buffers[i] for i in range(b) if buffers[i].label is True]
        big_seq.sort()

        return output_operation(full_buffers, q)
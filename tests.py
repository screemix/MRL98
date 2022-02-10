from streaming import Stream
from mrl98_new_algorithm import mrl98_new
from munro_paterson import munro_paterson
import numpy as np
import pandas as pd
from tqdm import tqdm
import time


# mrl_k_1 = {10 ** 5: 55, int((10 ** 5) * 1.5): 55, 10 ** 6: 54, int((10 ** 6) * 1.5): 54,
#              10 ** 7: 60, int((10 ** 7) * 1.5): 60}
# mrl_b_1 = {10 ** 5: 5, int((10 ** 5) * 1.5): 5, 10 ** 6: 7, int((10 ** 6) * 1.5): 7,
#              10 ** 7: 10, int((10 ** 7) * 1.5): 15}
#
# mrl_k_01 = {10 ** 5: 217, int((10 ** 5) * 1.5): 217, 10 ** 6: 229, int((10 ** 6) * 1.5): 229,
#              10 ** 7: 412, int((10 ** 7) * 1.5): 412}
# mrl_b_01 = {10 ** 5: 7, int((10 ** 5) * 1.5): 7, 10 ** 6: 12, int((10 ** 6) * 1.5): 12,
#              10 ** 7: 9, int((10 ** 7) * 1.5): 9}

mrl_k_001 = {10 ** 5: 2778, int((10 ** 5) * 1.5): 2778, 10 ** 6: 3031, int((10 ** 6) * 1.5): 3031,
             10 ** 7: 5495, int((10 ** 7) * 1.5): 5495}
mrl_b_001 = {10 ** 5: 3, int((10 ** 5) * 1.5): 3, 10 ** 6: 5, int((10 ** 6) * 1.5): 5,
             10 ** 7: 5, int((10 ** 7) * 1.5): 5}

munro_k_001 = {10 ** 5: 3125, int((10 ** 5) * 1.5): 3125, 10 ** 6: 3907, int((10 ** 6) * 1.5): 3907,
               10 ** 7: 9766, int((10 ** 7) * 1.5): 9766}
munro_b_001 = {10 ** 5: 6, int((10 ** 5) * 1.5): 6, 10 ** 6: 9, int((10 ** 6) * 1.5): 9, 10 ** 7: 11,
               int((10 ** 7) * 1.5): 11}


def test_e_mrl_98_new():
    mrl_k_001 = {10**5: 2778, 10**6: 3031, 10**7: 5495}
    mrl_b_001 = {10**5: 3, 10**6: 5, 10**7: 5}
    errors = dict()
    errors["q"] = [i for i in range(1, 16)]
    errors.update({n: [] for n in mrl_b_001.keys()})

    for n in mrl_b_001.keys():
        k = mrl_k_001[n]
        b = mrl_b_001[n]
        for q in tqdm(range(1, 16)):
            stream = Stream(k, int(n))
            _, e, _ = mrl98_new(b, k, 1/q, stream, test_mode=True)
            errors[n].append(e)
    df = pd.DataFrame(errors)
    df.to_csv("observed_e.csv")


def test_time_mrl_98_vs_munro_paterson():

    time_mrl = []
    time_munro = []

    for n in tqdm(mrl_k_001.keys()):
        stream = Stream(mrl_k_001[n], n, seed=42)
        start_time = time.time()
        _, _, _ = mrl98_new(mrl_b_001[n], mrl_k_001[n], 0.5, stream, test_mode=True)
        time_mrl.append(time.time() - start_time)

        stream = Stream(munro_k_001[n], n, seed=7)
        start_time = time.time()
        _, _, _ = munro_paterson(munro_b_001[n], munro_k_001[n], 0.5, stream, test_mode=True)
        time_munro.append(time.time() - start_time)

    return time_mrl, time_munro

def test_memory_mrl_98_vs_munro_paterson():

    mem_mrl = []
    mem_munro = []

    for n in tqdm(mrl_k_001.keys()):

        stream = Stream(mrl_k_001[n], n, seed=42)
        _, _, mem = mrl98_new(mrl_b_001[n], mrl_k_001[n], 0.5, stream, test_mode=True)
        mem_mrl.append(mem)

        stream = Stream(int(munro_k_001[n]), n, seed=7)
        _, _, mem = munro_paterson(munro_b_001[n], munro_k_001[n], 0.5, stream, test_mode=True)
        mem_munro.append(mem)

    return mem_mrl, mem_munro

def test_time_over_error():
    errors = {0.1: [], 0.01: [], 0.001: []}
    for error, ks, bs in [(0.1, mrl_k_1, mrl_b_1), (0.01, mrl_k_01, mrl_b_01), (0.001, mrl_k_001, mrl_b_001)]:
        for n in tqdm(ks.keys()):
            stream = Stream(ks[n], n, seed=42)
            start_time = time.time()
            _, _, mem = mrl98_new(bs[n], ks[n], 0.5, stream, test_mode=True)
            errors[error].append(time.time() - start_time)

    return errors
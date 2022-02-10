from streaming import Stream
from mrl98_new_algorithm import mrl98_new
from munro_paterson import munro_paterson
import numpy as np
import pandas as pd
from tqdm import tqdm
import time

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

    ns = [10**i for i in range(4, 9)]
    time_mrl = []
    time_munro = []
    b = 15
    k = 100

    for n in tqdm(ns):
        stream = Stream(k, n, seed=42)
        start_time = time.time()
        _, _, _ = mrl98_new(b, k, 0.5, stream, test_mode=True)
        time_mrl.append(time.time() - start_time)

        stream = Stream(k, n, seed=7)
        start_time = time.time()
        _, _, _ = munro_paterson(b, k, 0.5, stream, test_mode=True)
        time_munro.append(time.time() - start_time)

    return time_mrl, time_munro


def test_time_mrl_98_vs_munro_paterson():

    ns = [10**i for i in range(4, 9)]
    time_mrl = []
    time_munro = []
    b = 15
    k = 100

    for n in tqdm(ns):
        stream = Stream(k, n, seed=42)
        start_time = time.time()
        _, _, _ = mrl98_new(b, k, 0.5, stream, test_mode=True)
        time_mrl.append(time.time() - start_time)

        stream = Stream(k, n, seed=7)
        start_time = time.time()
        _, _, _ = munro_paterson(b, k, 0.5, stream, test_mode=True)
        time_munro.append(time.time() - start_time)

    return time_mrl, time_munro

def test_time_mrl_98_vs_munro_paterson():

    mrl_k_001 = {10 ** 5: 2778, (10 ** 5) * 1.5: 2778, 10 ** 6: 3031, (10 ** 6) * 1.5: 3031, 10 ** 7: 5495, (10 ** 7) * 1.5: 5495}
    mrl_b_001 = {10 ** 5: 3, (10 ** 5) * 1.5: 3, 10 ** 6: 5, (10 ** 6) * 1.5: 5, 10 ** 7: 5, (10 ** 7) * 1.5: 5}

    munro_k_001 = {10 ** 5: 3125, (10 ** 5) * 1.5: 3125, 10 ** 6: 3907, (10 ** 6) * 1.5: 3907, 10 ** 7: 9766, (10 ** 7) * 1.5: 9766}
    munro_b_001 = {10 ** 5: 6, (10 ** 5) * 1.5: 6, 10 ** 6: 9, (10 ** 6) * 1.5: 9, 10 ** 7: 11, (10 ** 7) * 1.5: 11}

    time_mrl = []
    time_munro = []
    b = 15
    k = 100

    for n in tqdm(mrl_k_001.keys()):
        stream = Stream(k, n, seed=42)
        start_time = time.time()
        _, _, _ = mrl98_new(mrl_b_001[n], mrl_k_001[n], 0.5, stream, test_mode=True)
        time_mrl.append(time.time() - start_time)

        stream = Stream(k, n, seed=7)
        start_time = time.time()
        _, _, _ = munro_paterson(munro_b_001[n], munro_k_001[n], 0.5, stream, test_mode=True)
        time_munro.append(time.time() - start_time)

    return time_mrl, time_munro

def test_memory_mrl_98_vs_munro_paterson():

    mrl_k_001 = {10 ** 5: 2778, (10 ** 5) * 1.5: 2778, 10 ** 6: 3031, (10 ** 6) * 1.5: 3031, 10 ** 7: 5495, (10 ** 7) * 1.5: 5495}
    mrl_b_001 = {10 ** 5: 3, (10 ** 5) * 1.5: 3, 10 ** 6: 5, (10 ** 6) * 1.5: 5, 10 ** 7: 5, (10 ** 7) * 1.5: 5}

    munro_k_001 = {10 ** 5: 3125, (10 ** 5) * 1.5: 3125, 10 ** 6: 3907, (10 ** 6) * 1.5: 3907, 10 ** 7: 9766, (10 ** 7) * 1.5: 9766}
    munro_b_001 = {10 ** 5: 6, (10 ** 5) * 1.5: 6, 10 ** 6: 9, (10 ** 6) * 1.5: 9, 10 ** 7: 11, (10 ** 7) * 1.5: 11}

    mem_mrl = []
    mem_munro = []

    _, _, mem = mrl98_new(mrl_b_001[n], mrl_k_001[n], 0.5, stream, test_mode=True)
    mem_mrl.append(time.time() - start_time)


    stream = Stream(k, n, seed=7)
    _, _, mem = munro_paterson(munro_b_001[n], munro_k_001[n], 0.5, stream, test_mode=True)
    mem_munro.append(mem)

    return mem_mrl, mem_murlo


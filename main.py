from streaming import Stream
from mrl98_new_algorithm import mrl98_new
from munro_paterson import munro_paterson
import numpy as np
import pandas as pd
from tqdm import tqdm

b = 5
k = 5495
n = 10**5
q = 1/16


# stream = Stream(k, n)
# # print(munro_paterson(b, k, q, stream,  test_mode=True))
#
# # stream = Stream(k, n)
# # print(mrl98_new(b, k, q, stream, test_mode=True))


def test_mrl_98_new():
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
            _, e = mrl98_new(b, k, 1/q, stream, test_mode=True)
            errors[n].append(e)
    df = pd.DataFrame(errors)
    df.to_csv("observed_e.csv")

# test_mrl_98_new()

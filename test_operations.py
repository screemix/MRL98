def rank(a, elem: int):
    elems = list(set(a))
    elems.sort()
    return elems.index(elem), len(elems)

def calculate_error(real_rank: int, observed_rank: int, N: int):
    return abs(real_rank - observed_rank) / N


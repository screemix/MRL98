# MRL98 implementation 

Implementation and comparison of Munro-Paterson and MRL98 (so-called "new") algorithms from paper ["Approximate Medians and other Quantiles in One Pass and with Limited Memory"](https://www2.cs.sfu.ca/CourseCentral/741/jpei/readings/MRL98.pdf)

## Repository structure
`operations.py`  - implementaion of `new`, `collaplse` and `output` operaions from original paper; class `Buffer`, auxilary function for merging and error calculation
munro_paterson.py - munro-paterson algorithm implementation
`mrl98_new_algorithm.py` - "new algorithm" from paper implementation
`streaming.py` - implementation of data streaming class
`graphs.py`, `tests.py` - function for testing time, memory consumption and errors o algorithms and its visualization
`main.py` - sample code of algorithm usage

## Streaming simulation

For testing purposes `Streaming` module was implemented. It takes `N` as the streamed dataset length and `k` as the bucket sequence size. Basically it creates a generator which could be iterated and returns k next or last remained elements in a random sequence of length `N`.

## Methods implementation

Both algoritms' implementations based on a universal framework described in the original paper. This framefork  consists of the following three operaions:

- `New` - Put the first bk elements into buffers successively and set their weights to 1.
- `Collapse` Compress elements from multiple buffers into one buffer. Specifically, each element from an input buffer Xi would be duplicated w(Xi) times. Then these duplicated elements are sorted and merged into a sequence, where k elements are selected at regular intervals and stored in the output buffer Y , whose weight w(Y) = 􏰃i w(Xi) 
- `Output` Select an element as the quantile answer from b buffers.

**Munro-Paterson algorithm**
- Initialize buffers with weights=0 and empty sequences
- If there are remained elements in a streamed sequence and empty buffer among buffers, it calls NEW on it
-  If there are remained elements in a streaming sequence and no empty buffers among buffers, algorithm calls COLLAPSE on two buffers having the same weigth
-  If there is no new elements in the streamed sequence, algorithm calls OUTPUT on full buffers

**MRL98 algorithm**
- Initialize buffers with weights=0, level=0 and empty sequences
- If there are remained elements in a streaming sequence and exactly one empty buffer among buffers, invoke NEW and assign it level the smallest level among full buffers
- If there are remained elements in a streaming sequence and at least two empty buffers among buffers, invoke NEW on each buffer and assign level 0 to each one
-  If there are remained elements in a streaming sequence and there is no empty buffer, invoke COLLAPSE on the set of buffers with level l and assign level=l+1 to each of them
- If there is no elements remained in the streaming sequence, algorithm invokes OUTPUT on non-empty buffers


## Results and comparison

Several experiments were conducted to test algorithms' performance in terms of time complexity and memory consumption. Also, one experiment was conducted to compare observed and theoretical errors. 

Optimal parameters for each error level were taken from original paper where they have been found as solutions of optimizational problem. 

**Excecution time**
The aim of paper was to optimize algorithm in terms of memory consumption, so there were no explicit remarks about execution time. Still, an experiment was performed to compare MRL98 and Munro-Paterson algorithms in term of excecution time. While error rate was fixed on 0.001, graph of execuion time over dataset size was plotted. It shows that there is no significant difference between two algorithms. Yet MRL98 is a bit faster:

![](https://i.imgur.com/vEYXW1o.png)

Figure 1: execution time over dataset size, fixed error level=0.001


Also, execution times of MRL98 algoritm alone were plotted depending on the error level. This graph vizualize the fact that execution time does not depends on error level, but on dataset size.

![](https://i.imgur.com/CRW6wZB.png)

Figure 2: execution time over dataset size for different error levels of MRL98

**Memory consumption**

As the main aim of paper was optimal streaming algorithm in terms of memory consumption, the difference between MRL98 and Munro-Paterson algorithms is an order of magnitude greater, *which is consistent with the original paper*:

![](https://i.imgur.com/i7Zwrhv.png)

Figure 3: memory consumption over dataset size, fixed error level=0.001

Unlike execution time, memory consumption does depend on error level guarantee. It is also consistent with the original work because value `bk` increases as error level decreases. 

![](https://i.imgur.com/amWRjjY.png)

Figure 4: Memory consumption over dataset size for different error rates of MRL98

**Observed error**

Observed error for fixed error guarantee=0.001 is beyond theorical level, which is consistent with the study:


| q | N=10^5 | N=10^6 | N=10^7 |
| -------- | -------- | -------- | -------- |
| 1 | 0.00005 | 0.000519 | 6.74e-05 |
| 2 | 0.00119 | 0.000682|0.0010121|
| 3 |0.00073  | 0.000878|0.0007146|
| 4 |0.00091 |0.001089|0.0003450|
| 5 |0.00173|0.000266|0.0006193|
| 6 |0.000297|0.0004864|0.0017291|
| 7 |0.000412|0.012727|0.0003662|
| 8 |0.0012|0.0003756|0.00025123|
| 9 |0.000233|0.0004058|0.00024197|
| 10|0.000424|0.0004532|0.00039018|
| 11|0.000235|0.0002307|0.00044353|
| 12|0.000271|0.000353|0.0003824|
| 13|0.000578|0.000513|0.00046376|
| 14|0.000279|0.0004363|0.00043112|
| 15|0.00101|0.0005768|0.00030799|

Table 1: Observed error based on 1/q quantile and dataset size=N for unsorted sequences and error guarantee=0.001


![](https://i.imgur.com/0ANEHU1.png)

Fgure 5: observed error from original study

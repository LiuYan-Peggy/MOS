# The statistical nature of *h*-index of a network node<br>

## Introduction<br>
We discover the statistical nature of *h*-index from the perspective of order statistics, and we obtain a new family of centrality indices by generalizing the *h*-index along this direction. 
However, using only one order statistic to gauge the node importance cannot fully exploit the rich information encoded in the order statistics. 
To this end, we propose to integrate ranking results from multiple order statistics, which is named MOS-index.
The above showed source codes are the calculation of MOS-index for each node in the network.

## Usage<br>
Implementation of MOS-index depends on Python 3.6 and R 3.6.3.<br>

Import MOS.py file into Python and import RRA.r file into R, then load the dataset to test.
rra.csv is a .csv file without any information at initial state, which is used for storing the aggregation result, then the result can be loaded by MOS.py from rra.csv.
It would be better if three files (MOS.py, RRA.r, rra.csv) are downloaded in the same file.

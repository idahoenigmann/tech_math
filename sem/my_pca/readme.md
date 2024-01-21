# Using PCA on EEG Data to Distinguish Sleep Stages

The objective of this project is to see whether it is possible to identify sleep stages
from eeg data using FFT, PCA and k-nearest-neighbor clustering.

The file main.py contains functions for
* calculating the PCA
* visualization
* k nearest neighbor
* reading data from file

pca_tests contains some tests and visualization for pca and k-nearest-neighbors. eeg
contains the analysis of the eeg data and sleep stages.

The data used for this project can be found at
https://www.physionet.org/content/capslpdb/1.0.0/ and is called n*.edf where * goes from
1 to 16. This data has to be added to the eeg/data directory. The files CAPsleepdatan*.csv
specify which sleep phases correspond to each point in time. This file can be found here
TODO.

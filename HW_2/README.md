# How to Build and Run
1. Run command:  python apriori.py
2. Currently, parameters are set directly in the script:- 
- s_threshold: minimum support threshold (default: 0.4)
- c_threshold: minimum cofidence threshold (default:0.6)


3. data: path to the test dataset file (default: "T10I4D100K.dat"), although this can be set to any file that exists in the directory, such as for testing on a small dataset - data.dat
- data , s_threshold and c_threshold can be changed by editing the __main__ block of the script.

## Note
The T10I4D100K.dat dataset can be downloaded from canvas assignment 2 instruction page, it is not included in the zipped code.
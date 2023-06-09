#!/usr/bin/env python
"""
Read in the synthetic data set and return them in the 
format required by TAPAS.
"""
import sys
import numpy as np
import pandas as pd 
import os 

# currently hard-code the model name, data path and dataset
datapath = "../datasets/"
dataset_name = "Adult"
model_name = "DPCGANS"
file = "dpcgans_sample_2000.csv"

def main(n):
    filename = os.path.join(datapath, dataset_name, model_name, file)
    data = pd.read_csv(filename, index_col=0)
    if n > data.shape[0]:
        raise ValueError("Do not have enough samples")
    data = data.iloc[:n, :]
    print(data.to_csv(index=None))



if __name__ == "__main__":
    if len(sys.argv) == 2:
        n_samples = int(sys.argv[1])
    else:
        raise RuntimeError("Need exactly one argument.")
    
    main(n_samples)
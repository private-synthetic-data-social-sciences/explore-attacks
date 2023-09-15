"""Call the generator for exploring

Mimicks https://github.com/alan-turing-institute/privacy-sdg-toolbox/blob/main/tapas/generators/generator.py
"""


import subprocess
from subprocess import PIPE
import pandas as pd
import numpy as np 

np.random.seed(1)

tabular_data=pd.read_csv("../datasets/Adult/Real/real_adult_data.csv")

tabular_data.drop(columns=["Unnamed: 0"], inplace=True)

tabular_data = tabular_data.sample(n=20)

exe = "src/generator_dp_cgans.py"
num_samples = 10

proc = subprocess.Popen([exe, f"{num_samples}"], stdin = PIPE, stdout = PIPE)
input = bytes(tabular_data.to_csv(None, index=False), 'utf-8')
output = proc.communicate(input = input)[0].decode()



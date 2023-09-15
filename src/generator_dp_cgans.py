#!/usr/bin/env python
"""Generate synthetic data with DP-CGANS model.

This generator can be called by TAPAS to generate synthetic data given an input dataset.
"""


import sys

from dp_cgans import DP_CGAN
import pandas as pd 
import io 


def read_data():
    "Read a csv from stdin"
    data = ""
    for line in sys.stdin:
        data += line
    df = pd.read_csv(io.StringIO(data), sep=",", encoding="utf-8")
    return df


def generate_data(df, n):
    """Train a generator on the dataframe df and return a synthetic dataset of size n"""
    model = DP_CGAN(
        epochs=100, # number of training epochs
        batch_size=200, # the size of each batch
        log_frequency=True,
        verbose=True,
        generator_dim=(128, 128, 128),
        discriminator_dim=(128, 128, 128),
        generator_lr=2e-4, 
        discriminator_lr=2e-4,
        discriminator_steps=1, 
        private=False,
    )

    model.fit(df)
    syn_data = model.sample(n)
    return syn_data

def main(n):
    """Generate synthetic data from an input dataset"""
    df = read_data()
    syn_data = generate_data(df, n)
    # print to console 
    print(syn_data.to_csv(None, index=False))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        n_samples = int(sys.argv[1])
    else:
        raise RuntimeError("Need exactly one argument.")
    
    main(n_samples)
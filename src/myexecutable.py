#!/usr/bin/env python
import sys
import numpy as np
import pandas as pd 

def main(n):
    rng = np.random.default_rng(123)
    wage = rng.random(n)
    identifier = np.arange(n)
    raw_data = np.stack([identifier, wage], axis=1)
    df = pd.DataFrame(raw_data, columns=["id", "wage"])
    df["id"] = df["id"].astype(int)
    print(df.to_csv(index=None))



if __name__ == "__main__":
    if len(sys.argv) == 2:
        n_samples = int(sys.argv[1])
    else:
        raise RuntimeError("Need exactly one argument.")
    
    main(n_samples)
    
    

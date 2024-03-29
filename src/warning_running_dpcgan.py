"""document a bug when running DP-CGAN

With this code, I get a RuntimeWarning. But it goes away with using only `columns_to_keep`.
"""

from dp_cgans import DP_CGAN
import pandas as pd

import numpy as np 

np.random.seed(1)

columns_to_keep = ["age", "education", "marital-status", "occupation", "race", "sex", "label"]
tabular_data=pd.read_csv("../datasets/Adult/Real/real_adult_data.csv", usecols=columns_to_keep)


tabular_data = tabular_data.sample(n=300)

# We adjusted the original CTGAN model from SDV. Instead of looking at the distribution of individual variable, we extended to two variables and keep their corrll
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

print("Start training model")
try:
   model.fit(tabular_data)
except Exception as e:
   breakpoint()


model.save("generator.pkl")

# Generate 100 synthetic rows
syn_data = model.sample(100)
syn_data.to_csv("syn_data_file.csv")
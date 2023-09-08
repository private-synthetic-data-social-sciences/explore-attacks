# explore-attacks
Explore libraries for inference attacks on synthetic tabular data

Installation: with poetry

```bash
# Sometimes it's necessary to tell poetry which python version to use
# https://stackoverflow.com/questions/59810276/poetry-doesnt-use-the-correct-version-of-python
pyenv local 3.9 
poetry env use $(which python) 

# Then install
poetry config virtualenvs.in-project true # not mandatory
poetry install --no-root
```

### Running TAPAS against new generators 

TAPAS communicates to the generator with [`tapas.generators.GeneratorFromExecutable.generate`](https://github.com/alan-turing-institute/privacy-sdg-toolbox/blob/main/tapas/generators/generator.py). A barebones executable that can be called from there should therefore like this:
```python
#!/usr/bin/env python
"my_executable_generator.py"
import sys
import pandas as pd 
import io 

N = sys.argv[1] # require exaclty one argument: N = number of samples to generate
# read data with sys.stdin 
# pass the data to your custom generator
    # any settings for the generator cannot be passed as arguments to this file!
# train the generator
# sample N synthetic records
# print them to the console
print(synthetic_df.to_csv(None, index=False))

```

This file should have the permissions `chmod +x my_executable_generator.py`. 

A working example is in `src/generator_dp_cgans.py`.
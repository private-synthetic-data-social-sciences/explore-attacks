# explore-attacks
Explore libraries for inference attacks on synthetic tabular data

Installation: wity poetry

```bash
# Sometimes it's necessary to tell poetry which python version to use
# https://stackoverflow.com/questions/59810276/poetry-doesnt-use-the-correct-version-of-python
pyenv local 3.9 
poetry env use $(which python) 

# Then install
poetry config virtualenvs.in-project true # not mandatory
poetry install --no-root
```

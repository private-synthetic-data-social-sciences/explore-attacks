"""Helper functions for attack_dpcgans.ipynb"""

import pandas as pd 
import json 

import tapas.datasets
import tapas.generators
import tapas.threat_models
import tapas.attacks
import tapas.report


def load_tabular_dataset(filename_data, filename_schema, N_subsample=None, columns_to_keep=None):
    """Load a tabular dataset for use with TAPAS.
    
    Arguments
    ---------
    filename_data: str
        Full path to the file to load.
    filename_schema: str
        Full path to the json file with the data schema.
    N_subsample: int, optional
        Number of random subsample to draw from the original data set.
    columns_to_keep: list, optional
        If specified, only work with a dataframe with those columns.
    """

    df = pd.read_csv(filename_data, index_col=0)
    df = df.sample(N_subsample)
    if columns_to_keep is not None:
        df = df.loc[:, columns_to_keep]

    with open(filename_schema) as file:
        # Load the JSON data into a dictionary
        data_schema = json.load(file)

    data_schema = [col for col in data_schema if col["name"] in columns_to_keep]
    assert len(data_schema) == len(columns_to_keep), "all columns in the dataframe need to be in the data schema"

    data_description = tapas.datasets.DataDescription(schema=data_schema)
    data = tapas.datasets.TabularDataset(data=df, description=data_description)
    return data


def load_generator(filename_exec, data):
    """Load the executable generator and fit it to the data
    
    filename_exec: str
        Full path and filename of the executable
    data: tapas.TabularDataset
        The real data that will be used by the generator to create synthetic data.
    """

    generator = tapas.generators.GeneratorFromExecutable(exe=filename_exec)
    generator.fit(data)
    return generator
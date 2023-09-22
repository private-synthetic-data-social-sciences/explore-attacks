"""Script for running one attack"""


import os 
import numpy as np 

import tapas.datasets
import tapas.generators
import tapas.threat_models
import tapas.attacks
import tapas.report

from src.helpers import load_generator, load_tabular_dataset

import logging 
import pickle

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        # logging.FileHandler(config.log_file.absolute(), mode="a"),
                        logging.StreamHandler()
                    ],
                    level=logging.INFO)

# TODO:
# lint 

logging.info("Loading data")

# ### Setup 
datapath = "../datasets"
dataset_name = "Adult"
model_name = "DPCGANS"
file = f"Real/real_{dataset_name.lower()}_data.csv"

schema = "data_schemas/adult.json"
executable_generator = "src/generator_dp_cgans.py"


# make some restrictions to speed up training
N_subsample = 500 
# keep only these columns for faster training. Needs to keep columns in the same order
# columns_to_keep = ["age", "education", "marital-status", "occupation", "race", "sex", "label"]
columns_to_keep = ["age", "occupation", "race", "label"] # this is much faster than the above
# categorical variables with more classes are more difficult to train
np.random.seed(1)

n_records_training = 10
n_records_synth = 10 
n_training_datasets = 10
n_testing_datasets = 12 # to highlight the distinction below 

# ### Load data 
data = load_tabular_dataset(
    filename_data=os.path.join(datapath, dataset_name, file),
    filename_schema=schema,
    N_subsample=N_subsample,
    columns_to_keep=columns_to_keep
)

generator = load_generator(executable_generator, data=data)

# ### Define target record
attack_ids = [0]
target_record = data.get_records(attack_ids)

data.drop_records(attack_ids, in_place=True)

# because we will use the ExactKnowledge scenario, we provide the exact data set of the size `n_records_training`. 
# If we used `AuxiliaryDataKnowledge`, we could specify these things in the definition of the threat model
specific_data = data.sample(n_samples=n_records_training)

threat_model = tapas.threat_models.TargetedMIA(
    attacker_knowledge_data=tapas.threat_models.ExactDataKnowledge(
        specific_data),       
    attacker_knowledge_generator=tapas.threat_models.BlackBoxKnowledge(
            generator, num_synthetic_records=n_records_synth,
        ),
    target_record=target_record,
    generate_pairs=False, # TODO: what does this do exactly?
    replace_target=False # TODO: what does this do exactly?
) 

attack = tapas.attacks.ClosestDistanceMIA(criterion="accuracy", label="Closest-Distance")

logging.info("Training attack")
attack.train(threat_model, num_samples=n_training_datasets) # that's short, 55.2 seconds with few columns

logging.info("Testing attack")
attack_summary = threat_model.test(attack, num_samples=n_testing_datasets) # 100 takes 10 minutes. 10 takes 40 seconds

# save the threat model 
logging.info("Done with testing")
metrics = attack_summary.get_metrics()

with open("saved_attacks/mia_closest_distance_acc.pkl", "wb") as f:
    pickle.dump(threat_model, file=f)


logging.info("Done.")




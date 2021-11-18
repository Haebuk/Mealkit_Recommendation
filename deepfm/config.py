# config.py
# ALL_FIELDS : X의 columns
ALL_FIELDS = ['user','name']
# CONT_FIELDS : 연속형인 columns
CONT_FIELDS = []
# CAT_FIELDS : 범주형 columns
CAT_FIELDS = list(set(ALL_FIELDS).difference(CONT_FIELDS))

# Hyper-parameters for Experiment
NUM_BIN = 10
BATCH_SIZE = 256
EMBEDDING_SIZE = 20
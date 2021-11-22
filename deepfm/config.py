# config.py
# ALL_FIELDS : X의 columns
ALL_FIELDS = ['user','brand','category']
# CONT_FIELDS : 연속형인 columns
CONT_FIELDS = []
# CAT_FIELDS : 범주형 columns
CAT_FIELDS = list(set(ALL_FIELDS).difference(CONT_FIELDS))

# Hyper-parameters for Experiment
NUM_BIN = 10
BATCH_SIZE = 32
EMBEDDING_SIZE = 20
EMB_VEC_SIZE = 768 
LEARNING_RATE = 1e-4
EPOCHS = 100
MODEL_PATH = 'models/deepFM/'
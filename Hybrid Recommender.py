import sys
import os
import pandas as pd
from fastFM import sgd, als
import numpy as np
import scipy
from sklearn.metrics import mean_squared_error, accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from utils.data_frame import DataFrame
from utils.pickles import *
import tensorflow as tf
from deepfm.train import get_data
from deepfm.only_emb import get_data_emb
if __name__ == '__main__':
    train_ds, test_ds, field_dict, field_index, Y_test = get_data()
    name_train, name_test, desc_train, desc_test, Y_train, Y_test= get_data_emb()
    print(train_ds)
    print(test_ds)

    deep_fm = tf.keras.models.load_model('models/deepFM/deepfm/epoch_24-auc_0.57124.tf')
    emb = tf.keras.models.load_model('models/deepFM/only_emb/epoch_45-auc_0.56-acc_0.76.tf')
    deep_fm.summary()
    emb.summary()

    # y = read_pickle_files('kurly_pred_mlp.pickle').apply(lambda x: 1 if x > 0.5 else 0)

    deep_fm_pred = deep_fm.predict(test_ds)
    emb_pred = emb.predict([name_test, desc_test])
    print(deep_fm_pred)
    print(emb_pred)
    print(deep_fm_pred.shape)
    print(emb_pred.shape)
    print(Y_test.shape)
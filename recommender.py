import pandas as pd
import numpy as np
from utils.data_frame import DataFrame
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score, roc_auc_score
import tensorflow as tf
from deepfm.preprocess import get_modified_data
from deepfm import config
from utils.pickles import *
import argparse


kurly_df = DataFrame('마켓컬리').get_FMdata()
review = DataFrame('마켓컬리', '리뷰').get_df()
info = DataFrame('마켓컬리', '정보').get_df()

# name parser
parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, default='방*민')
args = parser.parse_args()
NAME = args.name
# NAME = '유*'
buy = review.loc[review['user']==NAME, 'name']
df_col = kurly_df.columns
test_df = pd.DataFrame(columns=df_col)
total_name = review['name'].unique()
not_buy = [name for name in total_name if name not in buy.values]
not_brand = info.loc[info['name'].isin(not_buy), 'brand']
not_category = info.loc[info['name'].isin(not_buy), 'category']
test_df = pd.DataFrame(columns=df_col, index=range(len(not_buy)))

for i, (name, brand, category) in enumerate(zip(not_buy, not_brand, not_category)):

    test_df.loc[i, name] = 1
    test_df.loc[i, brand] = 1
    test_df.loc[i, category] = 1
    test_df.loc[i, NAME] = 1

test_df.fillna(0, inplace=True)
print('buy',buy.index)
title_emb = read_pickle_files('data/kurly_name_emb_df.pkl').loc[not_brand.index]
desc_emb = read_pickle_files('data/kurly_desc_emb_df_expanded.pkl').loc[not_brand.index]
# emb = tf.keras.models.load_model('models/deepFM/only_emb/rus/epoch_99-auc_0.93-acc_0.85.tf')
# emb_pred = emb.predict([title_emb, desc_emb]).reshape(-1)
# print('emp_pred:',emb_pred)

# print(test_df)
deep_fm = tf.keras.models.load_model('models/deepFM/deepfm2/epoch_57-auc_0.70061.tf')
field_dict, field_index, X_modified = \
        get_modified_data(test_df, config.ALL_FIELDS, config.CONT_FIELDS, config.CAT_FIELDS, False)
# test_ds = tf.data.Dataset.from_tensor_slices((title_emb, desc_emb, X_modified))
# test_ds = tf.data.Dataset.zip(test_ds).batch(config.BATCH_SIZE)
# for i in test_ds:
#     print(i)
#     break
# test_y_ds = tf.data.Dataset.from_tensor_slices(Y_test)
# test_ds = tf.data.Dataset.zip((test_x_ds, test_y_ds)).batch(config.BATCH_SIZE)
# test_ds = tf.data.Dataset.from_tensor_slices(
#         (tf.cast(X_modified.values, tf.float32))) \
#         .batch(1)

deep_fm_pred = deep_fm.predict([title_emb, desc_emb, X_modified])
print('deepfm_pred:',deep_fm_pred[:5])
# reshape
deep_fm_pred = deep_fm_pred.reshape(-1)
print(deep_fm_pred.shape)

# w_deep_fm = 0.3
# w_emb = np.round(1 - w_deep_fm, 2)
# weighted_pred = w_deep_fm * deep_fm_pred + w_emb * emb_pred
# print('weighted_pred:',weighted_pred)
print(np.sort(deep_fm_pred)[::-1][:20])
best = np.argsort(deep_fm_pred)[::-1][:20]
print('best:',best)
print(buy)
not_buy = pd.Series(not_buy)
# print(not_buy)
not_buy = not_buy.loc[not_buy.index.isin(best)]
for i in best:
    print(i, not_buy[i])


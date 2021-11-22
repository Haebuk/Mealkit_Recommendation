import enum
import config
from load_data import load_data
from preprocess import get_modified_data
from deepFM2 import DeepFM
from utils.data_frame import DataFrame
import numpy as np
import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from time import perf_counter
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.metrics import BinaryAccuracy, AUC
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, LearningRateScheduler
from utils.pickles import read_pickle_files

def get_data():
    # data = load_data('이마트몰','리뷰').get_df()
    data = DataFrame('마켓컬리', '정보').get_FMdata()
    X = data
    title_emb = read_pickle_files('data/kurly_name_emb_df_expanded.pkl')
    desc_emb = read_pickle_files('data/kurly_desc_emb_df_expanded.pkl')
    # X = pd.concat([X, title_emb, desc_emb], axis=1)
    # Y = DataFrame('이마트몰','리뷰').get_df().loc[:, 'star'].map({'0':0,'1':0,'2':0,'3':0,'4':1,'5':1})
    Y = read_pickle_files('kurly_pred_mlp.pickle').apply(lambda x: 1 if x > 0.5 else 0)
    # rus = RandomUnderSampler(random_state=0)
    # X, Y = rus.fit_resample(X, Y)
    
    field_dict, field_index, X_modified = \
        get_modified_data(X, config.ALL_FIELDS, config.CONT_FIELDS, config.CAT_FIELDS, False)
    print(X_modified)
    X_train, X_test, Y_train, Y_test = train_test_split(X_modified, Y, test_size=0.2, stratify=Y)
    name_train, name_test, desc_train, desc_test = title_emb.loc[X_train.index], title_emb.loc[X_test.index], desc_emb.loc[X_train.index], desc_emb.loc[X_test.index]

    train_x_ds = tf.data.Dataset.from_tensor_slices((name_train, desc_train, X_train))
    train_y_ds = tf.data.Dataset.from_tensor_slices(Y_train)
    train_ds = tf.data.Dataset.zip((train_x_ds, train_y_ds)).batch(config.BATCH_SIZE)

    test_x_ds = tf.data.Dataset.from_tensor_slices((name_test, desc_test, X_test))
    test_y_ds = tf.data.Dataset.from_tensor_slices(Y_test)
    test_ds = tf.data.Dataset.zip((test_x_ds, test_y_ds)).batch(config.BATCH_SIZE)

    return train_ds, test_ds, field_dict, field_index

def scheduler(epoch, lr):
   if epoch < 5:
     return lr
   else:
     return lr * tf.math.exp(-0.1)

# 반복 학습 함수
def train(epochs):
    train_ds, test_ds, field_dict, field_index = get_data()

    model = DeepFM(embedding_size=config.EMBEDDING_SIZE, num_feature=len(field_index),
                   num_field=len(field_dict), field_index=field_index)
    model.summary()
    optimizer = tf.keras.optimizers.Adam(learning_rate=config.LEARNING_RATE)

    print(f"Start Training: Batch Size: {config.BATCH_SIZE}, Embedding Size: {config.EMBEDDING_SIZE}, Leargning Rate: {config.LEARNING_RATE}")
    start = perf_counter() # 시간 Count

    ### fit method
    early_stopping = EarlyStopping(monitor='val_auc', patience=10, mode='max')
    lr_scheduler = LearningRateScheduler(scheduler)
    model_checkpoint = ModelCheckpoint(filepath=config.MODEL_PATH+'epoch_{epoch:02d}-auc_{val_auc:.2f}-acc_{val_binary_accuracy:.2f}.tf', monitor='val_auc', save_best_only=True, verbose=1, mode='max')
    model.compile(optimizer=optimizer, loss=tf.keras.losses.binary_crossentropy, metrics=[BinaryAccuracy(), AUC()])
    model.fit(train_ds, epochs=epochs, validation_data=test_ds, callbacks=[early_stopping, lr_scheduler])
    return model

if __name__ == '__main__':
    model = train(epochs=config.EPOCHS)
    model.summary()

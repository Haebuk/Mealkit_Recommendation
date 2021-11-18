import tensorflow as tf
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import wandb
import re
import emoji
from soynlp.normalizer import repeat_normalize
import pandas as pd
from wandb.keras import WandbCallback
from tensorflow.keras.layers import Input, Dense, concatenate, Conv1D, BatchNormalization, GlobalMaxPooling1D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras import losses
from tensorflow.keras import metrics
from tensorflow.keras.layers import Activation
from sklearn.model_selection import train_test_split

from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras import metrics
from tensorflow.keras.layers import Activation
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import BatchNormalization
from utils.pickles import *


PATH = './nsmc/'
ratings_train = pd.read_table(PATH + 'ratings_train.txt') 
ratings_test = pd.read_table(PATH + 'ratings_test.txt') 
print('Data Load Complete')

train_copy = ratings_train.copy()
test_copy = ratings_test.copy()
train_copy=train_copy.dropna(axis=0).reset_index(drop=True)
test_copy=test_copy.dropna(axis=0).reset_index(drop=True)

print('embedding ... ')
naver_train = read_pickle_files('naver_train.pickle')
naver_test = read_pickle_files('naver_test.pickle')
print('embedding complete ...')

train_x, val_x = train_test_split(naver_train, test_size=0.2, random_state=42)
train_y, val_y = train_test_split(train_copy['label'], test_size=0.2, random_state=42)

test_x = test_copy['document']
test_y = test_copy['label']

default_configs = {
    'layer1': 256,
    'layer2': 128,
    'layer3': 64,
    'dropout': 0.5,
    'learning_rate' : 0.001
}

wandb.init(project='Mealkit-Recommendation', entity='kuggle', config=default_configs)

config = wandb.config

def cnn_model():
  model = models.Sequential()
  model.add(layers.Dense(config.layer1, input_shape=(768,)))
  model.add(BatchNormalization())
  model.add(Activation('relu'))
  model.add(layers.Dropout(config.dropout))

  model.add(layers.Dense(config.layer2))
  model.add(BatchNormalization())
  model.add(Activation('relu'))
  model.add(layers.Dropout(config.dropout))

  model.add(layers.Dense(config.layer3))
  model.add(BatchNormalization())
  model.add(Activation('relu'))
  model.add(layers.Dropout(config.dropout))

  # model.add(layers.Dense(32))
  # model.add(BatchNormalization())
  # model.add(Activation('relu'))
  # model.add(layers.Dropout(0.5))

  model.add(layers.Dense(1, activation='sigmoid'))

  return model

  # # input layer
  # inputs = Input(shape=(train_vectors_X.shape[1],1))

  # # first feature extractor
  # conv1 = Conv1D(config.conv, kernel_size=config.kernel_size)(inputs)
  # batchnorm1 = BatchNormalization()(conv1)
  # relu1 = Activation('relu')(batchnorm1)
  # pool1 = GlobalMaxPooling1D()(relu1)

  # # second feature extractor
  # conv2 = Conv1D(config.conv, kernel_size=config.kernel_size)(inputs)
  # batchnorm2 = BatchNormalization()(conv2)
  # relu2 = Activation('relu')(batchnorm2)
  # pool2 = GlobalMaxPooling1D()(relu2)

  # # third feature extractor
  # conv3 = Conv1D(config.conv, kernel_size=config.kernel_size)(inputs)
  # batchnorm3 = BatchNormalization()(conv3)
  # relu3 = Activation('relu')(batchnorm3)
  # pool3 = GlobalMaxPooling1D()(relu3)

  # # merge feature extractors
  # merge = concatenate([pool1, pool2, pool3])

  # # interpretation layer
  # dropout1 = Dropout(config.dropout_rate)(merge)
  # dense1 = Dense(config.hidden1)(dropout1)
  # batchnorm_1 = BatchNormalization()(dense1)
  # relu_1 = Activation('relu')(batchnorm_1)
  # dropout2 = Dropout(config.dropout_rate)(batchnorm_1)
  # dense2 = Dense(config.hidden2)(dropout2)
  # batchnorm_2 = BatchNormalization()(dense2)
  # output = Dense(1, activation='sigmoid')(batchnorm_2)

  # return Model(inputs=inputs, outputs=output)

model2 = cnn_model()
model2.compile(optimizer=optimizers.Adam(learning_rate=config.learning_rate),
             loss=losses.binary_crossentropy,
             metrics=[metrics.binary_accuracy])

checkpoint = ModelCheckpoint(PATH, monitor='val_loss', verbose=1, save_best_only=True)
earlystopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1)

model2.fit(train_x, train_y, validation_data=(val_x, val_y), epochs=100, batch_size=256, callbacks=[checkpoint, earlystopping, WandbCallback()])



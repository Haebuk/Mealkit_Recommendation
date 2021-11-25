import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from deepfm import config
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.metrics import BinaryAccuracy, AUC
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, LearningRateScheduler
from utils.pickles import read_pickle_files
from imblearn.under_sampling import RandomUnderSampler

def get_data_emb():
    # data = load_data('이마트몰','리뷰').get_df()
    # data = DataFrame('마켓컬리', '정보').get_FMdata()
    # X = data
    title_emb = read_pickle_files('data/kurly_name_emb_df_expanded.pkl')
    desc_emb = read_pickle_files('data/kurly_desc_emb_df_expanded.pkl')
    # X = pd.concat([X, title_emb, desc_emb], axis=1)
    # Y = DataFrame('이마트몰','리뷰').get_df().loc[:, 'star'].map({'0':0,'1':0,'2':0,'3':0,'4':1,'5':1})
    Y = read_pickle_files('kurly_pred_mlp.pickle').apply(lambda x: 1 if x > 0.5 else 0)
    rus = RandomUnderSampler(random_state=0)
    title_emb, Y = rus.fit_resample(title_emb, Y)
    
    X_train, X_test, Y_train, Y_test = train_test_split(title_emb, Y, test_size=0.2, stratify=Y, random_state=42)
    name_train, name_test, desc_train, desc_test = title_emb.loc[X_train.index], title_emb.loc[X_test.index], desc_emb.loc[X_train.index], desc_emb.loc[X_test.index]
    print(f'EMB: y_train:{Y_train[:3]}, y_test:{Y_test[:3]}')

    return name_train, name_test, desc_train, desc_test, Y_train, Y_test

def scheduler(epoch, lr):
   if epoch < 5:
     return lr
   else:
     return lr * tf.math.exp(-0.1)

# 반복 학습 함수
def train(epochs):
    name_train, name_test, desc_train, desc_test, Y_train, Y_test = get_data_emb()

    title = tf.keras.layers.Input(shape=(768,), name='title')
    desc = tf.keras.layers.Input(shape=(768,), name='desc')
    # title = tf.keras.layers.Dense(units=768, activation='relu')(title)
    # desc = tf.keras.layers.Dense(units=768, activation='relu')(desc)
    dense = tf.keras.layers.Concatenate()([title, desc])
    # dense = tf.keras.layers.Dense(units=256, activation='relu')(concat)
    # dense = tf.keras.layers.Dense(units=128, activation='relu')(concat)
    dense = tf.keras.layers.Dense(units=1, activation='sigmoid')(dense)

    
    model = tf.keras.Model(inputs=[title, desc], outputs=dense)
    model.summary()
    optimizer = tf.keras.optimizers.Adam(learning_rate=config.LEARNING_RATE)

    print(f"Start Training: Batch Size: {config.BATCH_SIZE}, Leargning Rate: {config.LEARNING_RATE}")

    ### fit method
    early_stopping = EarlyStopping(monitor='val_auc', patience=10, mode='max')
    lr_scheduler = LearningRateScheduler(scheduler)
    model_checkpoint = ModelCheckpoint(filepath=config.MODEL_PATH+'only_emb/epoch_{epoch:02d}-auc_{val_auc:.2f}-acc_{val_binary_accuracy:.2f}.tf', monitor='val_auc', save_best_only=True, verbose=1, mode='max')
    model.compile(optimizer=optimizer, loss=tf.keras.losses.binary_crossentropy, metrics=[BinaryAccuracy(), AUC()])
    model.fit([name_train, desc_train], Y_train, epochs=epochs, validation_data=([name_test, desc_test], Y_test), callbacks=[early_stopping, lr_scheduler, model_checkpoint])
    return model

if __name__ == '__main__':
    model = train(epochs=config.EPOCHS)
    model.summary()

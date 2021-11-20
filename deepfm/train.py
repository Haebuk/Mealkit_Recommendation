import enum
import config
from load_data import load_data
from preprocess import get_modified_data
from DeepFM import DeepFM

import numpy as np
import pandas as pd
from time import perf_counter
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.metrics import BinaryAccuracy, AUC

def get_data():
    data = load_data('이마트몰','리뷰').get_df()
    X = data.loc[:, :'name']
    Y = data.loc[:, 'star'].map({'0':0,'1':0,'2':0,'3':0,'4':1,'5':1})

    field_dict, field_index, X_modified = \
        get_modified_data(X, config.ALL_FIELDS, config.CONT_FIELDS, config.CAT_FIELDS, False)

    X_train, X_test, Y_train, Y_test = train_test_split(X_modified, Y, test_size=0.2, stratify=Y)

    train_ds = tf.data.Dataset.from_tensor_slices(
        (tf.cast(X_train.values, tf.float32), tf.cast(Y_train, tf.float32))) \
        .shuffle(20000).batch(config.BATCH_SIZE)

    test_ds = tf.data.Dataset.from_tensor_slices(
        (tf.cast(X_test.values, tf.float32), tf.cast(Y_test, tf.float32))) \
        .shuffle(3000).batch(config.BATCH_SIZE)

    return train_ds, test_ds, field_dict, field_index, Y_test

def train_on_batch(model, optimizer, acc, auc, inputs, targets):
    with tf.GradientTape() as tape:
        y_pred = model(inputs)
        loss = tf.keras.losses.binary_crossentropy(from_logits=False, y_true=targets, y_pred=y_pred)

    grads = tape.gradient(target=loss, sources=model.trainable_variables)

    # apply_gradients()를 통해 processed gradients를 적용함
    optimizer.apply_gradients(zip(grads, model.trainable_variables))

    # accuracy & auc
    acc.update_state(targets, y_pred)
    auc.update_state(targets, y_pred)

    return loss


# 반복 학습 함수
def train(epochs):
    train_ds, test_ds, field_dict, field_index, Y_test = get_data()

    # 임베딩 사이즈: 256 / feature 수: 108 / group화된 feature 수: 14 / group_number
    model = DeepFM(embedding_size=config.EMBEDDING_SIZE, num_feature=len(field_index),
                   num_field=len(field_dict), field_index=field_index)

    # SGD
    optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

    print("Start Training: Batch Size: {}, Embedding Size: {}".format(config.BATCH_SIZE, config.EMBEDDING_SIZE))
    start = perf_counter() # 시간 Count

    # epoch = 100
    for i in range(epochs):
        acc = BinaryAccuracy(threshold=0.5) # Accuracy
        auc = AUC()                         # AUC_ROC
        loss_history = []

        for x, y in train_ds:
            loss = train_on_batch(model, optimizer, acc, auc, x, y)
            loss_history.append(loss)

        print("Epoch {:03d}: 누적 Loss: {:.4f}, Acc: {:.4f}, AUC: {:.4f}".format(
            i, np.mean(loss_history), acc.result().numpy(), auc.result().numpy()))

    test_acc = BinaryAccuracy(threshold=0.5)
    test_auc = AUC()
    y_pred_list = []
    for x, y in test_ds:
        y_pred = model(x)
        for pred in y_pred.numpy():
            y_pred_list.append(pred)
        test_acc.update_state(y, y_pred)
        test_auc.update_state(y, y_pred)

    compare_df = pd.DataFrame(Y_test)
    compare_df['y_pred'] = y_pred_list

    print("테스트 ACC: {:.4f}, AUC: {:.4f}".format(test_acc.result().numpy(), test_auc.result().numpy()))
    print("Batch Size: {}, Embedding Size: {}".format(config.BATCH_SIZE, config.EMBEDDING_SIZE))
    print("걸린 시간: {:.3f}".format(perf_counter() - start))
    # model.save_weights('weights/weights-epoch({})-batch({})-embedding({}).h5'.format(
    #     epochs, config.BATCH_SIZE, config.EMBEDDING_SIZE))
    return y_pred_list, compare_df


if __name__ == '__main__':
    result, compare_df = train(epochs=10)
    print(compare_df)

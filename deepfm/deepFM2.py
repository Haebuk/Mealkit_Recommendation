import tensorflow as tf
from layers import FM_layer
import config
from utils.pickles import read_pickle_files

tf.keras.backend.set_floatx('float32')
def DeepFM(num_feature, num_field, embedding_size, field_index):
    input = tf.keras.layers.Input(shape=(num_feature,), name='input')
    title = tf.keras.layers.Input(shape=(768,), name='title')
    desc = tf.keras.layers.Input(shape=(768,), name='desc')
    emb = tf.concat([title, desc], 1)
    # title = tf.keras.layers.Dense(units=64, activation='relu')(title)
    # desc = tf.keras.layers.Dense(units=64, activation='relu')(desc)
    emb = tf.keras.layers.Dense(units=64, activation='relu')(emb)
    emb = tf.keras.layers.Dense(units=2, activation='relu')(emb)
    y_fm, new_inputs = FM_layer(num_feature, num_field, embedding_size, field_index)(input)
    new_inputs = tf.reshape(new_inputs, [-1, num_feature*embedding_size])

    y_deep = tf.keras.layers.Dense(units=1024, activation='relu')(new_inputs)
    y_deep = tf.keras.layers.Dropout(rate=0.5)(y_deep)
    y_deep = tf.keras.layers.Dense(units=256, activation='relu')(y_deep)
    y_deep = tf.keras.layers.Dropout(rate=0.5)(y_deep)
    y_deep = tf.keras.layers.Dense(units=64, activation='relu')(y_deep)
    y_deep = tf.keras.layers.Dropout(rate=0.5)(y_deep)
    y_deep = tf.keras.layers.Dense(units=2, activation='relu')(y_deep)
    concat = tf.concat([y_fm, y_deep, emb], 1)
    y_pred = tf.keras.layers.Dense(units=1, activation='sigmoid')(concat)

    model = tf.keras.Model(inputs=[title, desc, input], outputs=y_pred)
    return model

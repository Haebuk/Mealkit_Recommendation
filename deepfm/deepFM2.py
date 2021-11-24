import sys
sys.path.append('../')
import tensorflow as tf
try:
    from deepfm.layers import FM_layer
except:
    from layers import FM_layer

tf.keras.backend.set_floatx('float32')
def DeepFM(num_feature, num_field, embedding_size, field_index):

    desc_input = tf.keras.layers.Input(shape=(768,), name='desc')
    desc = tf.keras.layers.Dense(units=64, activation='relu')(desc_input)
    desc = tf.keras.layers.Dropout(0.9)(desc)
    desc = tf.keras.layers.Dense(units=8, activation='relu')(desc)
    desc = tf.keras.layers.Dropout(0.5)(desc)

    title_input = tf.keras.layers.Input(shape=(768,), name='title')
    title = tf.keras.layers.Dense(units=64, activation='relu')(title_input)
    title = tf.keras.layers.Dropout(0.9)(title)
    title = tf.keras.layers.Dense(units=8, activation='relu')(title)
    title = tf.keras.layers.Dropout(0.5)(title)

    emb = tf.concat([title, desc], 1)
    # emb = tf.keras.layers.Dense(units=64, activation='relu')(emb)
    # emb = tf.keras.layers.Dropout(0.8)(emb)
    # emb = tf.keras.layers.Dense(units=16, activation='relu')(emb)
    input = tf.keras.layers.Input(shape=(num_feature,), name='input')
    y_fm, new_inputs = FM_layer(num_feature, num_field, embedding_size, field_index)(input)
    new_inputs = tf.reshape(new_inputs, [-1, num_feature*embedding_size])

    y_deep = tf.keras.layers.Dense(units=256)(new_inputs)
    y_deep = tf.keras.layers.BatchNormalization()(y_deep)
    y_deep = tf.keras.layers.Activation('relu')(y_deep)
    # y_deep = tf.keras.layers.Dropout(rate=0.3)(y_deep)
    y_deep = tf.keras.layers.Dense(units=64)(y_deep)
    y_deep = tf.keras.layers.BatchNormalization()(y_deep)
    y_deep = tf.keras.layers.Activation('relu')(y_deep)
    # y_deep = tf.keras.layers.Dropout(rate=0.3)(y_deep)
    y_deep = tf.keras.layers.Dense(units=2, activation='relu')(y_deep)
    concat = tf.concat([y_fm, y_deep, emb], 1)
    y_pred = tf.keras.layers.Dense(units=1, activation='sigmoid')(concat)

    model = tf.keras.Model(inputs=[title_input, desc_input, input], outputs=y_pred)
    return model

import sys
sys.path.append('../')
import tensorflow as tf
try:
    from deepfm.layers import FM_layer
except:
    from layers import FM_layer


tf.keras.backend.set_floatx('float32')

class DeepFM(tf.keras.Model):

    def __init__(self, num_feature, num_field, embedding_size, field_index):
        super(DeepFM, self).__init__()
        self.embedding_size = embedding_size    # k: 임베딩 벡터의 차원(크기)
        self.num_feature = num_feature          # f: 원래 feature 개수
        self.num_field = num_field              # m: grouped field 개수
        self.field_index = field_index          # 인코딩된 X의 칼럼들이 본래 어디 소속이었는지

        # Factorization Machine
        self.fm_layer = FM_layer(num_feature, num_field, embedding_size, field_index)

        # DNN
        self.relu = tf.keras.layers.ReLU()

        self.layers1 = tf.keras.layers.Dense(units=512)
        self.bn1 = tf.keras.layers.BatchNormalization()
        self.dropout1 = tf.keras.layers.Dropout(rate=0.)

        self.layers2 = tf.keras.layers.Dense(units=256)
        self.bn2 = tf.keras.layers.BatchNormalization()
        self.dropout2 = tf.keras.layers.Dropout(rate=0.5)


        self.layers3 = tf.keras.layers.Dense(units=64)
        self.bn3 = tf.keras.layers.BatchNormalization()
        self.dropout3 = tf.keras.layers.Dropout(rate=0.5)

        self.layers4 = tf.keras.layers.Dense(units=2)

        # 마지막 DNN+FM
        self.final = tf.keras.layers.Dense(units=1, activation='sigmoid')

    def __repr__(self):
        return "DeepFM Model: #Field: {}, #Feature: {}, ES: {}".format(
            self.num_field, self.num_feature, self.embedding_size)

    def call(self, inputs):
        # 1) FM Component: (num_batch, 2)
        y_fm, new_inputs = self.fm_layer(inputs)
        # print(new_inputs)
        # retrieve Dense Vectors: (num_batch, num_feature*embedding_size)
        new_inputs = tf.reshape(new_inputs, [-1, self.num_feature*self.embedding_size])

        # 2) Deep Component
        y_deep = self.layers1(new_inputs)
        y_deep = self.bn1(y_deep)
        y_deep = self.relu(y_deep)
        y_deep = self.dropout1(y_deep)
        y_deep = self.layers2(y_deep)
        y_deep = self.bn2(y_deep)
        y_deep = self.relu(y_deep)
        y_deep = self.dropout2(y_deep)
        y_deep = self.layers3(y_deep)
        y_deep = self.bn3(y_deep)
        y_deep = self.relu(y_deep)
        y_deep = self.dropout3(y_deep)
        y_deep = self.layers4(y_deep)

        # Concatenation
        y_pred = tf.concat([y_fm, y_deep], 1)
        y_pred = self.final(y_pred)
        y_pred = tf.reshape(y_pred, [-1, ])

        return y_pred
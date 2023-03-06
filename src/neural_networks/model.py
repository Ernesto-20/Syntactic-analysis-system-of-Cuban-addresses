import re

import keras.optimizers
import tensorflow as tf
import string
from keras.utils import pad_sequences
from keras.layers.core import Activation, Dropout, Dense
from tensorflow.python.ops.ragged.ragged_string_ops import string_bytes_split
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import pandas as pd
import numpy as np
from keras.layers import TextVectorization
from keras.utils import plot_model

from keras import Sequential, Model, Input
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional

from numpy.random import seed

seed(1)
tf.random.set_seed(2)


class Parser:
    def __init__(self):
        self.__data_Set = None
        self.__vocabulary = None
        self.model_select = False
        self.__dir_model_current = None
        self.__blstm_model = None
        self.__vectorize_model = None
        self.model = None
        self.__n_tag = None
        self.__val_tokens = None
        self.__test_tokens = None
        self.__train_tokens = None
        self.__val_targets = None
        self.__test_targets = None
        self.__train_targets = None
        self.__created_model = False
        self.__name_model = None
        self.__address = None
        self.__id_to_category = None
        self.__load_data = False
        self.__vectorize_layer = None
        self.__group_address = None

    def set_DataSet(self, data_set):
        self.__data_Set = data_set
        self.__load_data = True

    def create_model(self, name_model='default_model', ngrams=None, show_summary=False):
        if self.__load_data:
            self.__name_model = name_model

            output_dim = 64
            input_length = 25

            vectorize_model = self.__create_model_vectorization(ngrams)
            blstm_model = self.__create_model_blstm(self.__data_Set.get_input_dim(), output_dim, input_length)

            # self.__transform_to_tokens(self.__data_Set.get_x_train_sentence_values(),
            #                            self.__data_Set.get_x_test_sentence_values(),
            #                            self.__data_Set.get_x_val_sentence_values())

            inputs = keras.Input(shape=(1,), dtype="string")
            x = vectorize_model(inputs)
            outputs = blstm_model(x)
            self.model = keras.Model(inputs, outputs, name='Model')

            self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
            if show_summary:
                self.__vectorize_model.summary()
                self.__blstm_model.summary()
                self.model.summary()

            self.__created_model = True
            self.model_select = False

        return self.__created_model

    def __create_model_vectorization(self, ngrams):
        vectorize_layer = TextVectorization(
            standardize=custom_standardization,
            output_mode="int",
            output_sequence_length=self.__data_Set.get_max_len(),
            ngrams=ngrams,
            split=string_bytes_split
        )

        vectorize_layer.adapt(self.__data_Set.get_vocabulary())
        # vocab_size = len(self.__vectorize_layer.get_vocabulary())

        vectorize_layer_model = Sequential(name='Vectorization_Layer')
        vectorize_layer_model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
        vectorize_layer_model.add(vectorize_layer)

        vectorize_layer.compile()
        print(vectorize_layer.get_vocabulary())

        return vectorize_layer_model

    # def __convert_text_input(self, sample):
    #     text = sample
    #     text = tf.expand_dims(text, -1)
    #     return self.__vectorize_layer(text)

    # def __transform_to_tokens(self, train, test, val):
    #     self.__train_tokens = self.__transform_to_vector(train)
    #     self.__test_tokens = self.__transform_to_vector(test)
    #     self.__val_tokens = self.__transform_to_vector(val)
    #
    # def __transform_to_vector(self, sentence_list):
    #     temp = []
    #     for item in sentence_list:
    #         temp.append(self.__convert_text_input(item)[0])
    #     return np.array(temp)

    def __create_model_blstm(self, input_dim, output_dim, input_length):
        model = Sequential(name='Bidirectional_Long_Short_Term_Memory_Layer')

        # Add Input layer
        model.add(Input(shape=(self.__data_Set.get_max_len(),), dtype=tf.int32))

        # Add Embedding layer
        model.add(Embedding(input_dim=input_dim, output_dim=output_dim, input_length=input_length))

        # Add bidirectional LSTM
        model.add(Bidirectional(LSTM(units=output_dim, return_sequences=True, dropout=0.4, recurrent_dropout=0.4),
                                merge_mode='concat'))

        # Add LSTM
        model.add(LSTM(units=output_dim, return_sequences=True, dropout=0.5, recurrent_dropout=0.5))

        # Add timeDistributed Layer
        model.add(TimeDistributed(Dense(self.__data_Set.get_n_tag(), activation="relu")))
        model.add(Activation('softmax'))
        # model.add(Dense(8, activation='softmax'))

        # Optimiser
        adam = keras.optimizers.Adam(learning_rate=0.0005, beta_1=0.9, beta_2=0.999)

        # Compile model
        model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

        return model

    def fit_model(self, batch_size=1200, epochs=50):
        check = False
        if self.__created_model:
            # self.__blstm_model.fit(self.__train_tokens, self.__data_Set.get_y_train_values(), batch_size=batch_size,
            #                        verbose=1, epochs=epochs,
            #                        validation_data=(self.__val_tokens, self.__data_Set.get_y_val_values()))

            x = np.asarray(self.__data_Set.get_x_train_sentence_values())
            x_val = np.asarray(self.__data_Set.get_x_val_sentence_values())
            self.model.fit(x, self.__data_Set.get_y_train_values(), batch_size=batch_size,
                           verbose=1, epochs=epochs, validation_data=(x_val, self.__data_Set.get_y_val_values()))
            check = True
        # elif self.model_select and self.__load_data:
        #     check = True
        #     self.__vectorize_layer.adapt(self.__vocabulary)
        #
        #     train_sentence, test_sentence, val_sentence = self.__get_train_test_val_sentence()
        #     self.__set_tokens(train_sentence, test_sentence, val_sentence)
        #
        #     self.__blstm_model.fit(self.__train_tokens, self.__train_targets, batch_size=batch_size, verbose=1,
        #                                    epochs=epochs,
        #                                    validation_data=(self.__val_tokens, self.__val_targets))

        return check

    def evaluate_model(self):
        loss = None
        accuracy = None

        if self.__created_model:
            loss, accuracy = self.model.evaluate(np.asarray(self.__data_Set.get_x_test_sentence_values()), self.__data_Set.get_y_test_values())
        # elif self.model_select and self.__load_data:
        #     if self.__test_tokens != None:
        #         train_sentence, test_sentence, val_sentence = self.__get_train_test_val_sentence()
        #         self.__set_tokens(train_sentence, test_sentence, val_sentence)
        #
        #     loss, accuracy = self.__blstm_model.evaluate(self.__test_tokens, self.__test_targets)

        return loss, accuracy

    def save_model(self, file_path=''):
        if self.__created_model or self.model_select:
            self.__dir_model_current = str(file_path) + self.__name_model
            self.model.save(self.__dir_model_current)

        return self.__created_model

    def load_model(self, file_path='', name_model='trained_model', show_summary=False):
        self.__dir_model_current = file_path + name_model
        self.model = tf.keras.models.load_model(file_path + name_model,
                                                custom_objects={"custom_standardization": custom_standardization})

        vectorize_model = self.model.layers[1]
        blstm_model = self.model.layers[2]

        vectorize_layer = vectorize_model.layers[0]
        # self.__vocabulary = self.__vectorize_layer.get_vocabulary()

        # Optimiser
        adam = keras.optimizers.Adam(learning_rate=0.0005, beta_1=0.9, beta_2=0.999)

        # Compile model
        blstm_model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        if show_summary:
            vectorize_model.summary()
            blstm_model.summary()
            self.model.summary()

        self.model_select = True
        self.__created_model = False

        return self.model_select

    def predict(self, address_list):
        result = None
        if self.model_select or self.__created_model:
            result = self.model.predict(address_list)

        return np.round(result, decimals=2)
        # return result

    def process_address(self, address_list):
        classification = self.predict(address_list)

        list_address_classified = []
        index_address = 0
        for raw_address in classification:
            components = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
            probability = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}



            pre_presses_text = custom_standardization(address_list[index_address])
            words = str(pre_presses_text.numpy().decode('utf-8')).split()

            max_probability = np.amax(raw_address[0:len(words)], axis=1)

            for i in range(len(max_probability)):  # Lista de probabilidades
                index_tag = (int(np.where(raw_address[i] == max_probability[i])[0]))
                components[index_tag] += [words[i]]
                probability[index_tag] += [max_probability[i]]

            #     'house_num ,  locality ,  municipality ,  province ,  rw ,  street_1 ,  street_2 ,  street_3'
            list_address_classified.append(
                classification(street_1=components[5], street_2=components[6], street_3=components[7],
                                   locality=components[1], municipality=components[2], province=components[3],
                                   house_number=components[0], reserved_word=components[4],
                                   probability_1=probability[5], probability_2=probability[6],
                                   probability_3=probability[7],
                                   probability_locality=probability[1], probability_municipality=probability[2],
                                   probability_province=probability[3],
                                   probability_house_number=probability[0], probability_reserve_word=probability[4]))
            index_address += 1
        return list_address_classified

    def plot_model(self):
        plot_model(self.__vectorize_model, 'vectorized_model.jpg')
        plot_model(self.__blstm_model, 'blstm_model.jpg')
        plot_model(self.model, 'end_model.jpg')


def custom_standardization(input_string):
    """ transforms words into lowercase and deletes punctuations """
    lowercas = tf.strings.lower(input_string)

    stripped_spanish = tf.strings.regex_replace(lowercas,
                                                'á', 'a')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                'é', 'e')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                'í', 'i')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                'ó', 'o')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                'ú', 'u')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                'ü', 'u')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                ',', ' ')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                ';', ' ')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                'entre', 'entre ')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                'e /', 'entre ')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                'e/', 'entre ')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                '#', 'num ')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                'apt.', 'apt. ')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                'apartamento', 'apartamento ')
    stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                '/', 'entre ')

    output = tf.strings.regex_replace(
        stripped_spanish, '[%s]' % re.escape(string.punctuation), '')
    return output


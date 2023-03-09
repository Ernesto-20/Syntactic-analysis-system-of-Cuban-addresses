import re

import keras.optimizers
import tensorflow as tf
import string
from tensorflow import keras
from tensorflow.python.client.session import Session
from tensorflow.python.ops.ragged.ragged_string_ops import ngrams
from keras_preprocessing.sequence import pad_sequences
from keras.layers.core import Activation, Dropout, Dense
from tensorflow.python.ops.ragged.ragged_string_ops import string_bytes_split
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import pandas as pd
import numpy as np
from keras.layers import TextVectorization
from keras.utils import plot_model

from keras import Sequential, Model, Input
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional, Concatenate

from numpy.random import seed

from src.utils.data_set import DataSet


class NeuralModel:

    def create_model(self, data_set: DataSet, name_model='default_model'):
        output_dim = 64
        input_length = 25

        tv_by_character = self.__create_layer_vectorization(name='TextVectorization_Character',
                                                            max_len=data_set.get_max_len_character(),
                                                            vocabulary=data_set.get_vocabulary(),
                                                            split=string_bytes_split)
        vocab_size_character = len(tv_by_character.get_layer('text_vectorization').get_vocabulary())

        tv_by_trigram = self.__create_layer_vectorization(name='TextVectorization_Trigram',
                                                          max_len=data_set.get_max_len_trigram(),
                                                          vocabulary=data_set.get_vocabulary(), split=split_and_remove_spacewhite)
        vocab_size_trigram = len(tv_by_trigram.get_layer('text_vectorization_1').get_vocabulary())
        # print('VOCABULARY TRIGRAM:')
        # print(tv_by_trigram.get_layer('text_vectorization_1').get_vocabulary())

        tv_by_word = self.__create_layer_vectorization(name='TextVectorization_Word',
                                                            max_len=data_set.get_max_len_character(),
                                                            vocabulary=data_set.get_vocabulary(), )

        BLSTM_Character = self.__create_layer_blsm_and_embedding(name='Bidirectional_LSMT_Character',
                                                                 input_dim=(data_set.get_max_len_character(),),
                                                                 vocab_size=vocab_size_character, output_dim=output_dim,
                                                                 input_length=input_length)

        BLSTM_Trigram = self.__create_layer_blsm_and_embedding(name='Bidirectional_LSMT_Trigram',
                                                               input_dim=(data_set.get_max_len_trigram(),),
                                                               vocab_size=vocab_size_trigram, output_dim=output_dim,
                                                               input_length=input_length)

        inputs = keras.Input(shape=(1,), dtype="string")
        outputs_branch_character = BLSTM_Character(tv_by_character(inputs))
        outputs_branch_trigram = BLSTM_Trigram(tv_by_trigram(inputs))
        print('Max_len_word: ', data_set.get_max_len_word())
        embedding_word = self.__create_layer_embedding(name='Embedding_Word', input_dim=(data_set.get_max_len_character(),),
                                                       vocab_size=len(data_set.get_vocabulary()), output_dim=output_dim,
                                                       input_length=input_length)
        outputs_embedding_word = embedding_word(tv_by_word(inputs))

        concatenated_branch_trigram_with_character = Concatenate()([outputs_branch_character, outputs_branch_trigram])
        BLSTM_Concatenated = Bidirectional(LSTM(units=output_dim, return_sequences=True, dropout=0.4, recurrent_dropout=0.4), merge_mode='sum')
        outputs_BLSTM_Concatenated = BLSTM_Concatenated(concatenated_branch_trigram_with_character)

        print('BLSTM_Concatenated: input_shape: ', BLSTM_Concatenated.input_shape, '  output_shape: ', BLSTM_Concatenated.output_shape)
        print('embedding_word: input_shape: ', embedding_word.input_shape, '  output_shape: ',embedding_word.output_shape)

        concatenated_branch_concatenated1_with_word = Concatenate()([outputs_BLSTM_Concatenated, outputs_embedding_word])
        BLSTM_Concatenated2 = Bidirectional(LSTM(units=output_dim), merge_mode='sum')(concatenated_branch_concatenated1_with_word)

        output = BLSTM_Concatenated2
        model = keras.Model(inputs, output, name='Model')

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def __create_layer_embedding(self, name, input_dim, vocab_size, output_dim, input_length):
        model = Sequential(name=name)

        # Add Input layer
        model.add(Input(shape=input_dim, dtype=tf.int32))

        # Add Embedding layer
        model.add(Embedding(input_dim=vocab_size, output_dim=output_dim, input_length=input_length))

        return model

    def __create_layer_blsm_and_embedding(self, name, input_dim, vocab_size, output_dim, input_length):
        model = Sequential(name=name)

        # Add Input layer
        model.add(Input(shape=input_dim, dtype=tf.int32))

        # Add Embedding layer
        model.add(Embedding(input_dim=vocab_size, output_dim=output_dim, input_length=input_length))

        # Add bidirectional LSTM
        model.add(Bidirectional(LSTM(units=output_dim, return_sequences=True, dropout=0.4, recurrent_dropout=0.4),
                                merge_mode='sum'))

        return model

    def __create_layer_blsm(self, name, input_dim, output_dim):
        model = Sequential(name=name)

        # Add Input layer
        model.add(Input(shape=input_dim, dtype=tf.int32))

        # Add bidirectional LSTM
        model.add(Bidirectional(LSTM(units=output_dim, return_sequences=True, dropout=0.4, recurrent_dropout=0.4),
                                merge_mode='sum'))

        return model

    def __create_layer_vectorization(self, name, max_len, vocabulary, ngrams=None, split="whitespace"):
        vectorize_layer = TextVectorization(
            standardize=custom_standardization,
            output_mode="int",
            output_sequence_length=max_len,
            ngrams=ngrams,
            split=split
        )

        vectorize_layer.adapt(vocabulary)

        vectorize_layer_model = Sequential(name=name)
        vectorize_layer_model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
        vectorize_layer_model.add(vectorize_layer)

        return vectorize_layer_model


def split_and_remove_spacewhite(input_data):
    result = tf.strings.regex_replace(input_data, ' ', '')
    result = string_bytes_split(result)
    return ngrams(result, ngram_width=3)
    #
    # result = tf.strings.regex_replace(input_data, ' ', '')
    # return string_bytes_split(result)

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

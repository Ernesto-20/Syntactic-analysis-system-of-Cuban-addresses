from typing import Callable

import keras
import keras.optimizers
from keras.utils import plot_model
import numpy as np
from tensorflow.python.keras.engine.functional import Functional
import tensorflow as tf
from keras import Sequential
from keras.layers import LSTM, Embedding, Dense, Bidirectional, Concatenate, Reshape, Flatten
from keras.layers import TextVectorization
from tensorflow.python.ops.ragged.ragged_string_ops import string_bytes_split
from src.neural_networks.neural_parser import NeuralParser
from src.tools.address_data_set import DataSet


class DeepParserConfig:
    def __init__(self, output_emb_char,
               output_emb_trigram,
               output_emb_word,
               units_char_blstm,
               units_trigram_blstm,
               units_word_blstm,
               dropout_char_blstm,
               dropout_trigram_blstm,
               rdropout_char_blstm,
               rdropout_trigram_blstm,
               dropout_char_trigram_blstm,
               rdropout_char_trigram_blstm,
               dropout_char_trigram_word_blstm,
               rdropout_char_trigram_word_blstm,
               learning_rate,
               ):
        self.__output_emb_char = output_emb_char
        self.__output_emb_trigram = output_emb_trigram
        self.__output_emb_word = output_emb_word
        self.__units_char_blstm = units_char_blstm
        self.__units_trigram_blstm = units_trigram_blstm
        self.__units_word_blstm = units_word_blstm

        self.__dropout_char_blstm = dropout_char_blstm
        self.__dropout_trigram_blstm = dropout_trigram_blstm
        self.__rdropout_char_blstm = rdropout_char_blstm
        self.__rdropout_trigram_blstm = rdropout_trigram_blstm
        self.__dropout_char_trigram_blstm = dropout_char_trigram_blstm
        self.__rdropout_char_trigram_blstm = rdropout_char_trigram_blstm
        self.__dropout_char_trigram_word_blstm = dropout_char_trigram_word_blstm
        self.__rdropout_char_trigram_word_blstm = rdropout_char_trigram_word_blstm

        self.__learning_rate = learning_rate

    def get_output_emb_char(self):
        return self.__output_emb_char

    def get_output_emb_trigram(self):
        return self.__output_emb_trigram

    def get_output_emb_word(self):
        return self.__output_emb_word

    def get_units_char_blstm(self):
        return self.__units_char_blstm

    def get_units_trigram_blstm(self):
        return self.__units_trigram_blstm

    def get_units_word_blstm(self):
        return self.__units_word_blstm

    def get_dropout_char_blstm(self):
        return self.__dropout_char_blstm

    def get_dropout_trigram_blstm(self):
        return self.__dropout_trigram_blstm

    def get_rdropout_char_blstm(self):
        return self.__rdropout_char_blstm

    def get_rdropout_trigram_blstm(self):
        return self.__rdropout_trigram_blstm

    def get_dropout_char_trigram_blstm(self):
        return self.__dropout_char_trigram_blstm

    def get_rdropout_char_trigram_blstm(self):
        return self.__rdropout_char_trigram_blstm

    def get_dropout_char_trigram_word_blstm(self):
        return self.__dropout_char_trigram_word_blstm

    def get_rdropout_char_trigram_word_blstm(self):
        return self.__rdropout_char_trigram_word_blstm

    def get_learning_rate(self):
        return self.__learning_rate


class DeepParserModel(NeuralParser):

    def __init__(self, data_set: DataSet, cleaner_method, config=None, model=None):
        self.__data = data_set
        self.__cleaner_method = cleaner_method

        if config is None:
            self.__config = DeepParserConfig(
                output_emb_char=128,
                output_emb_trigram=128,
                output_emb_word=64,
                units_char_blstm=32,
                units_trigram_blstm=32,
                units_word_blstm= 30,
                dropout_char_blstm=0,
                dropout_trigram_blstm=0,
                rdropout_char_blstm=0,
                rdropout_trigram_blstm=0,
                dropout_char_trigram_blstm=0.3,
                rdropout_char_trigram_blstm=0,
                dropout_char_trigram_word_blstm=0.4,
                rdropout_char_trigram_word_blstm=0,
            )
        elif isinstance(config, DeepParserConfig):
            self.__config = config
        else:
            print('Retornar una Excepcion')

        if model is None:
            self._create_model()
        # elif type(model) is not Functional:
        #     raise NotImplementedError('Model variable could be Keras.Model instance')
        else:
            self.__model = model

    def _create_model(self):
        inputs = keras.Input(shape=(1,), dtype="string", name='Input')
        tv_by_character = self._create_layer_vectorization(name='Character_TextVectorization',
                                                            max_len=self.__data.get_max_len_character(),
                                                            split=string_bytes_split)
        vocab_size_character = len(tv_by_character.get_layer('text_vectorization').get_vocabulary())
        layer_tv_character = tv_by_character(inputs)
        tv_by_trigram = self._create_layer_vectorization(name='Trigram_TextVectorization',
                                                          max_len=self.__data.get_max_len_trigram(),
                                                          split=string_bytes_split,
                                                          ngrams=3)
        vocab_size_trigram = len(tv_by_trigram.get_layer('text_vectorization_1').get_vocabulary())
        layer_tv_by_trigram = tv_by_trigram(inputs)
        tv_by_word = self._create_layer_vectorization(name='Word_TextVectorization',
                                                       max_len=self.__data.get_max_len_word())
        vocab_size_word = len(tv_by_word.get_layer('text_vectorization_2').get_vocabulary())
        layer_tv_by_word = tv_by_word(inputs)
        embedding_character = Embedding(vocab_size_character, self.__config.get_output_emb_char(),
                                        name='Character_Embedding')
        layer_embedding_character = embedding_character(layer_tv_character)
        blstm_character = Bidirectional(LSTM(units=self.__config.get_units_char_blstm(), return_sequences=True,
                                             dropout=self.__config.get_dropout_char_blstm(),
                                             recurrent_dropout=self.__config.get_rdropout_char_blstm()),
                                        merge_mode='concat', name='Character_BLSTM')
        layer_blstm_character = blstm_character(layer_embedding_character)
        embedding_trigram = Embedding(vocab_size_trigram, self.__config.get_output_emb_trigram(),
                                      name='Trigram_Embedding')
        layer_embedding_trigram = embedding_trigram(layer_tv_by_trigram)
        blstm_trigram = Bidirectional(LSTM(units=self.__config.get_units_trigram_blstm(), return_sequences=True,
                                           dropout=self.__config.get_dropout_trigram_blstm(),
                                           recurrent_dropout=self.__config.get_rdropout_trigram_blstm()),
                                      merge_mode='concat', name='Trigram_BLSTM')
        layer_blstm_trigram = blstm_trigram(layer_embedding_trigram)
        embedding_word = Embedding(vocab_size_word, self.__config.get_output_emb_word(), name='Word_Embedding')
        layer_embedding_word = embedding_word(layer_tv_by_word)
        concat = Concatenate(name='Character_Trigram_Concat')([layer_blstm_character, layer_blstm_trigram])
        blstm_concat = Bidirectional(
            LSTM(units=self.__data.get_max_len_word(), return_sequences=False,
                 dropout=self.__config.get_dropout_char_trigram_blstm(),
                 recurrent_dropout=self.__config.get_rdropout_char_trigram_blstm()),
            merge_mode='sum', name='Character_Trigram_BLSTM')
        layer_blstm_concat = blstm_concat(concat)

        # ********* PROJECTION LAYER ***************
        projection = Reshape((self.__data.get_max_len_word(), 1), name='Character_Trigram_Projection')(
            layer_blstm_concat)
        concat_2 = Concatenate(name='Word_Projection_Concat')([projection, layer_embedding_word])
        # ********* PROJECTION LAYER ***************

        blstm_concat_2 = Bidirectional(
            LSTM(units=self.__config.get_units_word_blstm(), return_sequences=True,
                 dropout=self.__config.get_dropout_char_trigram_word_blstm(),
                 recurrent_dropout=self.__config.get_rdropout_char_trigram_word_blstm()),
            merge_mode='concat', name='Word_Projection_BLSTM')
        layer_blstm_concat_2 = blstm_concat_2(concat_2)
        output = Dense(self.__data.get_n_tag(), activation='softmax', name='Classifier')(layer_blstm_concat_2)
        model = keras.Model(inputs, output, name='DeepParser')
        # Optimiser
        opt = keras.optimizers.Adam(learning_rate=0.0005)
        # metrics = [tf.metrics.CategoricalAccuracy(), tf.metrics.Precision(), tf.metrics.Recall(), DeepParserModel.my_metric]
        metrics = [DeepParserModel.precision]
        # metrics = [tf.metrics.Accuracy()]
        # Accuracy tells you how many times the ML model was correct overall.
        # Precision is how good the model is at predicting a specific category.
        # Recall tells you how many times the model was able to detect a specific category.
        model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=metrics)
        model.summary()
        self.__model = model
        # plot_model(model, 'DeepParse_Architecture.png')

    @staticmethod
    @tf.keras.utils.register_keras_serializable()
    def precision(y_true, y_pred):

        result = tf.equal(tf.argmax(y_true, axis=-1), tf.argmax(y_pred, axis=-1))
        result = tf.reduce_sum(tf.cast(result, tf.float32))

        corrects_number = result
        wrongs_number = (float(len(y_pred)) * len(y_pred[0])) - corrects_number

        true_positive = corrects_number
        false_positive = wrongs_number
        # false_negative = wrongs_number
        # true_negative = corrects_number * (class_number - 1) + wrongs_number * (class_number - 2)

        return true_positive/(true_positive + false_positive)

    def _create_layer_vectorization(self, name, max_len, ngrams=None, split="whitespace"):
        vectorize_layer = TextVectorization(
            standardize=self.__cleaner_method,
            output_mode="int",
            output_sequence_length=max_len,
            ngrams=ngrams,
            split=split
        )

        vectorize_layer.adapt(self.__data.get_vocabulary())

        vectorize_layer_model = Sequential(name=name)
        vectorize_layer_model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
        vectorize_layer_model.add(vectorize_layer)

        return vectorize_layer_model

    @property
    def cleaner_method(self) -> Callable:
        return self.__cleaner_method

    @property
    def data(self) -> DataSet:
        return self.__data

    @property
    def model(self) -> keras.Model:
        return self.__model

    @property
    def config(self) -> DeepParserConfig:
        return self.__config

import keras
import keras.optimizers
import numpy as np
import tensorflow as tf
from keras import Sequential
from keras.layers import LSTM, Embedding, Dense, Bidirectional, Concatenate, Reshape, Flatten
from keras.layers import TextVectorization
from tensorflow.python.ops.ragged.ragged_string_ops import ngrams
from tensorflow.python.ops.ragged.ragged_string_ops import string_bytes_split

from src.neural_networks.neural_parser import NeuralParser
from src.tools.address_cleaner import AddressCleaner
from src.tools.address_data_set import DataSet
from src.tools.decoder import Decoder
import string


class DeepParserModel(NeuralParser):

    def __init__(self, data_set: DataSet, address_cleaner: AddressCleaner, model=None):
        self.data = data_set
        self.address_cleaner = address_cleaner
        if model is None:
            output_dim = 100
            input_length = 25

            inputs = keras.Input(shape=(1,), dtype="string")

            tv_by_character = self.__create_layer_vectorization(name='TextVectorization_Character',
                                                                max_len=data_set.get_max_len_character(),
                                                                split=string_bytes_split)
            vocab_size_character = len(tv_by_character.get_layer('text_vectorization').get_vocabulary())
            layer_tv_character = tv_by_character(inputs)

            tv_by_trigram = self.__create_layer_vectorization(name='TextVectorization_Trigram',
                                                              max_len=data_set.get_max_len_trigram(),
                                                              split=string_bytes_split,
                                                              ngrams=3)
            vocab_size_trigram = len(tv_by_trigram.get_layer('text_vectorization_1').get_vocabulary())
            layer_tv_by_trigram = tv_by_trigram(inputs)

            tv_by_word = self.__create_layer_vectorization(name='TextVectorization_Word',
                                                           max_len=data_set.get_max_len_word())
            vocab_size_word = len(tv_by_word.get_layer('text_vectorization_2').get_vocabulary())
            layer_tv_by_word = tv_by_word(inputs)

            embedding_character = Embedding(vocab_size_character, 25, name='Embedding_Character')
            layer_embedding_character = embedding_character(layer_tv_character)
            blstm_character = Bidirectional(LSTM(units=25, return_sequences=True, dropout=0.6, recurrent_dropout=0.1),
                                            merge_mode='concat')
            layer_blstm_character = blstm_character(layer_embedding_character)

            embedding_trigram = Embedding(vocab_size_trigram, 25, name='Embedding_Trigram')
            layer_embedding_trigram = embedding_trigram(layer_tv_by_trigram)
            blstm_trigram = Bidirectional(LSTM(units=25, return_sequences=True, dropout=0.6, recurrent_dropout=0.1),
                                          merge_mode='concat')
            layer_blstm_trigram = blstm_trigram(layer_embedding_trigram)

            embedding_word = Embedding(vocab_size_word, output_dim, name='Embedding_Word')
            layer_embedding_word = embedding_word(layer_tv_by_word)
            concat = Concatenate()([layer_blstm_character, layer_blstm_trigram])
            blstm_concat = Bidirectional(
                LSTM(units=output_dim, return_sequences=True, dropout=0.2, recurrent_dropout=0.1),
                merge_mode='concat')
            layer_blstm_concat = blstm_concat(concat)

            # ********* LAYER PROJECT ***************
            projection = Flatten()(layer_blstm_concat)
            projection = Dense(units=data_set.get_max_len_word() * 100)(projection)
            projection = Reshape((data_set.get_max_len_word(), 100))(projection)
            # ********* LAYER PROJECT ***************

            concat_2 = Concatenate()([projection, layer_embedding_word])
            blstm_concat_2 = Bidirectional(
                LSTM(units=data_set.get_n_tag(), return_sequences=True, dropout=0, recurrent_dropout=0),
                merge_mode='sum')
            layer_blstm_concat_2 = blstm_concat_2(concat_2)

            output = Dense(data_set.get_n_tag(), activation='softmax')(layer_blstm_concat_2)
            model = keras.Model(inputs, output, name='Model')

            # opt = keras.optimizers.Adam(learning_rate=0.0005)

            # Optimiser
            opt = keras.optimizers.Adam(learning_rate=0.0005, beta_1=0.9, beta_2=0.999)

            # metrics = [tf.metrics.Accuracy(), tf.metrics.Recall(), tf.metrics.Precision()]
            metrics = [tf.metrics.Accuracy()]
            # Accuracy tells you how many times the ML model was correct overall.
            # Precision is how good the model is at predicting a specific category.
            # Recall tells you how many times the model was able to detect a specific category.

            model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
            # model.summary()
            self.model = model
            # plot_model(model, 'DeepParse_Architecture.jpg')
        elif type(model) is not keras.Model:
            raise NotImplementedError('model variable could be Keras.Model instance')
        else:
            self.model = model

    def __create_layer_vectorization(self, name, max_len, ngrams=None, split="whitespace"):
        vectorize_layer = TextVectorization(
            standardize=self.address_cleaner.custom_standardization,
            output_mode="int",
            output_sequence_length=max_len,
            ngrams=ngrams,
            split=split
        )

        vectorize_layer.adapt(self.get_data().get_vocabulary())

        vectorize_layer_model = Sequential(name=name)
        vectorize_layer_model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
        vectorize_layer_model.add(vectorize_layer)

        return vectorize_layer_model

    def train(self, batch_size=1200, epochs=50):
        x = np.asarray(self.data.get_x_train_sentence_values())
        x_val = np.asarray(self.data.get_x_val_sentence_values())
        self.model.fit(x, self.data.get_y_train_values(), batch_size=batch_size,
                       verbose=1, epochs=epochs, validation_data=(x_val, self.data.get_y_val_values()))

    def predict(self, address_list: list):
        address_list = preprocessing(address_list)
        result = self.model.predict(address_list)
        # print('\n\n\n\n\n\n')
        # print(np.round(result, decimals=2))
        # print('\n\n\n\n\n\n')
        return np.round(result, decimals=2)

    def evaluate(self):
        loss, accuracy, recall, precision = self.model.evaluate(
            np.asarray(self.__data_Set.get_x_test_sentence_values()),
            self.__data_Set.get_y_test_values())

        return loss, accuracy

    def get_address_cleaner(self) -> AddressCleaner:
        return self.address_cleaner

    def get_data(self) -> DataSet:
        return self.data

    def get_model(self) -> keras.Model:
        return self.model


def split_and_remove_spacewhite(input_data):
    # Puede que se elimine
    result = tf.strings.regex_replace(input_data, ' ', '')
    result = string_bytes_split(result)
    return ngrams(result, ngram_width=3)


def preprocessing(address):
    temp = []
    for sentence in address:
        some_punctuations = ['á', 'ä', 'Á', 'Ä', 'é', 'ë', 'É', 'Ë', 'í', 'ï', 'Í', 'Ï', 'ó', 'ö', 'Ó', 'Ö', 'ú', 'ü',
                             'Ú', 'Ü']
        stripped_spanish = ''.join(ch for ch in sentence if ch in string.printable or ch in some_punctuations)
        temp.append(stripped_spanish)

    return temp

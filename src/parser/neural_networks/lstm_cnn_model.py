import keras
import numpy as np
import tensorflow as tf
from keras import Sequential
from keras.layers import Reshape, TimeDistributed, Embedding, Dropout, MaxPooling1D, Flatten, Bidirectional, LSTM, \
    Concatenate, Dense, TextVectorization
from tensorflow.python.ops.ragged.ragged_string_ops import string_bytes_split
from transformers import Conv1D


from parser.neural_networks.neural_parser import NeuralParser
from src.tools.address_cleaner import AddressCleaner
from noise_generator.address_data_set import DataSet



class LstmCnnModel(NeuralParser):

    def __init__(self, data_set: DataSet, address_cleaner: AddressCleaner, model=None):
        self.data = data_set
        self.address_cleaner = address_cleaner
        if model is None:
            output_dim = 100

            inputs = keras.Input(shape=(1,), dtype="string")

            # CHARACTER VECTORIZATION PROCESS
            tv_by_character = self.__create_layer_vectorization(name='TextVectorization_Character',
                                                                max_len=self.data.get_max_len_character(),
                                                                vocabulary=self.data.get_vocabulary(),
                                                                split=string_bytes_split)
            vocab_size_character = len(tv_by_character.get_layer('text_vectorization').get_vocabulary())
            layer_tv_character = tv_by_character(inputs)

            # TRIGRAM VECTORIZATION PROCESS
            tv_by_trigram = self.__create_layer_vectorization(name='TextVectorization_Trigram',
                                                              max_len=self.data.get_max_len_trigram(),
                                                              vocabulary=self.data.get_vocabulary(),
                                                              split=string_bytes_split,
                                                              ngrams=3)
            vocab_size_trigram = len(tv_by_trigram.get_layer('text_vectorization_1').get_vocabulary())
            print(vocab_size_trigram)
            layer_tv_by_trigram = tv_by_trigram(inputs)

            # WORD VECTORIZATION PROCESS
            tv_by_word = self.__create_layer_vectorization(name='TextVectorization_Word',
                                                           max_len=self.data.get_max_len_word(),
                                                           vocabulary=self.data.get_vocabulary(), )
            vocab_size_word = len(tv_by_word.get_layer('text_vectorization_2').get_vocabulary())
            layer_tv_by_word = tv_by_word(inputs)

            # CHARACTER PROCESS
            layer_tv_character_reshape = Reshape((-1, tv_by_character.output_shape[1]))(layer_tv_character)
            time_embedding_character = TimeDistributed(
                Embedding(vocab_size_character, 25, name='Embedding_Character'))
            layer_time_emb = time_embedding_character(layer_tv_character_reshape)
            dropout_character = Dropout(0.68)
            layer_time_dropout = dropout_character(layer_time_emb)
            time_conv_1d_character = TimeDistributed(Conv1D(kernel_size=3, filters=25,
                                                            padding='same', activation='relu', strides=1))
            layer_time_conv_1d_character = time_conv_1d_character(layer_time_dropout)
            max_pooling_1d_character = TimeDistributed(MaxPooling1D(vocab_size_character))
            layer_max_pooling_1d_character = max_pooling_1d_character(layer_time_conv_1d_character)
            time_flatten_character = TimeDistributed(Flatten())
            layer_time_flatten_character = time_flatten_character(layer_max_pooling_1d_character)
            blstm_character = Bidirectional(
                LSTM(units=25, return_sequences=True, dropout=0.6, recurrent_dropout=0.1),
                merge_mode='concat')
            layer_blstm_character = blstm_character(layer_time_flatten_character)

            # TRIGRAM PROCESS
            layer_tv_trigram_reshape = Reshape((-1, tv_by_trigram.output_shape[1]))(layer_tv_by_trigram)
            time_embedding_trigram = TimeDistributed(Embedding(vocab_size_trigram, 25, name='Embedding_Trigrams'))
            layer_time_emb_trigram = time_embedding_trigram(layer_tv_trigram_reshape)
            dropout_trigram = Dropout(0.68)
            layer_time_dropout = dropout_trigram(layer_time_emb_trigram)
            time_conv_1d_trigram = TimeDistributed(Conv1D(kernel_size=3, filters=25,
                                                          padding='same', activation='relu', strides=1))
            layer_time_conv_1d_trigram = time_conv_1d_trigram(layer_time_dropout)
            max_pooling_1d_trigram = TimeDistributed(MaxPooling1D(pool_size=3, strides=1))
            layer_max_pooling_1d_trigram = max_pooling_1d_trigram(layer_time_conv_1d_trigram)
            time_flatten_trigram = TimeDistributed(Flatten())
            layer_time_flatten_trigram = time_flatten_trigram(layer_max_pooling_1d_trigram)
            blstm_trigram = Bidirectional(LSTM(units=25, return_sequences=True, dropout=0.6, recurrent_dropout=0.1),
                                          merge_mode='concat')
            layer_blstm_trigram = blstm_trigram(layer_time_flatten_trigram)

            # CONCATENATE TRIGRAM CHARACTER PROCESS
            layer_character_trigram_concat = Concatenate()([layer_blstm_character, layer_blstm_trigram])
            blstm_concat_character_trigram = Bidirectional(
                LSTM(units=output_dim, return_sequences=True, dropout=0.2, recurrent_dropout=0.1),
                merge_mode='concat')
            layer_blstm_character_trigram_concat = blstm_concat_character_trigram(layer_character_trigram_concat)

            # WORD PROCESS USING 2xLSTM+BLSTM
            embedding_word = Embedding(vocab_size_word, output_dim, name='Embedding_Word')
            layer_embedding_word = embedding_word(layer_tv_by_word)

            lstm_forward_layer = LSTM(units=output_dim, return_sequences=True,
                                      dropout=0.2,
                                      recurrent_dropout=0.1)(layer_embedding_word)
            lstm_forward_linear_layer = Dense(1, activation='linear')(lstm_forward_layer)
            lstm_forward_log_softmax_layer = Dense(5, activation='softmax')(lstm_forward_linear_layer)

            lstm_backward_layer = LSTM(units=output_dim, return_sequences=True,
                                       dropout=0.2, recurrent_dropout=0.1,
                                       go_backwards=True)(layer_embedding_word)
            lstm_backward_linear_layer = Dense(1, activation='linear')(lstm_backward_layer)
            lstm_backward_log_softmax_layer = Dense(5, activation='softmax')(lstm_backward_linear_layer)

            concatenate_layer = Concatenate()([lstm_forward_log_softmax_layer, lstm_backward_log_softmax_layer])
            blstm_lstm_concat_word = Bidirectional(
                LSTM(units=output_dim, return_sequences=True, dropout=0.2, recurrent_dropout=0.1),
                merge_mode='concat')
            layer_blstm_lstm_concat_word = blstm_lstm_concat_word(concatenate_layer)

            # CONCATENATE CHAR_TRIGRAM WORD PROCESS
            # ********* LAYER PROJECT ***************
            print(layer_blstm_character_trigram_concat)
            projection = Flatten()(layer_blstm_character_trigram_concat)
            projection = Dense(units=self.data.get_max_len_word() * 100)(projection)
            projection = Reshape((self.data.get_max_len_word(), 100))(projection)
            print(projection)
            # ********* LAYER PROJECT ***************

            concat_2 = Concatenate()([projection, layer_blstm_lstm_concat_word])
            blstm_concat_2 = Bidirectional(
                LSTM(units=self.data.get_n_tag(), return_sequences=True, dropout=0, recurrent_dropout=0),
                merge_mode='sum')
            layer_blstm_concat_2 = blstm_concat_2(concat_2)

            output = Dense(self.data.get_n_tag(), activation='softmax')(layer_blstm_concat_2)
            model_complex = keras.Model(inputs, output, name='Model')

            opt = tf.keras.optimizers.adam_v2.Adam(learning_rate=0.0005, beta_1=0.9, beta_2=0.999)
            model_complex.compile(loss='categorical_crossentropy',
                                  optimizer=opt,
                                  metrics=['accuracy'])
            model_complex.summary()

        self.model = model_complex
    def __create_layer_vectorization(self, name, max_len, ngrams=None, split="whitespace"):
        vectorize_layer = TextVectorization(
            standardize=self.cleaner_method,
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
        result = self.model.predict(address_list)
        return np.round(result, decimals=2)

    def evaluate(self):
        loss, accuracy, recall, precision = self.model.evaluate(
            np.asarray(self.__data_Set.get_x_test_sentence_values()),
            self.__data_Set.get_y_test_values())

        return loss, accuracy

    def get_cleaner_method(self):
        return self.cleaner_method

    def get_data(self) -> DataSet:
        return self.data

    def get_model(self) -> keras.Model:
        return self.model

    def set_data(self, data: DataSet) -> None:
        if data.get_n_tag() == self.data.get_n_tag():
            self.data = data
        else:
            raise NotImplementedError('The number of tags does not correspond to the trained network')

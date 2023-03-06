import pandas as pd


class DataSet:
    def __init__(self, vocabulary_word, max_len_character, max_len_trigram, max_len_word, n_tag, id_to_category, input_dim,
                 x_train_sentence, x_test_sentence, x_val_sentence, y_train, y_test, y_val):
        self.__vocabulary_word = vocabulary_word
        self.max_len_character = max_len_character
        self.max_len_trigram = max_len_trigram
        self.max_len_word = max_len_word
        self.__n_tag = n_tag
        self.__id_to_category = id_to_category
        self.__x_train_sentence = x_train_sentence
        self.__x_test_sentence = x_test_sentence
        self.__x_val_sentence = x_val_sentence
        self.__y_train = y_train
        self.__y_test = y_test
        self.__y_val = y_val
        self.__input_dim = input_dim

    def get_x_train_sentence_values(self):
        return self.__x_train_sentence

    def get_x_test_sentence_values(self):
        return self.__x_test_sentence

    def get_x_val_sentence_values(self):
        return self.__x_val_sentence

    def get_y_train_values(self):
        return self.__y_train

    def get_y_test_values(self):
        return self.__y_test

    def get_y_val_values(self):
        return self.__y_val

    def get_vocabulary(self):
        return self.__vocabulary_word

    def get_max_len_character(self):
        return self.max_len_character

    def get_max_len_trigram(self):
        return self.max_len_trigram

    def get_max_len_word(self):
        return self.max_len_word

    def get_n_tag(self):
        return self.__n_tag

    def get_input_dim(self):
        return self.__input_dim

    def get_id_to_category(self):
        return self.__id_to_category

import pandas as pd


class DataSet:
    def __init__(self, vocabulary, max_len_character, max_len_trigram, max_len_word, n_tag, id_to_category,
                 x_train, x_test, x_val, y_train, y_test, y_val):
        self.__vocabulary = vocabulary
        self.__max_len_character = max_len_character
        self.__max_len_trigram = max_len_trigram
        self.__max_len_word = max_len_word
        self.__n_tag = n_tag
        self.__id_to_category = id_to_category
        self.__x_train = x_train
        self.__x_test = x_test
        self.__x_val = x_val
        self.__y_train = y_train
        self.__y_test = y_test
        self.__y_val = y_val

    def get_x_train_values(self):
        return self.__x_train

    def get_x_test_values(self):
        return self.__x_test

    def get_x_val_values(self):
        return self.__x_val

    def get_y_train_values(self):
        return self.__y_train

    def get_y_test_values(self):
        return self.__y_test

    def get_y_val_values(self):
        return self.__y_val

    def get_vocabulary(self):
        return self.__vocabulary

    def get_max_len_character(self):
        return self.__max_len_character

    def get_max_len_trigram(self):
        return self.__max_len_trigram

    def get_max_len_word(self):
        return self.__max_len_word

    def get_n_tag(self):
        return self.__n_tag

    def get_id_to_category(self):
        return self.__id_to_category

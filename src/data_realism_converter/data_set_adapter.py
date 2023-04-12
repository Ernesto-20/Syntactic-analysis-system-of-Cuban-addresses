import pandas as pd
from keras.utils import pad_sequences, to_categorical
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.tools.address_data_set import DataSet


class DataSetAdapter:

    def adapt_data_set(self, data_set: DataFrame):
        # Parametrizar el porcentaje del tamaño de entrenamiento, prueba y validación
        print('create DS_W')

        data_set['Tag'] = data_set['Tag'].astype('category')
        data_set['Tag_id'] = data_set['Tag'].cat.codes
        id_to_category = pd.Series(data_set.Tag.values, index=data_set.Tag_id).to_dict()
        print(id_to_category)
        n_tag = len(id_to_category)
        input_dim = len(list(set(data_set['Word'].to_list()))) + 1
        # print('List: ',data_set['Word'].to_list())
        # print('\n\nInput_dim: ',input_dim)
        data_fillna = data_set.fillna(method='ffill', axis=0)
        # Groupby and collect columns
        group_addres = data_fillna.groupby(
            ['Sentence #'], as_index=False
        )[['Word', 'Tag', 'Tag_id']].agg(lambda x: list(x))

        features, targets = group_addres['Word'].tolist(), group_addres['Tag_id'].tolist()

        train_features, test_features, train_targets, test_targets = train_test_split(
            features, targets,
            train_size=0.8,
            test_size=0.2,
            random_state=42,
            shuffle=True,
        )
        train_features, val_features, train_targets, val_targets = train_test_split(
            train_features, train_targets,
            train_size=0.75,
            test_size=0.25,
            random_state=42,
            shuffle=True,
        )

        # Vocabulary is the list of all sentence of train set
        vocabulary_word = self.__get_sentence(train_features)

        train_features_sentence = self.__get_sentence(train_features)
        test_features_sentence = self.__get_sentence(test_features)
        val_features_sentence = self.__get_sentence(val_features)

        max_len_word = max([len(s) for s in group_addres['Word'].tolist()])
        # print('Max_len_word: ',max_len_word)
        max_len_characters = max(
            [len(''.join(s)) for s in group_addres['Word'].tolist()])  # Se cuenta tambien los signos de puntacion.
        max_len_trigram = max_len_characters

        train_targets = self.__get_tags(train_targets, n_tag, max_len_word)
        test_targets = self.__get_tags(test_targets, n_tag, max_len_word)
        val_targets = self.__get_tags(val_targets, n_tag, max_len_word)

        return DataSet(vocabulary_word, max_len_characters, max_len_trigram, max_len_word, n_tag, id_to_category,
                       input_dim,
                       train_features_sentence, test_features_sentence, val_features_sentence, train_targets,
                       test_targets, val_targets)

    def __get_sentence(self, words_list):
        sentence_list = []
        for feature in words_list:
            sentence = ''
            for word in feature:
                sentence += word + ' '
            # text = tf.expand_dims(sentence, -1)
            # text = str(text.numpy().decode('utf-8'))
            sentence_list.append([sentence])
        return sentence_list

    def __get_tags(self, data, n_tag, max_len, value=None):
        if value is None:
            value = n_tag - 1

        tags = pad_sequences(data, maxlen=max_len, dtype='int32', padding='post', value=value)
        tags = to_categorical(tags, num_classes=n_tag)

        return tags

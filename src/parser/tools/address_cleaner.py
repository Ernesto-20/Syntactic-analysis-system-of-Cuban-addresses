import re
import tensorflow as tf
import unicodedata


class AddressCleaner:

    @staticmethod
    def cleaner_method(method='custom_standardization'):
        if method == 'custom_standardization':
            return AddressCleaner._custom_standardization
        elif method == 'custom_standardization_v2':
            return AddressCleaner.__custom_standardization
        else:
            raise NotImplementedError('There is no such cleaning method')

    @staticmethod
    @tf.keras.utils.register_keras_serializable()
    def _custom_standardization(input_string):
        """ transforms words into lowercase and deletes punctuations """

        stripped_spanish = tf.strings.lower(input_string)

        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                        '1/2', 'medio')

        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'á', 'a')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'ä', 'a')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'Á', 'a')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'Ä', 'a')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'é', 'e')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'ë', 'e')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'É', 'e')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'Ë', 'e')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'í', 'i')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'ï', 'i')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'Í', 'i')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'Ï', 'i')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'ó', 'o')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'ö', 'o')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'Ó', 'o')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'Ö', 'o')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'ú', 'u')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'ü', 'u')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'Ú', 'u')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'Ü', 'u')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    ',', ' , ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    ';', ' , ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'ñ', 'n')
        # stripped_spanish = tf.strings.regex_replace(stripped_spanish,
        #                                             'entre', 'entre ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '#', ' # ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '%', ' % ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '@', 'a')
        # stripped_spanish = tf.strings.regex_replace(stripped_spanish,
        #                                             '&', ' y ')
        # stripped_spanish = tf.strings.regex_replace(stripped_spanish,
        #                                             '/', '/ ')
        # stripped_spanish = tf.strings.regex_replace(stripped_spanish,
        #                                             'apt.', 'apt. ')
        # stripped_spanish = tf.strings.regex_replace(stripped_spanish,
        #                                             'apt', 'apt ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'apartamento', ' apartamento ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish, '[^a-zA-Z0-9 -/]', '')

        stripped_spanish = tf.strings.regex_replace(
            stripped_spanish, '[%s]' % re.escape(r"""!"$&'()*+-.;<=>?@[]^_`{|}~"""), '')

        output = tf.strings.regex_replace(stripped_spanish, 'medio','1/2 ')

        return output

    @staticmethod
    @tf.keras.utils.register_keras_serializable()
    def __custom_standardization(input_string):
        """Transforms words into lowercase and deletes punctuations"""

        stripped_spanish = tf.strings.lower(input_string)
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '½', 'medio1')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '1/2', 'medio2')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '1 / 2', 'medio3')
        replacements = {
            'á': 'a', 'ä': 'a', 'Á': 'a', 'Ä': 'a',
            'é': 'e', 'ë': 'e', 'É': 'e', 'Ë': 'e',
            'í': 'i', 'ï': 'i', 'Í': 'i', 'Ï': 'i',
            'ó': 'o', 'ö': 'o', 'Ó': 'o', 'Ö': 'o',
            'ú': 'u', 'ü': 'u', 'Ú': 'u', 'Ü': 'u',
            ',': ' , ', ';': ' , ', 'ñ': 'n',
            '#': ' # ', '%': ' % ', '@': 'a',
            'apartamento': ' apartamento ',
        }

        for search, replace in replacements.items():
            stripped_spanish = tf.strings.regex_replace(stripped_spanish, search, replace)

        stripped_spanish = tf.strings.regex_replace(stripped_spanish, '[^a-zA-Z0-9 -/]', '')

        stripped_spanish = tf.strings.regex_replace(
            stripped_spanish, '[%s]' % re.escape(r"""!"$&'()*+-;<=>?@[]^_`{|}~"""), '')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish, 'medio1','½')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish, 'medio2','1/2')
        output = tf.strings.regex_replace(stripped_spanish, 'medio3','1 / 2')

        return output

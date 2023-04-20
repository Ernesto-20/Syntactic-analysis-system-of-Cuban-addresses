import re
import string
import tensorflow as tf


class AddressCleaner:

    @staticmethod
    def cleaner_method(method='custom_standardization'):
        if method == 'custom_standardization':
            return AddressCleaner.__custom_standardization
        else:
            raise NotImplementedError('There is no such cleaning method')

    @staticmethod
    @tf.keras.utils.register_keras_serializable()
    def __custom_standardization(input_string):
        """ transforms words into lowercase and deletes punctuations """

        stripped_spanish = tf.strings.lower(input_string)

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
                                                    ',', ' ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    ';', ' ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'entre', 'entre ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'e /', ' entre ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'e/', ' entre ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '#', ' num ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'apt.', 'apt. ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'apartamento', 'apartamento ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '/', ' entre ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish, '[^a-zA-Z0-9 -]', '')

        output = tf.strings.regex_replace(
            stripped_spanish, '[%s]' % re.escape(string.punctuation), '')

        return output


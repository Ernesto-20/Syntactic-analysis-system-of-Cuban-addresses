import re
import tensorflow as tf


class AddressCleaner:

    @staticmethod
    def cleaner_method(method='custom_standardization'):
        if method == 'custom_standardization':
            return AddressCleaner.__custom_standardization
        elif method == 'custom_standardization_v2':
            return AddressCleaner.__custom_standardization_v2
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
                                                    ',', ' , ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    ';', ' , ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'ñ', 'n')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'entre', 'entre ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '#', ' # ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '%', ' % ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '@', 'a')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '&', ' y ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    '/', ' / ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'apt.', 'apt. ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'apt', 'apt ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish,
                                                    'apartamento', 'apartamento ')
        stripped_spanish = tf.strings.regex_replace(stripped_spanish, '[^a-zA-Z0-9 -/]', '')

        output = tf.strings.regex_replace(
            stripped_spanish, '[%s]' % re.escape(r"""!"$&'()*+-.;<=>?@[]^_`{|}~"""), '')

        return output

    @staticmethod
    @tf.keras.utils.register_keras_serializable()
    def __custom_standardization_v2(input_string):
        # Transforma toda la cadena a minúsculas
        lower_str = input_string.lower()

        # Quitar ½ y 1/2 en textos
        spec_text = re.sub(r'½|1/2', ' ', lower_str)

        # Reemplaza los caracteres y vocales especiales por espacios
        char_spvow_off_str = re.sub('[^a-zA-Z0-9 \n\.]', ' ', spec_text)

        # Quita cualquier caracter que no sea número o letra por espacio
        clear_str = re.sub('[^0-9a-zA-Z]+', ' ', char_spvow_off_str)

        return clear_str

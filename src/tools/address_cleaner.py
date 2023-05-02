import tensorflow as tf
import re
import string
import tensorflow as tf


class AddressCleaner:

    def custom_standardization(self, input_string):
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
                                                    '/', 'entre ')
        output = tf.strings.regex_replace(
            stripped_spanish, '[%s]' % re.escape(string.punctuation), '')

        return output

    def custom_standardization_v2(self,texto):
        # Transforma toda la cadena a minúsculas
        texto = texto.lower()

        # Reemplaza los caracteres y vocales especiales por espacios
        texto = re.sub('[^a-zA-Z0-9 \n\.]', ' ', texto)

        # Quita cualquier caracter que no sea número o letra por espacio
        texto = re.sub('[^0-9a-zA-Z]+', ' ', texto)

        nuevo_texto = re.sub(r"1/2|½", " ", texto)
        return nuevo_texto


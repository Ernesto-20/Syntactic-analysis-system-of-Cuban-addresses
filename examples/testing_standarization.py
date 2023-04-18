import re
import string
import unicodedata
import tensorflow as tf

def custom_standardization_v2(str_sentence: string):

    # Convierte toda la cadena a minúsculas
    str_lower = str_sentence.lower()

    # Cambia todos los signos de puntuación por espacios
    str_sign_off = re.sub(r'[^\w\s]', ' ', str_lower)

    # Convierte las letras especiales y las vocales con acentos en letras normales
    str_esp_ch_off = unicodedata.normalize('NFKD', str_sign_off).encode('ASCII', 'ignore').decode('utf-8')

    # Revisa cada palabra de la cadena
    # para ver si quedan signos de puntuación o caracteres especiales y los sustituye por espacios
    words = str_esp_ch_off.split()
    words = [re.sub(r'[^\w\s]', ' ', word) for word in words]
    str_clear = ' '.join(words)

    return str_clear


def custom_standardization( input_string):
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


sentence = "Edificio 15A @pto  7  %  11 C  y  11 D  Bahia, Habana del Este,LA HABANA DEL ESTE,La Habana"

print("Funcion: custom_standardization ")
print("Resultado:"+" "+custom_standardization(sentence))
print()
print()
print()
print()
print("Funcion: custom_standardization_v2 ")
print("Resultado:"+" "+custom_standardization_v2(sentence))

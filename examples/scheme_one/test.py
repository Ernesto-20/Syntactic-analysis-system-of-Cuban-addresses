import tensorflow as tf
from tensorflow.python.ops.ragged.ragged_string_ops import string_bytes_split
from src.parser.tools.address_cleaner import AddressCleaner

cleaner_method = AddressCleaner.cleaner_method(method='custom_standardization')

print('Init')
neural_parser = model = tf.keras.models.load_model('../../assets/trained_models/model_type_two/EXP6_C5_D100K/model', custom_objects={cleaner_method.__name__: cleaner_method,
                                                                                 'string_bytes_split': string_bytes_split})
print('Finish')
import dill
import tensorflow as tf
from tensorflow.python.ops.ragged.ragged_string_ops import string_bytes_split

from parser.tools.address_cleaner import AddressCleaner

file_path = '../../assets/trained_models/model_type_two/EXP6_C5_D100K'

cleaner_method = AddressCleaner.cleaner_method('custom_standardization_v2')



print(' cargue el cleaner')

model = tf.keras.models.load_model(file_path + '/model', custom_objects={cleaner_method.__name__: cleaner_method,
                                                                         'string_bytes_split': string_bytes_split})


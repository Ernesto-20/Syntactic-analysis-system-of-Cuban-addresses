from src.address_parser.address_parser import AddressParser
from src.data_preprocessing.address_cleaner import AddressCleaner
from src.neural_networks.deep_parser_model import DeepParserModel
from src.tools.data_set_manage import DataSetManage
from src.tools.decoder import Decoder
from src.tools.neural_parser_manage import NeuralParserManage
import tensorflow as tf


def load_data_set_saved(data_set_directory):
    """Load a saved data set """
    return DataSetManage.load(data_set_directory)


# load dataset saved
def train(data_set_directory, save_directory, name_model='colab_training'):
    resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu='')
    tf.config.experimental_connect_to_cluster(resolver)
    # This is the TPU initialization code that has to be at the beginning.
    tf.tpu.experimental.initialize_tpu_system(resolver)
    print("All devices: ", tf.config.list_logical_devices('TPU'))

    strategy = tf.distribute.TPUStrategy(resolver)

    data_set = load_data_set_saved(data_set_directory)

    # create model
    with strategy.scope():
        model = DeepParserModel(data_set, AddressCleaner.cleaner_method('custom_standardization'))

    # train
    model.train(batch_size=800, epochs=45)
    # address_parser = AddressParser(model, Decoder(data_set.get_id_to_category(),
    #                                               AddressCleaner.cleaner_method('custom_standardization')))

    # save
    NeuralParserManage.save_neural_parser(model, route=save_directory, name=name_model)
    print('Finish')

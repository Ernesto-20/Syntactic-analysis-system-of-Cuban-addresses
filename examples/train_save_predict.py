import pandas as pd

from src.address_parser.address_parser import AddressParser
from src.data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.noise_generator import NoiseGenerator
from src.neural_networks.deep_parser_model import DeepParserModel
from src.data_preprocessing.address_cleaner import AddressCleaner
from src.tools.data_set_manage import DataSetManage
from src.tools.decoder import Decoder
from src.tools.neural_parser_manage import NeuralParserManage


def load_data_set_saved():
    """Load a saved data set """
    return DataSetManage.load('../assets/default_data_set/model_type_one/DS_Habana_25000_PC_v1')


def create_new_data_set():
    """Create a new data set with adding noise"""
    # load corpus
    data = pd.read_excel('../assets/default_corpus/model_type_one/corpus_short.xlsx')

    # data realism convert
    generator = NoiseGenerator()
    data_with_noise = generator.generate_noise(data)

    # create object DataSet with data generated
    return DataSetAdapter.adapt(data_with_noise, training_percentage=0.8, testing_percentage=0.15,
                                validation_percentage=0.05)


print('Init')

# load dataset saved
data_set = load_data_set_saved()

# create model
model = DeepParserModel(data_set, AddressCleaner.cleaner_method('custom_standardization'))

# train
model.train(batch_size=480, epochs=40)
print(data_set.get_id_to_category())
print(data_set.get_n_tag())
address_parser = AddressParser(model, Decoder(data_set.get_id_to_category(),
                                              AddressCleaner.cleaner_method('custom_standardization')))

# save
NeuralParserManage.save_neural_parser(model, route='../assets/trained_models/model_type_one', name='pc_trained_v2')
print('Finish')

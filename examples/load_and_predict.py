import pandas as pd

from src.address_parser import AddressParser
from src.data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.noise_generator import NoiseGenerator
from src.neural_networks.deep_parser_model import DeepParserModel
from src.tools.address_cleaner import AddressCleaner
from src.tools.decoder import Decoder
from src.tools.neural_parser_manage import NeuralParserManage

print('Init')
neural_parser = NeuralParserManage.load_neural_parser(route='../assets/trained_models/model_type_one', name='test_model')
address_parser = AddressParser(neural_parser, Decoder(neural_parser.get_data().get_id_to_category(), neural_parser.get_address_cleaner().custom_standardization))
print('Finish')

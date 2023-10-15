import pandas as pd

from data_preprocessing.address_cleaner import AddressCleaner
from data_realism_converter.data_set_adapter import DataSetAdapter
from neural_networks.deep_parser_model import DeepParserModel
from neural_networks.lstm_cnn_model import LstmCnnModel
from src.data_realism_converter.scheme_two_noise_generator import SchemeTwoNoiseGenerator
from src.tools.data_set_manage import DataSetManage


print('Loading Datasets')
eq1_data = DataSetManage.load( '../assets/default_data_set/model_type_three/EQ_S3_1000')

print('Creating Neural Model')

model = LstmCnnModel(eq1_data, AddressCleaner.cleaner_method('custom_standardization'),config=None,model=None)


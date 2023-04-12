from src.data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.noise_generator import NoiseGenerator
from src.data_realism_converter.preprocessing_model_type_one import PDModelTypeOne
from src.neural_networks.deep_parser_model import DeepParserModel
import pandas as pd

from src.tools.data_set_manage import DataSetManage

print('Init')
data = pd.read_excel('assets/default_corpus/model_type_one/corpus_1.xlsx')

noise_generator = NoiseGenerator()
data_with_noise = noise_generator.generate_noise(data, address_amount=100)
adapt = DataSetAdapter()
data_set = adapt.adapt_data_set(data_with_noise)

# Example: save data_set
manage_ds = DataSetManage()
manage_ds.save(data_set, route_and_name='assets/default_data_set/funciono')
print('DataSet is saved')

# Example: load data_Set
# manage_ds = ManageDataSet()
# data_set = manage_ds.load(route_and_name='test_dataset')
# print('DataSet is loaded')


# parser = DeepParserModel()
# parser.create_model(data_with_noise)
# parser.fit_model(data_with_noise, batch_size=500, epochs=40)
print('finish')

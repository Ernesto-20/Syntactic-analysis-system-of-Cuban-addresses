import pandas as pd

from src.address_parser import AddressParser
from src.data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.noise_generator import NoiseGenerator
from src.neural_networks.deep_parser_model import DeepParserModel
from src.data_preprocessing.address_cleaner import AddressCleaner
from src.tools.decoder import Decoder
from src.tools.neural_parser_manage import NeuralParserManage

print('Init')
# load corpus
data = pd.read_excel('../assets/default_corpus/model_type_one/corpus_short.xlsx')

# data realism convert
generator = NoiseGenerator()
data_with_noise = generator.generate_noise(data)

# create object DataSet with data generated
data_set = DataSetAdapter.adapt(data_with_noise, training_percentage=0.7, testing_percentage=0.18, validation_percentage=0.12)

# create model
model = DeepParserModel(data_set, AddressCleaner.cleaner_method('custom_standardization'))

# train
model.train(batch_size=1000, epochs=1)
address_parser = AddressParser(model, Decoder(data_set.get_id_to_category(), AddressCleaner.cleaner_method('custom_standardization')))

# Predict
# result_list = address_parser.process_address(['calle parque entre av. carolina, san miguel del padron',
#                                          'vista hermosa, San miguel del padro, e/ ave. carolina y cale garido.',
#                                          'vista hermosa, San miguel del padro, e/ ave. carolina y cale garido reparto vista hermosa'])

# print('\tRESULTS OF ADDRESS PARSER\n')
# for result in result_list:
#     print(result)

# save
NeuralParserManage.save_neural_parser(model, route='../assets/trained_models/model_type_one',
                                      name='default_model')
print('Finish')

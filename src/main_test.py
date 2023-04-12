import pandas as pd

from src.address_parser import AddressParser
from src.data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.noise_generator import NoiseGenerator
from src.neural_networks.deep_parser_model import DeepParserModel
from src.tools.address_cleaner import AddressCleaner
from src.tools.decoder import Decoder
from src.tools.neural_parser_manage import NeuralParserManage

print('Init')
data = pd.read_excel('../assets/default_corpus/model_type_one/corpus_1.xlsx')

generator = NoiseGenerator()
data_with_noise = generator.generate_noise(data, address_amount=10)

# Especificar en la clase adapter los parametros de conjunto de datos para el entrenamiento, prueba y validación
adapt = DataSetAdapter()
data_set = adapt.adapt_data_set(data_with_noise)

address_cleaner = AddressCleaner()
model = DeepParserModel(data_set, address_cleaner)
# model.train(batch_size=500, epochs=1)
address_parser = AddressParser(model, Decoder(data_set.get_id_to_category(), address_cleaner.custom_standardization))


# result_list = address_parser.process_address(['calle parque entre av. carolina, san miguel del padron',
#                                          'vista hermosa, San miguel del padro, e/ ave. carolina y cale garido.',
#                                          'vista hermosa, San miguel del padro, e/ ave. carolina y cale garido reparto vista hermosa'])

# print('\tRESULTS OF ADDRESS PARSER\n')
# for result in result_list:
#     print(result)

NeuralParserManage.save_neural_parser(model, route='../assets/trained_models/model_type_one', name='test_model')

print('Finish')

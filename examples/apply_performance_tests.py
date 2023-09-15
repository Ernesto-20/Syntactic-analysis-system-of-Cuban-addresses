import pandas as pd

from src.data_preprocessing.address_cleaner import AddressCleaner
from src.data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.scheme_one_noise_generator import SchemeOneNoiseGenerator
from src.neural_networks.deep_parser_model import DeepParserModel


def create_new_data_set():
    # load corpus
    data = pd.read_excel('../assets/default_corpus/model_type_one/corpus_short.xlsx')

    # data realism convert
    generator = SchemeOneNoiseGenerator()
    data_with_noise = generator.generate_noise(data,address_amount=5000)

    # create object DataSet with data generated
    return DataSetAdapter.adapt(data_with_noise, training_percentage=0.7, testing_percentage=0.18,
                                validation_percentage=0.12)


print('Init')
# load dataset saved
data_set = create_new_data_set()
# create a new data set
# data_set = create_new_data_set()

# create model
model = DeepParserModel(data_set, AddressCleaner.cleaner_method('custom_standardization'))

# train
model.train_and_log(100,500,"pruebas_rend_I1")


# Predict
# result_list = address_parser.process_address(['calle parque entre av. carolina, san miguel del padron',
#                                          'vista hermosa, San miguel del padro, e/ ave. carolina y cale garido.',
#                                          'vista hermosa, San miguel del padro, e/ ave. carolina y cale garido reparto vista hermosa'])

# print('\tRESULTS OF ADDRESS PARSER\n')
# for result in result_list:
#     print(result)

# save

print('Finish')

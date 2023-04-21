import pandas as pd

from src.address_parser.address_parser import AddressParser
from src.data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.noise_generator import NoiseGenerator
from src.neural_networks.deep_parser_model import DeepParserModel
from src.data_preprocessing.address_cleaner import AddressCleaner
from src.neural_networks.lstm_cnn_model import LstmCnnModel
from src.tools.data_set_manage import DataSetManage
from src.tools.decoder import Decoder
from src.tools.neural_parser_manage import NeuralParserManage


def load_data_set_saved():
    return DataSetManage.load('../assets/default_data_set/model_type_one/DefaultDataSet')


def create_new_data_set():
    # load corpus
    data = pd.read_excel('../assets/default_corpus/model_type_one/corpus_short.xlsx')

    # data realism convert
    generator = NoiseGenerator()
    data_with_noise = generator.generate_noise(data)

    # create object DataSet with data generated
    return DataSetAdapter.adapt(data_with_noise, training_percentage=0.7, testing_percentage=0.18,
                                validation_percentage=0.12)


print('Init')
# load dataset saved
data_set = load_data_set_saved()
# create a new data set
# data_set = create_new_data_set()

# create model
model = LstmCnnModel(data_set, AddressCleaner.cleaner_method('custom_standardization_v2'))

# train
model.train(batch_size=1000, epochs=1)
address_parser = AddressParser(model, Decoder(data_set.get_id_to_category(),
                                              AddressCleaner.cleaner_method('custom_standardization')))

history =

plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()


print('Finish')
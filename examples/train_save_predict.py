import pandas as pd

from noise_generator.tools.data_set_adapter import DataSetAdapter
from src.noise_generator.scheme_one_noise_generator import SchemeOneNoiseGenerator
# from src.neural_networks.deep_parser_model import DeepParserModel
from parser.neural_networks.deep_parser_model import DeepParserModel
from parser.tools.address_cleaner import AddressCleaner
from noise_generator.tools.data_set_manage import DataSetManage


def load_data_set_saved():
    """Load a saved data set """
    return DataSetManage.load('../assets/default_data_set/model_type_one/DS_Habana_5000_PC_v2')


def create_new_data_set():
    """Create a new data set with adding noise"""
    # load corpus
    data = pd.read_excel('../assets/default_corpus/model_type_one/corpus_short.xlsx')

    # data realism convert
    generator = SchemeOneNoiseGenerator()
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
history = model.train(batch_size=560, epochs=10)
# print(data_set.get_id_to_category())
# print(data_set.get_n_tag())
# parser = AddressParser(model, Decoder(data_set.get_id_to_category(),
#                                               AddressCleaner.cleaner_method('custom_standardization')))
# parser.process_address(['Hola compadre'])
#
# # save
# NeuralParserManage.save_neural_parser(model, route='../assets/trained_models/model_type_one', name='pc_trained_v1')
# import matplotlib.pyplot as plt
#
# print(history.history.keys())
# acc = history.history['categorical_accuracy']
# val_acc = history.history['val_categorical_accuracy']
# loss = history.history['loss']
# val_loss = history.history['val_loss']
#
# epochs = 1
# plt.plot(epochs, acc, 'bo', label='Training acc')
# plt.plot(epochs, val_acc, 'b', label='Validation acc')
# plt.title('Training and validation accuracy')
# plt.legend()
# plt.figure()
# plt.plot(epochs, loss, 'bo', label='Training loss')
# plt.plot(epochs, val_loss, 'b', label='Validation loss')
# plt.title('Training and validation loss')
# plt.legend()
# plt.show()

print('Finish')

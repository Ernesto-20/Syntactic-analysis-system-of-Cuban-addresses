from src.preprocessing_data.preprocessing import PreprocessingData
from src.preprocessing_data.preprocessing_model_type_one import PDModelTypeOne
from src.neural_networks.neural_model import NeuralModel
import pandas as pd
from src.utils.manageDataSet import ManageDataSet

print('Init')
# Working data
data = pd.read_excel('assets/default_corpus/model_type_one/corpus_1.xlsx')

preprocessing = PDModelTypeOne()

data_with_noise = preprocessing.generate_noise(data)
# del data

data_set = preprocessing.create_DataSet_Word(data_with_noise)
# del data_with_noise


# manage_ds = ManageDataSet()
# manage_ds.save(data_set, route_and_name='test_dataset')
# print('DataSet is saved')


# load data_Set, create and train model
# manage_ds = ManageDataSet()
# data_set = manage_ds.load(route_and_name='test_dataset')
# print('DataSet is loaded')


parser = NeuralModel()
parser.create_model(data_set)
parser.fit_model(data_set, batch_size=500, epochs=100)
print('finish')

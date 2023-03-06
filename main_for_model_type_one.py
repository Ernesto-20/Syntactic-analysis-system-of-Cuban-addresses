from src.preprocessing_data.preprocessing import PreprocessingData
from src.preprocessing_data.preprocessing_model_type_one import PDModelTypeOne
from src.neural_networks.neural_model import NeuralModel
import pandas as pd
import sys
import pickle
from pandas import ExcelWriter

data = pd.read_excel('assets/default_corpus/model_type_one/corpus.xlsx')

preprocessing = PDModelTypeOne()

data_with_noise = preprocessing.generate_noise(data)
del data

data_set = preprocessing.create_DataSet_Word(data_with_noise)
del data_with_noise

parser = NeuralModel()
parser.create_model(data_set, 'Un modelo de prueba')
# parser.fit_model(batch_size=800, epochs=100)






# # print('Creando Data Set.')
# print('\tstep 0')
# data = pd.read_excel('assets/default_corpus/model_type_one/corpus.xlsx')
#
# print('\tstep 1')
# preprocessing = PDModelTypeOne()
#
# print('\tstep 2')
# data_with_noise = preprocessing.generate_noise(data)
# # print('data_with_noise v1', sys.getsizeof(data_with_noise))
# #
# write = ExcelWriter('DataSet-Prueba.xlsx')
# data_with_noise.to_excel(write, 'DataSet', index = False)
# write.save()
#
# data_with_noise.to_csv('DataSet-Prueba-CSV.csv', index = False)
# write.save()
# #
# # data_set = preprocessing.create_DataSet_Word(data_with_noise)
# # with open("data_set_saved.pickle", "wb") as file:
# #     pickle.dump(data_set, file)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # V2
# data_with_noise_v2 = pd.read_excel('DataSet-Prueba.xlsx')
# data_with_noise_v3 = pd.read_csv('DataSet-Prueba-CSV.csv')
#
# print('DS 1', sys.getsizeof(data_with_noise))
# print('DS 2', sys.getsizeof(data_with_noise_v2))
# print('DS 3', sys.getsizeof(data_with_noise_v3))
#
# if data_with_noise.equals(data_with_noise_v2):
#     print('Los DF son identicos')
# else:
#     print('Los DF no son iguales')
#
# print('$$$$$$$$$$$$$$$$$')
#
# write = ExcelWriter('DataSet-Prueba-REGRABADO.xlsx')
# data_with_noise_v2.to_excel(write, 'DataSet', index = False)
# write.save()
#
# data_with_noise_v4 = pd.read_excel('DataSet-Prueba.xlsx')
# print('DS 4', sys.getsizeof(data_with_noise_v4))
#
# if data_with_noise_v2.equals(data_with_noise_v4):
#     print('Los DF son identicos')
# else:
#     print('Los DF no son iguales')

# data_set = preprocessing.create_DataSet_Word(data_with_noise_v2)
# with open("data_set_saved_v2.pickle", "wb") as file:
#     pickle.dump(data_set, file)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # V3
# data = pd.read_excel('assets/default_corpus/model_type_one/corpus.xlsx')
#
# print('\tstep 1')
# preprocessing = PDModelTypeOne()
#
# print('\tstep 2')
# data_with_noise = preprocessing.generate_noise(data)
# del data
#
# data_set = preprocessing.create_DataSet_Word(data_with_noise)
# with open("data_set_saved_v3.pickle", "wb") as file:
#     pickle.dump(data_set, file)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # V4
# data = pd.read_excel('assets/default_corpus/model_type_one/corpus.xlsx')
# preprocessing = PDModelTypeOne()
#
# data_with_noise = preprocessing.generate_noise(data)
# del data
#
# data_set = preprocessing.create_DataSet_Word(data_with_noise)
# del data_with_noise
#
# with open("data_set_saved_v4.pickle", "wb") as file:
#     pickle.dump(data_set, file)

# print('\tstep 3')


# print('\tstep 4')
# del data_with_noise
#
# print('\tstep 5')
# #
# print('Creando modelo y entrenando')
# print('\tstep 0')
#
# # data_set = None
# # with open("data_set_saved.pickle", "rb") as file:
# #      data_set = pickle.load(file)
# #
# print('\tstep 1')
# parser = Parser()
# print('\tstep 2')
# parser.set_DataSet(data_set)
# print('\tstep 3')
# parser.create_model('nuevo modelo')
# print('\tstep 4')
# parser.fit_model(batch_size=800, epochs=100)
# print('\tstep 5')
# #

print('finish')

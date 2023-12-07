import dill
import pandas as pd
from pandas._libs.lib import Literal

from noise_generator.tools.data_set_adapter import DataSetAdapter
from noise_generator.tools.data_set_manage import DataSetManage
from parser.neural_networks import neural_parser

print('MODEL 3 EXP5_C5_D100KR')
print('Init')
data = pd.read_csv('../../assets/default_corpus/model_type_three/EXP5DS_200000.xlsx')


# then its adapt that dataframe to dataset
data_set = DataSetAdapter().adapt(data, 0.79, 0.05, 0.15)

# save the dataset created
DataSetManage.save(data_set,'../../assets/default_corpus/model_type_three/EXP5DS_200000')

file_path = '../../assets/trained_models/model_type_three/EXP5_C5_D100KR'
dir_data_set = file_path + '/data_set'
DataSetManage.save(data_set, route_and_name=dir_data_set)



print('EXP6_C5_D100K')
print('Init')
data = pd.read_csv('../../assets/default_corpus/model_type_two/EXP6DS_100000.xlsx')


# then its adapt that dataframe to dataset
data_set = DataSetAdapter().adapt(data, 0.79, 0.05, 0.15)

# save the dataset created
DataSetManage.save(data_set,'../../assets/default_corpus/model_type_two/EXP6DS_100000')

file_path = '../../assets/trained_models/model_type_three/EXP6_C5_D100K'
dir_data_set = file_path + '/data_set'

DataSetManage.save(data_set, route_and_name=dir_data_set)
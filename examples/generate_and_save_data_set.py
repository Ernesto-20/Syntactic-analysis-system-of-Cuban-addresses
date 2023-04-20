import pandas as pd

from src.data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.noise_generator import NoiseGenerator
from src.tools.data_set_manage import DataSetManage

print('Init')
# load corpus
data = pd.read_excel('../assets/default_corpus/model_type_one/corpus_short.xlsx')

# data realism convert
generator = NoiseGenerator()
data_with_noise = generator.generate_noise(data)

data_set = DataSetAdapter().adapt(data_with_noise, 0.70, 0.10, 0.20)

DataSetManage.save(data_set, '../assets/default_data_set/model_type_one/DefaultDataSet')
print('End')

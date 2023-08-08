import pandas as pd

from src.data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.noise_generator import NoiseGenerator
from src.tools.data_set_manage import DataSetManage

print('Init')
# load corpus
data = pd.read_excel('../assets/default_corpus/model_type_one/corpus_short_only_havana.xlsx')

# data realism convert
generator = NoiseGenerator()
data_with_noise = generator.generate_noise(data, address_amount=100)
# data_with_noise.to_csv('Prueba 1-10mil.csv')
data_set = DataSetAdapter().adapt(data_with_noise, 0.80, 0.05, 0.15)
# print(data_set.get_id_to_category())
# print(data_set.get_x_train_sentence_values()[0])
# print(data_set.get_y_train_values()[0])

# Uncomment to see addresses with noise
# count = 0
# for address in data_set.get_x_test_sentence_values():
#     print(address)
#     count += 1
#     if count == 10:
#         break

DataSetManage.save(data_set, '../assets/default_data_set/model_type_one/DS_Habana_100_test')
print('End')



import pandas as pd

from src.data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.scheme_one_noise_generator import SchemeOneNoiseGenerator
from src.tools.data_set_manage import DataSetManage

print('Init')
# load corpus
data = pd.read_excel('../assets/default_corpus/model_type_one/corpus_long_only_havana.xlsx')

# data realism convert
generator = SchemeOneNoiseGenerator()
data_with_noise = generator.generate_noise(data, address_amount=100)
# data_with_noise.to_excel('test.xlsx')
data_set = DataSetAdapter().adapt(data_with_noise, 0.80, 0.05, 0.15)

# Uncomment to see addresses with noise
# count = 0
# for address in data_set.get_x_test_sentence_values():
#     print(address)
#     count += 1
#     if count == 10:
#         break

DataSetManage.save(data_set, '../assets/default_data_set/model_type_one/DS_Habana_5000_PC_v2')
print('End')



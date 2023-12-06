import pandas as pd

from src.noise_generator.tools.data_set_adapter import DataSetAdapter
from src.noise_generator.scheme_one_noise_generator import SchemeOneNoiseGenerator
from src.noise_generator.tools.data_set_manage import DataSetManage


print('Init')
# Load corpus
data = pd.read_excel('../../assets/default_corpus/model_type_one/corpus_190000.xlsx')

# Simulated noise generator
generator = SchemeOneNoiseGenerator()
data_with_noise = generator.generate_noise(data)
data_set = DataSetAdapter().adapt(data_with_noise, 0.80, 0.05, 0.15)

# Uncomment to see addresses with noise
count = 0
for address in data_set.get_x_test_values():
    print(address)
    count += 1
    if count == 5:
        break

DataSetManage.save(data_set, '../../assets/default_data_set/model_type_one/DataSet_190000')
print('End')



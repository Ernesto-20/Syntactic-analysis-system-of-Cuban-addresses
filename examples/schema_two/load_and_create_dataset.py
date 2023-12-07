import pandas as pd

from noise_generator.tools.data_set_adapter import DataSetAdapter
from noise_generator.tools.data_set_manage import DataSetManage
from src.noise_generator.scheme_two_noise_generator import SchemeTwoNoiseGenerator

print('Init')
# load corpus from excel in drive
data = pd.read_excel(
    '../../assets/default_corpus/model_type_two/corpus_type_two_havana.xlsx')
# Instance of our Generator Model two
generator = SchemeTwoNoiseGenerator()

# we generate an address amount with type
data_with_noise = generator.generate_noise(data, type='eq', address_amount=50)

# then its adapt that dataframe to dataset
data_set = DataSetAdapter().adapt(data_with_noise, 0.69, 0.10, 0.20)

# save the dataset created
DataSetManage.save(data_set, '../../assets/default_data_set/model_type_two/EQ_S2_1000')


print(data_with_noise)


# print('Loading Datasets')
# eq1_data = DataSetManage.load( '../assets/default_data_set/model_type_two/EQ_S2_1000')
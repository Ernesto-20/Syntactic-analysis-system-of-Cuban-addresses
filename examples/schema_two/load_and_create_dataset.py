import pandas as pd

from data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.scheme_two_noise_generator import SchemeTwoNoiseGenerator
from src.tools.data_set_manage import DataSetManage

print('Init')
# load corpus from excel in drive
data = pd.read_excel('../assets/default_corpus/model_type_two/corpus.xlsx')
# Instance of our Generator Model two
generator = SchemeTwoNoiseGenerator()
# we generate an address amount with type
data_with_noise = generator.generate_noise(data,type='eq', address_amount=1000)

# then its adapt that dataframe to dataset
data_set = DataSetAdapter().adapt(data_with_noise, 0.69, 0.10, 0.20)
# save the dataset created
DataSetManage.save(data_set, '../assets/default_data_set/model_type_two/EQ_S2_1000')

print(data_with_noise)

data_with_noise.to_excel('../assets/default_data_set/model_type_two/EQ_S2_1000.xlsx',index=False)

print('Loading Datasets')
eq1_data = DataSetManage.load( '../assets/default_data_set/model_type_two/EQ_S2_1000')
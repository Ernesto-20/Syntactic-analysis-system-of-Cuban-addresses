import pandas as pd
from noise_generator.tools.data_set_adapter import DataSetAdapter
from noise_generator.tools.data_set_manage import DataSetManage
from src.noise_generator.scheme_two_noise_generator import SchemeTwoNoiseGenerator

print('Init')
# load corpus from excel in drive
data = pd.read_excel(
    '../../assets/default_corpus/model_type_two/corpus_type_two_havana_w.xlsx')
# Instance of our Generator Model two
generator = SchemeTwoNoiseGenerator()

tp = 'eq'
address = 100

# we generate an address amount with type
data_with_noise = generator.generate_noise(data, type=tp, address_amount=address)

# then its adapt that dataframe to dataset
data_set = DataSetAdapter().adapt(data_with_noise, 0.69, 0.10, 0.20)

# save the dataset created
DataSetManage.save(data_set, f'../../assets/default_data_set/model_type_two/{tp}_S2_{address}')

data_with_noise.to_excel(f'../../assets/default_data_set/model_type_two/{tp}_S2_{address}.xlsx', index=False)

print('Loading Datasets')
eq1_data = DataSetManage.load(f'../../assets/default_data_set/model_type_two/{tp}_S2_{address}')

print('Finish')

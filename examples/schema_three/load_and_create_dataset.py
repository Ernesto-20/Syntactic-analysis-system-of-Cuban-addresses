import pandas as pd

from src.noise_generator.tools.data_set_adapter import DataSetAdapter
from src.noise_generator.scheme_three_noise_generator import NoiseGeneratorModelThree
from src.noise_generator.tools.data_set_manage import DataSetManage

print('Init')

# load corpus from excel in drive
data = pd.read_excel('../../assets/default_corpus/model_type_three/corpus_type_three.xlsx')

# Instance of our Generator Model three
generator = NoiseGeneratorModelThree()

tp = 'eq'
address = 100

# we generate an address amount with type
data_with_noise = generator.generate_noise(data, type=tp, address_amount=address)

# then its adapt that dataframe to dataset
data_set = DataSetAdapter().adapt(data_with_noise, 0.69, 0.10, 0.20)

# save the dataset created
DataSetManage.save(data_set, f'../../assets/default_data_set/model_type_three/{tp}_S3_{address}')

data_with_noise.to_excel(f'../../assets/default_data_set/model_type_three/{tp}_S3_{address}.xlsx', index=False)

print('Loading Datasets')
eq1_data = DataSetManage.load(f'../../assets/default_data_set/model_type_three/{tp}_S3_{address}')

print('Finish')

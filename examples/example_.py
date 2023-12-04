import pandas as pd

from data_realism_converter.address_noise_generator import AddressNoiseGenerator
from data_realism_converter.data_set_adapter import DataSetAdapter
from tools.data_set_manage import DataSetManage

print('Init')

# '../assets/default_corpus/model_type_two/corpus_type_two_havana_w.xlsx'

# load corpus from excel in drive
data = pd.read_excel('../assets/default_corpus/model_type_two/corpus_type_two_havana_w.xlsx')
# Instance of our Generator Model two
generator = AddressNoiseGenerator()

addresses = 100

# we generate an address amount with type
data_with_noise = generator.generate_noise(data,model='building',typea='eval',address_amount=addresses)

data_with_noise.to_excel(f'../examples/lista_eval_schema_building.xlsx',index=False)

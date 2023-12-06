import pandas as pd

from src.noise_generator.scheme_two_noise_generator import SchemeTwoNoiseGenerator
from tools.model_tester import import_address_list_two

print('Init')
# load corpus from excel in drive
data = pd.read_excel(
    'C:/Users/Frank/Documents/GitHub/Syntactic-analysis-system-of-Cuban-addresses/assets/default_corpus/model_type_two/corpus_type_two_havana_w.xlsx')
# Instance of our Generator Model two
generator = SchemeTwoNoiseGenerator()

addresses = 10

# we generate an address amount with type
real_addresses = generator.generate_noise(data, type='ea', address_amount=addresses)

print(real_addresses)

real_addresses.to_excel('list_eval_10.xlsx', index=False)
count = 0

addresses_list = import_address_list_two(real_addresses)
print(len(addresses_list))

for obj in addresses_list:
    print(obj)
    count += 1


#
#
model_data_high = NeuralParserManage.load_neural_parser(route='C:/Users/Frank/Documents/GitHub/Syntactic-analysis-system-of-Cuban-addresses/assets/trained_models/model_type_two',
                                                        name='EXP4_model_congf_high')

# parser = AddressParser(model_data_high, Decoder(model_data_high.data.get_id_to_category(),
#                                                         AddressCleaner.cleaner_method('custom_standardization')))
#
# result_list = parser.process_address_two(real_addresses['full_address'].to_list())
#
# print(result_list)
# print('\tRESULTS OF ADDRESS PARSER\n')
# count = 0
# for result in result_list:
#     print(result)
#     count += 1
#
#
#
# print(calculate_results_two(result_list, addresses_list))
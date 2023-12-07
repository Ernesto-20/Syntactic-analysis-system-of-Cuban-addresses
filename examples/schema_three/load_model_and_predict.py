from parser.tools.neural_parser_manage import NeuralParserManage
from src.parser.tools.address_cleaner import AddressCleaner
from src.noise_generator.tools.data_set_manage import DataSetManage
from utils.model_tester import import_address_list_two, import_address_list_three, calculate_results_two, \
    calculate_results_three
import pandas as pd
from parser.address_parser import AddressParser
from parser.tools.decoder import Decoder

# print('EXP6_C5_D100K')
# model_data_high = NeuralParserManage.load_neural_parser(route='../../assets/trained_models/model_type_two/',
#                                                                                        name='EXP6_C5_D100K')

print('MODEL 3 EXP5_C5_D100KR')
model_type_three = NeuralParserManage.load_neural_parser(route='../../assets/trained_models/model_type_three/',
                                                         name='EXP5_C5_D100KR')

main_decoder = Decoder(model_type_three.data.get_id_to_category(),
                       AddressCleaner.cleaner_method('custom_standardization_v2'))

main_parser = AddressParser(model_type_three, main_decoder)

lista = pd.read_excel('lista_eval_schema_distance.xlsx')

result_list = main_parser.process_address_three(lista['full_address'].to_list())


lista_real = import_address_list_three(lista)
print('\tRESULTS OF ADDRESS PARSER\n')
count = 0
for result in result_list:
    print(result)
    count += 1

print(calculate_results_three(result_list, lista_real))
from src.address_parser.address_parser import AddressParser
from src.tools.decoder import Decoder
from src.tools.neural_parser_manage import NeuralParserManage
from src.data_preprocessing.address_cleaner import AddressCleaner
from tests.tools.compare_results import accurracy
from tests.tools.address_list import ADDRESS_LIST
import pandas as pd

print('Init')
# neural_parser = NeuralParserManage.load_neural_parser(route='../assets/trained_models/model_type_one', name='model_colab')
neural_parser = NeuralParserManage.load_neural_parser(route='../assets/trained_models/model_type_one', name='default_model_instance_1C')
neural_parser.evaluate()

# address_parser = AddressParser(neural_parser, Decoder(neural_parser.get_data().get_id_to_category(), neural_parser.get_cleaner_method()))
address_parser = AddressParser(neural_parser, Decoder(neural_parser.get_data().get_id_to_category(), AddressCleaner.cleaner_method('custom_standardization')))

# Predict
evaluates = pd.read_excel('../assets/default_corpus/model_type_one/evaluate.xlsx')
result_list = address_parser.process_address_data_frame(evaluates)
#
print('\tRESULTS OF ADDRESS PARSER\n')
count = 0
for result in result_list:
    print(count+1, ' ', str(evaluates.iloc[count, 0]))
    print(result)
    count += 1

print('Acurracy: ', accurracy(result_list, ADDRESS_LIST))

# AddressParser.to_xlsx(result_list, name_file='NewResults')
#
print('Finish')
#

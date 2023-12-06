from src.parser.address_parser import AddressParser
from src.parser.tools.decoder import Decoder
from src.parser.tools.neural_parser_manage import NeuralParserManage
from src.parser.tools.address_cleaner import AddressCleaner
from src.utils.compare_results import calculate_results
from src.utils.address_list import ADDRESS_LIST_EVAL_1
import pandas as pd

print('Init')
neural_parser = NeuralParserManage.load_neural_parser(route='../../assets/trained_models/model_type_one', name='colab_trained_v28')
# neural_parser = NeuralParserManage.load_neural_parser(route='../../assets/trained_models/model_type_two', name='EXP6_C5_D100K')
# neural_parser = NeuralParserManage.load_neural_parser(route='../../assets/trained_models/model_type_three', name='EXP5_C5_D100KR')
# neural_parser.evaluate()

address_parser = AddressParser(neural_parser, Decoder(neural_parser.data.get_id_to_category(), AddressCleaner.cleaner_method('custom_standardization')))

# Predict
evaluates = pd.read_excel('../../assets/default_corpus/model_type_one/evaluate 1.xlsx')
result_list = address_parser.process_address_data_frame(evaluates)

print('\tRESULTS OF ADDRESS PARSER\n')
count = 0
for result in result_list:
    print(count+1, ' ', str(evaluates.iloc[count, 0]))
    print(result)
    count += 1

print(calculate_results(result_list, ADDRESS_LIST_EVAL_1))

# AddressParser.to_xlsx(result_list, name_file='NewResults')
print('Finish')

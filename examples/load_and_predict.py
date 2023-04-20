from src.address_parser import AddressParser
from src.tools.decoder import Decoder
from src.tools.neural_parser_manage import NeuralParserManage
from src.tools.export_to_xlsx import export_to_xlsx

print('Init')
neural_parser = NeuralParserManage.load_neural_parser(route='../assets/trained_models/model_type_one', name='test_model')
address_parser = AddressParser(neural_parser, Decoder(neural_parser.get_data().get_id_to_category(), neural_parser.get_cleaner_method()))

# Predict
result_list = address_parser.process_address(['calle parque entre av. carolina, san miguel del padron',
                                         'vista hermosa, San miguel del padro, e/ ave. carolina y cale garido.',
                                         'vista hermosa, San miguel del padro, e/ ave. carolina y cale garido reparto vista hermosa'])

print('\tRESULTS OF ADDRESS PARSER\n')
for result in result_list:
    print(result)

export_to_xlsx(result_list, 'breve_resultados')

print('Finish')


from src.address_parser.address_parser import AddressParser
from src.tools.decoder import Decoder
from src.tools.neural_parser_manage import NeuralParserManage
import pandas as pd

print('Init - Retrain')
neural_parser = NeuralParserManage.load_neural_parser(route='../assets/trained_models/model_type_one', name='default_model_instance_1C')
neural_parser.train(1000, 15)
print('Finish  - Retrain')

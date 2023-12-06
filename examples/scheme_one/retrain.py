from parser.tools.neural_parser_manage import NeuralParserManage

print('Init - Retrain')
neural_parser = NeuralParserManage.load_neural_parser(route='../../assets/trained_models/model_type_one', name='test_cpy_14')
neural_parser.train(1000, 15)
print('Finish  - Retrain')

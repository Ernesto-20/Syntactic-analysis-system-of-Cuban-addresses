from tensorflow.python.ops.ragged.ragged_string_ops import string_bytes_split
from src.neural_networks.deep_parser_model import DeepParserModel
from src.neural_networks.neural_parser import NeuralParser
from src.tools.data_set_manage import DataSetManage
import tensorflow as tf
import dill


class NeuralParserManage:

    @staticmethod
    def save_neural_parser(neural_parser: NeuralParser, route='assets/trained_models/model_type_one/',
                           name='model_pretrained'):
        if type(route) is not str:
            raise NotImplementedError('route variable could be string instance')
        if type(name) is not str:
            raise NotImplementedError('name_model variable could be string instance')
        # save model
        route = NeuralParserManage._reformat_and_validate_route(route)
        name = NeuralParserManage._reformat_and_validate_name_model(name)
        dir_model = route + '/' + name + '/model'
        dir_data_set = route + '/' + name + '/data_set'
        dir_cleaner_method = route + '/' + name + '/cleaner_method'
        dir_config = route + '/' + name + '/config'

        neural_parser.model.save(dir_model, save_format="tf")
        DataSetManage.save(neural_parser.data, route_and_name=dir_data_set)
        # Save cleaner method with dill
        dill.dump(neural_parser.cleaner_method, open(dir_cleaner_method, 'wb'))
        dill.dump(neural_parser.config, open(dir_config, 'wb'))

    @staticmethod
    def load_neural_parser(route='default', name='default') -> NeuralParser:
        file_path = route + '/' + name
        # load data set
        data = DataSetManage.load(file_path + '/data_set')

        # load address cleaner
        cleaner_method = dill.load(open(file_path + '/cleaner_method', 'rb'))

        config = dill.load(open(file_path + '/config', 'rb'))
        # load keras model
        model = tf.keras.models.load_model(file_path + '/model', custom_objects={cleaner_method.__name__: cleaner_method,
                                                                                 'string_bytes_split': string_bytes_split})
        return DeepParserModel(data, cleaner_method=cleaner_method, config=config, model=model)

    @staticmethod
    def _reformat_and_validate_route(route: str):
        if len(route) == 0:
            raise NotImplementedError('name_model variable cannot be an empty text')

        if route[len(route) - 1] == '/':
            route = route[:len(route) - 1]

        if len(route.split()) == 0:
            raise NotImplementedError('route variable cannot be an text with only withe space')

        return route

    @staticmethod
    def _reformat_and_validate_name_model(name_model: str):
        if len(name_model) == 0:
            raise NotImplementedError('name_model variable cannot be an empty text')
        if name_model[len(name_model) - 1] == '/':
            name_model = name_model[:len(name_model) - 1]
        if name_model[0] == '/':
            name_model = name_model[1:]

            # Repeating validation because the before steps has removed a character
        if len(name_model) == 0:
            raise NotImplementedError('name_model variable cannot be an empty text')
        if len(name_model.split()) == 0:
            raise NotImplementedError('name_model variable cannot be an text with only withe space')

        return name_model

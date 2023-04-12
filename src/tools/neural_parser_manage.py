from src.neural_networks.deep_parser_model import DeepParserModel
from src.neural_networks.neural_parser import NeuralParser
from src.tools.address_cleaner import AddressCleaner
from src.tools.data_set_manage import DataSetManage
from src.tools.address_data_set import DataSet
import pickle
import tensorflow as tf
import re
import string


class NeuralParserManage:

    @staticmethod
    def save_neural_parser(neural_parser: NeuralParser, route='assets/trained_models/model_type_one/',
                           name='model_pretrained'):
        if type(route) is not str:
            raise NotImplementedError('route variable could be string instance')
        if type(name) is not str:
            raise NotImplementedError('name_model variable could be string instance')
        # save model
        dir_model = ''
        route = NeuralParserManage.__reformat_and_validate_route(route)
        name = NeuralParserManage.__reformat_and_validate_name_model(name)
        dir_model = route + '/' + name + '/model'
        dir_data_set = route + '/' + name + '/data_set'
        dir_address_cleaner = route + '/' + name + '/address_cleaner'

        neural_parser.get_model().save(dir_model, save_format="tf")
        DataSetManage.save(neural_parser.get_data(), route_and_name=dir_data_set)
        # Save AddressCleaner Object
        with open(dir_address_cleaner + '.pickle', "wb") as file:
            pickle.dump(neural_parser.get_address_cleaner(), file)

    @staticmethod
    def load_neural_parser(route='default', name='default') -> NeuralParser:
        file_path = route+'/'+name
        # load data set
        data = DataSetManage.load(file_path+'/data_set')

        # load address cleaner
        address_cleaner = None
        with open(file_path + '/address_cleaner.pickle', "rb") as file:
            address_cleaner = pickle.load(file)

        # load keras model
        model = tf.keras.models.load_model(file_path+'/model', custom_objects={"custom_standardization": address_cleaner.custom_standardization})

        return DeepParserModel(data, address_cleaner, model=model)

    @staticmethod
    def __reformat_and_validate_route(route: str):
        if len(route) == 0:
            raise NotImplementedError('name_model variable cannot be an empty text')

        if route[len(route) - 1] == '/':
            route = route[:len(route) - 1]

        if len(route.split()) == 0:
            raise NotImplementedError('route variable cannot be an text with only withe space')

        return route

    @staticmethod
    def __reformat_and_validate_name_model(name_model: str):
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



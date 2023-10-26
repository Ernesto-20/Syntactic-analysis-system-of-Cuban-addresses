from src.neural_networks.neural_parser import NeuralParser
from src.structured_direction.classified_address_one import ClassifiedAddressOne
from src.tools.decoder import Decoder
import pandas as pd
from pandas import DataFrame


class AddressParser:

    def __init__(self, model: NeuralParser, decoder: Decoder):
        self.model = model
        self.decoder = decoder

    def process_address(self, address_list: list):
        probability_matrix = self.model.predict(address_list)

        return self.decoder.decode_to_scheme_one(probability_matrix, address_list)

    def process_address_two(self, address_list: list):
        probability_matrix = self.model.predict(address_list)

        return self.decoder.decode_to_scheme_two(probability_matrix, address_list)

    def process_address_three(self, address_list: list):
        probability_matrix = self.model.predict(address_list)

        return self.decoder.decode_to_scheme_three(probability_matrix, address_list)

    def process_address_data_frame(self, address: DataFrame):
        address_list = []
        for i in address.index:
            if len(str(address.iloc[i, 0])) != 0:
                address_list.append(str(address.iloc[i, 0]))
        probability_matrix = self.model.predict(address_list)

        return self.decoder.decode_to_scheme_one(probability_matrix, address_list)

    def process_address_two_data_frame(self, address: DataFrame):
        address_list = []
        for i in address.index:
            if len(str(address.iloc[i, 0])) != 0:
                address_list.append(str(address.iloc[i, 0]))
        probability_matrix = self.model.predict(address_list)

        return self.decoder.decode_to_scheme_two(probability_matrix, address_list)

    def process_address_three_data_frame(self, address: DataFrame):
        address_list = []
        for i in address.index:
            if len(str(address.iloc[i, 0])) != 0:
                address_list.append(str(address.iloc[i, 0]))
        probability_matrix = self.model.predict(address_list)

        return self.decoder.decode_to_scheme_three(probability_matrix, address_list)

    @staticmethod
    def to_xlsx(list_address: list, name_file='Results'):
        if len(list_address) == 0:
            raise NotImplementedError('The list should have at least one address')
        elif isinstance(list_address[0], ClassifiedAddressOne):
            AddressParser.__export_one(list_address, name_file=name_file, format='xlsx')
        # FRANK poner la otra condicion de que si es instancia de ClassifiedAddresTwoAndThree

    @staticmethod
    def to_csv(list_address: list, name_file='Results'):
        if len(list_address) == 0:
            raise NotImplementedError('The list should have at least one address')
        elif isinstance(list_address[0], ClassifiedAddressOne):
            AddressParser.__export_one(list_address, name_file=name_file, format='csv')
        # FRANK poner la otra condicion de que si es instancia de ClassifiedAddresTwoAndThree
    @staticmethod
    def _export_one(list_address: list, name_file='Results', format='xlsx'):
        principal_street_list = []
        first_side_street_list = []
        second_side_street_list = []
        locality_list = []
        municipality_list = []
        province_list = []
        buildings_list = []
        apartment_list = []
        reserve_words_list = []

        for address in list_address:
            principal_street_list.append(' '.join(address.principal_street))
            first_side_street_list.append(' '.join(address.first_side_street))
            second_side_street_list.append(' '.join(address.second_side_street))
            locality_list.append(' '.join(address.locality))
            municipality_list.append(' '.join(address.municipality))
            province_list.append(' '.join(address.province))
            buildings_list.append(' '.join(address.building))
            apartment_list.append(' '.join(address.apartment))
            reserve_words_list.append(' '.join(address.reserve_word))

        df = DataFrame({
            'Principal Street': principal_street_list,
            'First Side Street': first_side_street_list,
            'Second Side Street': second_side_street_list,
            'Building': buildings_list,
            'Apartment': apartment_list,
            'Locality': locality_list,
            'Municipality': municipality_list,
            'Province': province_list,
            'Reserved Word': reserve_words_list,
        })

        if format == 'xlsx':
            writer = pd.ExcelWriter(name_file + '.xlsx', engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name=name_file)
            writer.save()
        elif format == 'csv':
            df.to_csv(name_file)
        else:
            raise NotImplementedError('This export format is not implemented')





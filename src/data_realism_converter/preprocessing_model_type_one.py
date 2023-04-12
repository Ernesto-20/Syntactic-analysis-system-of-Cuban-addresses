import math

from pandas import DataFrame
import random as rm
import itertools as itt

from src.data_realism_converter.noise_generator import NoiseGenerator
from src.tools.lookup import *


class PDModelTypeOne:
    def generate_noise(self, data_set: DataFrame, address_amount= 15333):
        # 15333 direcciones limpias de caracteres extraños
        print('Generate some noise -- Type One')
        address_number = 0
        address_list = []
        words_list = []
        tag_list = []
        for i in data_set.index:
            # 1048576 total de filas que permite ExcelWrite a llenar en una sola hoja de excel.
            # if len(words_list) > 1048576 - 50:
            #     break
            if address_number == address_amount:
                break

            dictAddress = {}
            components = []

            street_1 = str(data_set.iloc[i, 0])
            street_2 = str(data_set.iloc[i, 1])
            street_3 = str(data_set.iloc[i, 2])
            locality = str(data_set.iloc[i, 3])
            municipality = str(data_set.iloc[i, 4])
            province = str(data_set.iloc[i, 5])

            # CREATING COMPONENT 1  --- [type_street], [street_1] ---

            # Adding street_type_1 and street_1
            is_corner_1 = True if rm.randint(0, 100) > 90 else False
            component_1_str = ''
            component_2_str = ''
            if is_corner_1:
                # Adding street_type_1 and street_1
                street_type_1 = self.__generate_prefix_randomly(RW_STREETS, components, 20)
                component_1_str = street_type_1 + ' ' + street_1

                components += [[item, 'street_1'] for item in street_1.split()]
                dictAddress[component_1_str] = components

                # conjunction prefix
                components += [['y', 'rw']]

                # Adding street_type_2 and street_2
                street_type_2 = self.__generate_prefix_randomly(RW_STREETS, components, 20)
                components += [[item, 'street_2'] for item in street_2.split()]

                # Se deberia agregar prefijo de esquina: [esq, esquina, etc.] (con poca probabilidad)
                component_1_str += ' y' + street_type_2 + street_2
                dictAddress[component_1_str] = components
            else:
                # Adding street_type_1 and street_1
                street_type_1 = self.__generate_prefix_randomly(RW_STREETS, components, 20)
                component_1_str = street_type_1 + ' ' + street_1

                components += [[item, 'street_1'] for item in street_1.split()]
                dictAddress[component_1_str] = components

                # CREATING COMPONENT 2  --- [div_street], [type_street], [street_2], [and], [type_street], [street_3] ---
                components = []
                    # Adding separator type as 'entre' or 'e/' or others.
                div_street = RW_DIV_STREET[rm.randint(0, 4)]
                components = [[item, 'rw'] for item in div_street.split()]

                # Adding street_type_2 and street_2
                street_type_2 = self.__generate_prefix_randomly(RW_STREETS, components, 25)
                components += [[item, 'street_2'] for item in street_2.split()]

                # Adding separator type 'y'.
                components += [['y', 'rw']]

                # Adding street_type_3 and street_3
                street_type_3 = self.__generate_prefix_randomly(RW_STREETS, components, 25)
                components += [[item, 'street_3'] for item in street_3.split()]

                component_2_str = div_street + street_type_2 + ' ' + street_2 + ' y' + street_type_3 + ' ' + street_3
                dictAddress[component_2_str] = components

            # CREATING COMPONENT 3  --- [type_num_house],[house_number] ---

            random_num = rm.randint(100, 9000)
            components = []
            component_3_str = ''
            if random_num < 6000:
                house_number = str(random_num)

                # Adding type_num_house and house_number
                type_num_house = self.__generate_prefix_randomly(RW_HOUSE_NUMBER, components, 20)
                components = [[item, 'rw'] for item in type_num_house.split()]  # reserved word
                components += [[item, 'house_num'] for item in house_number.split()]

                component_3_str = type_num_house + ' ' + house_number
                # Setting apartment number
                apartment_num = rm.randint(100, 201)
                if apartment_num > 175:
                    type_num_apartment = self.__generate_prefix_randomly(RW_APARTMENT, components, 10)
                    components += [[item, 'rw'] for item in str(apartment_num).split()]
                    component_3_str += ' ' + type_num_apartment + ' ' + str(apartment_num)

                    # Setting floor type
                    random = rm.randint(100, 201)
                    if random > 175:
                        type_floor = self.__generate_prefix_randomly(RW_NUMBER_FLOOR, components, 15)
                        component_3_str += ' ' + type_floor

                dictAddress[component_3_str] = components

            # CREATING COMPONENT 4  --- [locality] ---
            components = []
            component_4_str = ''
            if locality != '':
                component_4_str = self.__generate_prefix_randomly(RW_LOCALITY, components, 14)
            components += [[item, 'locality'] for item in locality.split()]
            component_4_str += locality
            dictAddress[component_4_str] = components

            # CREATING COMPONENT 5  --- [municipality] ---
            components = [[item, 'municipality'] for item in municipality.split()]
            component_5_str = municipality
            dictAddress[component_5_str] = components

            # CREATING COMPONENT 6  --- [province] ---
            components = [[item, 'province'] for item in province.split()]
            component_6_str = province
            dictAddress[component_6_str] = components

            # *********** non-standardization **********
            datasAddress = [component_1_str]
            if component_2_str != '':
                datasAddress += [component_2_str]
            if component_3_str != '':
                datasAddress += [component_3_str]
            datasAddress += [component_4_str, component_5_str, component_6_str]
            permutations = list(itt.permutations(datasAddress))

            amount_permutation = math.factorial(len(datasAddress)) - 1
            datasAddress = permutations[rm.randint(0, amount_permutation)]

            reorder_componentes = []
            for item in datasAddress:
                reorder_componentes += dictAddress[item]
            # *********** non-standardization **********

            address_number += 1
            self.__add_address(reorder_componentes, address_number, address_list, words_list, tag_list)

        return self.__generate_data_frame(address_list, words_list, tag_list)

    def __generate_data_frame(self, address_list, words_list, tag_list):
        # columns_sentences = pd.DataFrame({'Sentence #': address_list})
        # column_word = pd.DataFrame({'Word': words_list})
        # column_tag = pd.DataFrame({'Tag': tag_list})
        #
        # return pd.concat([columns_sentences, column_word, column_tag], axis=1)
        return DataFrame({
            'Sentence #': address_list,
            'Word': words_list,
            'Tag': tag_list
        })

    def __generate_prefix_randomly(self, types, current_components, top):
        """ Randomly generates a street type and assigns it to the list.

            param rw_list: List of components of an address

            param top: integer indicating a probability margin for not choosing any type.
            As top increases, the probability of not choosing a street type increases.

            :return: The list with the new street type incorporated if it was the case, otherwise, it is returned unchanged.
            In addition, the type of street is returned if it has been generated.
        """
        num_random = rm.randint(0, top)
        amount_types = len(types)
        prefix = ''

        # Creating and adding the street type
        prefix = types[amount_types - 1 if num_random >= amount_types - 1 else num_random]
        current_components += [[item, 'rw'] for item in prefix.split()]

        prefix = ' ' + prefix

        return prefix

    def __add_address(self, result_list, address_number, address_list, words_list, tag_list):
        address_list.append('Sentence ' + str(address_number))

        count = 0
        for labels in result_list:
            if labels[0] != 'nan':
                tag_list.append(labels[1])
                words_list.append(str(labels[0]).lower())

                if 0 != count and len(words_list) == len(address_list) + 1:
                    address_list.append(None)
            count += 1
        
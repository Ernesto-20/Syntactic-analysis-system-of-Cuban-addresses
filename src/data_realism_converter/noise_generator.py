import math
import random

from pandas import DataFrame
import random as rm
import itertools as itt

from src.data_realism_converter.generator import Generator
from src.tools.lookup import STREET_NAME_PREFIX, STREET_NAME_SUFFIX, LOCALITY_PREFIX, MUNICIPALITY_PREFIX, \
    PROVINCE_PREFIX, BETWEEN_PREFIX, \
    BUILDING_PREFIX, APARTMENT_PREFIX, IMPLICIT_APARTMENT, APARTMENT_SPECIFICATION, CORNER_CONNECTOR_PREFIX, STREET_SUFFIX_POSSIBILITIES, PROPERTY_PREFIX


class NoiseGenerator(Generator):
    '''
        Caracterizacion del modelo 1: (Componentes para permutar)

        De acuerdo a la localidad, municipio, provincia se tiene los siguientes componentes: (Componentes Basicos)
            [ prefijo + locaclidad]     [ prefijo + municipio]      [ prefijo + provincia]
        De a cuerdo a las calles, esquinas, entrecalles, edificacion ( casa o edificio y numero de apartamento o piso) se pueden dividir en:

            Tipo 1: Calle y entrecalles
                [ prefijo + calle principal]    [ prefijo + calle secundaria + conjuncion + prefijo + calle secundaria] +-  [ prefijo + edificio + apat.]
            Tipo 2: esquinas
                2.1
                    [ esq + prefijo calle + conjuncion + prefijo + calle]
                2.2
                    [ prefijo + calle + esq + prefijo + calle]
            Tipo 2 Con variaciones: informacion de edificios, casas, piso, apartamento, etc.
                2.1.1
                    [ esq + prefijo calle + EDF + conjuncion + prefijo + calle]
                    [ esq + prefijo calle + conjuncion + prefijo + calle + EDF]
                2.2.1
                    [ prefijo + calle + EDF + esq + prefijo + calle]
                    [ prefijo + calle + esq + prefijo + calle + EDF]
            Tipo 3: Solo calle principal
                    [ prefijo + calle principal] [ prefijo + edificio + apat.]
    '''

    def generate_noise(self, data_set: DataFrame, address_amount=None):
        rm.seed(155)
        # print('Generate Noise -- Type I')
        address_number = 0
        address_list = []
        words_list = []
        tags_list = []

        for i in data_set.index:
            # print('address number: ', address_number+1)
            if address_amount is not None and address_number == address_amount:
                break
            components = []

            principal_street = str(data_set.iloc[i, 0])
            first_side_street = str(data_set.iloc[i, 1])
            second_side_street = str(data_set.iloc[i, 2])
            locality = str(data_set.iloc[i, 3])
            municipality = str(data_set.iloc[i, 4])
            province = str(data_set.iloc[i, 5])

            # Determinar si es tipo 1 o 2:
            if not self.__is_empty(first_side_street) and not self.__is_empty(second_side_street):
                # Is type one
                principal_street_added_word = self.__generate_prefix_or_suffix_randomly(principal_street,
                                                                                        entity_type='principal_street')
                first_side_street_added_word = self.__generate_prefix_or_suffix_randomly(first_side_street,
                                                                                         entity_type='first_side_street')
                second_side_street_added_word = self.__generate_prefix_or_suffix_randomly(second_side_street,
                                                                                          entity_type='second_side_street')

                between_prefix = super().generate_prefix_randomly(BETWEEN_PREFIX, 100)
                first_side_street_added_word = [[item, 'first_side_street'] for item in first_side_street.split()] if \
                    between_prefix[0][0] in ['e/c', 'e\c', 'entre calles'] else first_side_street_added_word

                conjunction_prefix = [
                    ['e' if (second_side_street_added_word[0][0][0].lower() == 'i') else self.__generate_conjunction(), 'rw']]

                # create component
                components.append(principal_street_added_word)
                flag = False
                if rm.randint(1, 100) < 15:
                    flag = True
                    components.append(
                        between_prefix + first_side_street_added_word + conjunction_prefix + second_side_street_added_word)

                if rm.randint(1, 100) <= 50:
                    # Contain building
                    building_component, apartment_component = self.generate_building_and_apartment()
                    components.append(building_component)
                    components.append(apartment_component)
                if not flag:
                    components.append(
                        between_prefix + first_side_street_added_word + conjunction_prefix + second_side_street_added_word)

            elif not self.__is_empty(first_side_street) or not self.__is_empty(second_side_street):
                #   Is type 2
                side_street = first_side_street if self.__is_empty(second_side_street) else second_side_street

                principal_street_added_word = self.__generate_prefix_or_suffix_randomly(principal_street,
                                                                                        entity_type='principal_street')
                side_street_added_word = self.__generate_prefix_or_suffix_randomly(first_side_street,
                                                                                   entity_type='first_side_street')

                if rm.randint(1, 100) <= 50:
                    # Is type 2.1
                    corner_prefix = super().generate_prefix_randomly(CORNER_CONNECTOR_PREFIX, 100)
                    conjunction_prefix = [
                        ['e' if side_street_added_word[0][0][0] == 'i' else self.__generate_conjunction(), 'rw']]

                    if rm.randint(1, 100) <= 50:
                        # Contain Building
                        building_component, apartment_component = self.generate_building_and_apartment()
                        if rm.randint(1, 100) <= 50:
                            # Is type 2.1.1 left building
                            components.append(
                                corner_prefix + principal_street_added_word +
                                building_component + apartment_component +
                                conjunction_prefix + side_street_added_word
                            )
                        else:
                            # Is type 2.1.1 right building
                            components.append(
                                corner_prefix + principal_street_added_word +
                                conjunction_prefix + side_street_added_word +
                                building_component + apartment_component
                            )
                    else:
                        # Not contain building
                        components.append(
                            corner_prefix + principal_street_added_word + conjunction_prefix + side_street_added_word)
                else:
                    # Is type 2.2
                    corner_prefix = super().generate_prefix_randomly(CORNER_CONNECTOR_PREFIX, 100)

                    if rm.randint(1, 100) <= 50:
                        # Contain Building
                        building_component, apartment_component = self.generate_building_and_apartment()
                        if rm.randint(1, 100) <= 50:
                            # Is type 2.1.1 left building
                            components.append(
                                principal_street_added_word +
                                building_component + apartment_component +
                                corner_prefix + side_street_added_word
                            )
                        else:
                            # Is type 2.1.1 right building
                            components.append(
                                principal_street_added_word +
                                corner_prefix + side_street_added_word +
                                building_component + apartment_component
                            )
                    else:
                        # Not contain building
                        components.append(principal_street_added_word + corner_prefix + side_street_added_word)
            else:
                # Is type 3
                principal_street_added_word = self.__generate_prefix_or_suffix_randomly(principal_street,
                                                                                        entity_type='principal_street')
                components.append(principal_street_added_word)
                if rm.randint(1, 100) <= 50:
                    # Contain building
                    building_component, apartment_component = self.generate_building_and_apartment()
                    components.append(building_component)
                    components.append(apartment_component)
            # permutation between components
            permutation_bool = rm.randint(1, 100) <= 5

            # Components Basics
            if not self.__is_empty(locality):
                between_prefix = [[' , ', 'rw']] if rm.randint(1, 100) < 70 and permutation_bool is False else []
                locality_prefix = super().generate_prefix_randomly(LOCALITY_PREFIX, 25)
                components.append(
                    between_prefix + locality_prefix + [[item, 'locality'] for item in locality.split()]
                )
            if not self.__is_empty(municipality):
                between_prefix = [[' , ', 'rw']] if rm.randint(1, 100) < 75 and permutation_bool is False else []
                municipality_prefix = super().generate_prefix_randomly(MUNICIPALITY_PREFIX, 5)
                components.append(
                    between_prefix + municipality_prefix + [[item, 'municipality'] for item in municipality.split()]
                )
            if not self.__is_empty(province):
                province_prefix = super().generate_prefix_randomly(PROVINCE_PREFIX, 1)
                between_prefix = [[' , ', 'rw']] if rm.randint(1, 100) < 85 and permutation_bool is False else []
                components.append(
                    between_prefix + province_prefix + [[item, 'province'] for item in province.split()]
                )

            #  Components permutation
            if permutation_bool:
                components = super().generate_non_standardization(components)

            address_number += 1
            self.__add_new_address(components, address_number, address_list, words_list, tags_list)

        # Adding real address
        real_address = self.__add_real_address()
        for address in real_address:
            address_number += 1
            self.__add_new_address(address, address_number, address_list, words_list, tags_list)
        print('El total de direcciones fue de ', address_number)
        return self.__generate_data_frame(address_list, words_list, tags_list)

    def generate_building_and_apartment(self):
        """
            Returns a tupa of two items. The first item is a list containing what is related to buildings and the other item is a list referring to apartments.
            If no apartment was generated, by probability, then the second item will be an empty list
        :return: tuple(building_list, apartment_list)
        """

        identification_building = self.__generate_building_syntetic()
        identification_building_prefix = super().generate_prefix_randomly(BUILDING_PREFIX, 90)
        building_number = []
        if not identification_building.isalpha():
            building_number = super().generate_prefix_randomly(PROPERTY_PREFIX, 15)

        random_value = rm.randint(1, 100)
        if random_value > 40:
            # Does not contain apartment
            return (identification_building_prefix + building_number + [[item, 'building'] for item in
                                                                    identification_building.split()], [])
        elif random_value <= 39:
            # Contain apartment
            # is_explicit_apartment

            identification_apartment = self.__generate_apartment_syntetic()
            identification_apartment_prefix = super().generate_prefix_randomly(APARTMENT_PREFIX,
                                                                               70)
            apartment_number = []
            if not identification_apartment.isalpha():
                apartment_number = super().generate_prefix_randomly(PROPERTY_PREFIX, 15)

            apartment_specification = super().generate_prefix_randomly(APARTMENT_SPECIFICATION, 2)

            return (identification_building_prefix + building_number + [[item, 'building'] for item in
                                                  identification_building.split()]), \
                (identification_apartment_prefix + apartment_number + [[item, 'apartment'] for item
                                                                      in identification_apartment.split()] +
                 apartment_specification)
        else:
            # is implicit apartment
            identification_apartment_implicit_prefix = super().generate_prefix_randomly(IMPLICIT_APARTMENT,
                                                                               100)

            return ((identification_building_prefix + building_number + [[item, 'building'] for item in
                                                                        identification_building.split()]),
                    identification_apartment_implicit_prefix)

    def __generate_data_frame(self, address_list, words_list, tags_list):
        return DataFrame({
            'Sentence #': address_list,
            'Word': words_list,
            'Tag': tags_list
        })

    def __add_new_address(self, components, address_number, address_list, words_list, tags_list):
        address_list.append('Sentence ' + str(address_number))

        # breaking down
        georeferential_elements_list = []
        for element in components:
            georeferential_elements_list += element

        count = 0
        var_aleatory = rm.randint(1, 6)
        amount_errors = var_aleatory if rm.randint(1, 10) <= 2 else 0
        for compound_items in georeferential_elements_list:
            if compound_items[0] != 'nan':
                word = str(compound_items[0])
                if amount_errors > 0 and rm.randint(1, 10) <= 3:
                    word = super().generate_spelling_errors(word)

                words_list.append(word)
                tags_list.append(str(compound_items[1]))

                if count != 0 and len(words_list) == len(address_list) + 1:
                    address_list.append(None)
            count += 1

    def __is_empty(self, entity):

        return len(entity) == 0 or len(entity.split()) == 0 or entity == 'nan' or entity is None

    def __generate_building_syntetic(self):
        random_value = rm.randint(1, 100)
        if random_value <= 38:
            # only numbers
            number = rm.randint(1, 100)
            # two digits
            if number <= 25:
                return str(rm.randint(1, 99))
            # three digits
            if number <= 50:
                return str(rm.randint(100, 999))
            # four digits
            if number <= 75:
                return str(rm.randint(1000, 9999))
            # five digits
            if number <= 100:
                return str(rm.randint(10000, 99999))

        elif random_value <= 56:
            # only letter
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'R', 'S', 'T']
            temp = rm.randint(0, 100)
            if temp <= 90:
                # one letter
                return letters[rm.randint(0, len(letters) - 1)]
            else:
                # two letters
                return letters[rm.randint(0, len(letters) - 1)] + letters[rm.randint(0, len(letters) - 1)]

        else:
            #  numbers and letters
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'R', 'S', 'T']
            letter = letters[rm.randint(0, len(letters) - 1)]
            number = ''
            random_number = rm.randint(1, 100)
            # two digits
            if random_number <= 25:
                number = str(rm.randint(1, 99))
            # three digits
            elif random_number <= 50:
                number = str(rm.randint(100, 999))
            # four digits
            elif random_number <= 75:
                number = str(rm.randint(1000, 9999))
            # five digits
            elif random_number <= 100:
                number = str(rm.randint(10000, 99999))

            letter_position = rm.randint(0, len(number)-1)
            building_name = number[0: letter_position] + letter + number[letter_position:]
            return building_name

    def __generate_apartment_syntetic(self):
        random_value = rm.randint(1, 100)
        if random_value <= 50:
            # only numbers
            return str(rm.randint(10, 101))
        elif random_value <= 75:
            # only letters
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'R', 'S', 'T']
            return letters[rm.randint(0, len(letters) - 1)]
        else:
            #  numbers and letters
            letters = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'R', 'S', 'T']
            letter = letters[rm.randint(0, len(letters) - 1)]
            letter_position = rm.randint(0, 2)
            number = str(rm.randint(1, 90))

            return number[0: letter_position] + letter + number[letter_position:]

    def __generate_prefix_or_suffix_randomly(self, street_name: str, entity_type: str):
        '''
        :param street_name:
        :return:
            A list of reserved words that will correspond to suffixes or street prefixes.
            A boolean indicating whether the list corresponds to a suffix or prefix.
        '''

        street_name_contain_some_type_prefix = False
        for type in STREET_NAME_PREFIX:
            for word in street_name.split():
                if type.lower() == word.lower():
                    street_name_contain_some_type_prefix = True
                    break
            if street_name_contain_some_type_prefix:
                break

        if not street_name_contain_some_type_prefix:
            possibility_suffix = self.__eval_possibility_suffix_street(street_name)
            if possibility_suffix:
                return [[item, entity_type] for item in street_name.split()] + super().generate_suffix_randomly(
                    STREET_NAME_SUFFIX, 90)

            return super().generate_prefix_randomly(STREET_NAME_PREFIX, 50) + [[item, entity_type] for item in
                                                                               street_name.split()]
        else:
            return [[item, entity_type] for item in street_name.split()]
    def __eval_possibility_suffix_street(self, street_name: str):

        if not self.__is_empty(street_name):
            for poss in STREET_SUFFIX_POSSIBILITIES:
                if poss == street_name.lower():
                    return True

        return False

    def __generate_conjunction(self):
        '''
            This function will return one of the following conjunctions "and, &, &&"
        '''
        if rm.randint(0, 100) <= 6:
            if rm.randint(0, 10) < 7:
                return '&'
            else:
                return '&%'
        else:
            return 'y'

    def __add_real_address(self):
        '''
            :return 19 real address
        '''
        return [
            [[['calle', 'rw'], ['30', 'principal_street'], ['959', 'building'], ['e', 'apartment'], ['entre', 'rw'],
              ['avenida', 'rw'], ['26', 'first_side_street'], ['y', 'rw'], ['47', 'second_side_street'],
              ['Plaza', 'municipality'], ['de', 'municipality'], ['la', 'municipality'], ['Revolucion', 'municipality'],
              ['La', 'province'], ['Habana', 'province']]],
            [[['ave', 'rw'], ['67', 'principal_street'], ['no', 'rw'], ['13613', 'building'], ['e', 'apartment'],
              ['136', 'first_side_street'], ['y', 'rw'], ['138', 'second_side_street'], ['Marianao', 'municipality'],
              ['Marianao', 'municipality'], ['La', 'province'], ['HAbana', 'province'], ]],
            [[['calle', 'rw'], ['Gomez', 'principal_street'], ['2', 'building'], ['E', 'building'], ['entre', 'rw'],
              ['calle', 'rw'], ['Marti', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'],
              ['Washington', 'second_side_street'], ['reparto', 'rw'], ['barrio', 'rw'], ['Azul', 'locality'],
              ['Arroyo', 'municipality'], ['Naranjo', 'municipality'], ['La', 'province'], ['Habana', 'province']]],
            [[['San', 'principal_street'], ['Juan', 'principal_street'], ['de', 'principal_street'],
              ['Dios', 'principal_street'], ['Edif', 'rw'], ['108', 'building'], ['apto', 'rw'], ['15', 'apartment'],
              ['entre', 'rw'], ['aguacate', 'first_side_street'], ['y', 'rw'], ['Compostela', 'second_side_street'],
              ['La', 'municipality'], ['Habana', 'municipality'], ['Vieja', 'municipality'], ['La', 'province'],
              ['Habana', 'province']]],
            [[['avenida', 'rw'], ['del', 'principal_street'], ['sur', 'principal_street'], ['entre', 'rw'],
              ['primelles', 'first_side_street'], ['y', 'rw'], ['Lazada', 'second_side_street'], [',', 'rw'],
              ['Norte', 'locality'], ['III', 'locality'], [',', 'rw'], ['CERRO', 'municipality'], [',', 'rw'],
              ['LA', 'province'], ['HABANA', 'province'], ]],
            [[['San', 'principal_street'], ['Juan', 'principal_street'], ['DE', 'principal_street'],
              ['dios', 'principal_street'], ['entre', 'rw'], ['aguacate', 'first_side_street'], ['y', 'rw'],
              ['compostela', 'second_side_street'], [',', 'rw'], ['La', 'municipality'], ['Habana', 'municipality'],
              ['Vieja', 'municipality'], [',', 'rw'], ['La', 'province'], ['Habana', 'province'], ]],
            [[['27', 'principal_street'], ['b', 'principal_street'], ['entre', 'rw'], ['230', 'first_side_street'],
              ['y', 'rw'], ['234', 'second_side_street'], [',', 'rw'], ['La', 'locality'], ['Coronela', 'locality'],
              [',', 'rw'], ['La', 'municipality'], ['Lisa', 'municipality'], [',', 'rw'], ['La', 'province'],
              ['Habana', 'province'], ]],
            [[['calle', 'rw'], ['REYES', 'principal_street'], ['entre', 'rw'], ['c', 'first_side_street'], ['y', 'rw'],
              ['calle', 'rw'], ['Altarriba', 'second_side_street'], ['Edificio', 'rw'], ['319', 'building'],
              ['Apto', 'rw'], ['9', 'apartment'], ['Barrio', 'rw'], ['Lawton', 'locality'], ['Diez', 'municipality'],
              ['de', 'municipality'], ['Octubre', 'municipality'], ['La', 'province'], ['Habana', 'province'], ]],
            [[['calle', 'rw'], ['real', 'principal_street'], ['#', 'rw'], ['360', 'building'], ['poblado', 'rw'],
              ['bacuranao', 'locality'], [',', 'rw'], ['guanabacoa', 'municipality'], [',', 'rw'], ['La', 'province'],
              ['Habana', 'province'], ]],
            [[['calle', 'rw'], ['82', 'principal_street'], ['E', 'rw'], ['/', 'rw'], ['calle', 'rw'],
              ['5D', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'], ['7', 'second_side_street'],
              ['Edificio', 'rw'], ['iacc', 'building'], ['#', 'rw'], ['5d14', 'building'], [',', 'rw'], ['apto', 'rw'],
              ['8', 'apartment'], ['repto', 'rw'], ['villa', 'locality'], ['panamericana', 'locality'], [',', 'rw'],
              ['La', 'municipality'], ['Habana', 'municipality'], ['del', 'municipality'], ['Este', 'municipality'],
              [',', 'rw'], ['La', 'province'], ['Habana', 'province'], ]],
            [[['calle', 'rw'], ['5ta', 'principal_street'], ['num', 'rw'], ['5800', 'building'], ['Bajo', 'rw'],
              ['entre', 'rw'], ['calle', 'rw'], ['b', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'],
              ['c', 'second_side_street'], [',', 'rw'], ['SAN', 'municipality'], ['MIGUEL', 'municipality'],
              ['DEL', 'municipality'], ['PADRON', 'municipality'], [',', 'rw'], ['LA', 'province'],
              ['HABANA', 'province'], ]],
            [[['calle', 'rw'], ['A', 'principal_street'], ['no', 'rw'], ['48', 'building'], ['y', 'rw'], ['apto', 'rw'],
              ['1', 'apartment'], ['e', 'apartment'], ['entre', 'rw'], ['calle', 'rw'], ['pinar', 'first_side_street'],
              ['del', 'first_side_street'], ['rio', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'],
              ['woodberry', 'second_side_street'], ['reparto', 'rw'], ['callejas', 'locality'],
              ['ARROYO', 'municipality'], ['NARANJO', 'municipality'], ['LA', 'province'], ['HABANA', 'province']]],
            [[['calle', 'rw'], ['7ma', 'principal_street'], ['e', 'rw'], ['entre', 'rw'], ['calle', 'rw'],
              ['l', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'], ['10', 'second_side_street'],
              ['edificio', 'rw'], ['10103', 'building'], ['apto', 'rw'], ['23', 'apartment'], ['reparto', 'rw'],
              ['Altahabana', 'locality'], ['BOYEROS', 'municipality'], ['LA', 'province'], ['HABANA', 'province'], ]],
            [[['avenida', 'rw'], ['27', 'principal_street'], ['b', 'principal_street'], ['entre', 'rw'],
              ['calle', 'rw'], ['230', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'],
              ['234', 'second_side_street'], ['edificio', 'rw'], ['22', 'building'], ['apto', 'rw'],
              ['18', 'apartment'], ['reparto', 'rw'], ['la', 'locality'], ['coronela', 'locality'],
              ['la', 'municipality'], ['lisa', 'municipality'], ['La', 'province'], ['Habana', 'province'], ]],
            [[['avenida', 'rw'], ['27', 'principal_street'], ['b', 'principal_street'], ['e', 'rw'], ['entre', 'rw'],
              ['calle', 'rw'], ['230', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'],
              ['234', 'second_side_street'], ['Edificio', 'rw'], ['10', 'building'], ['Apto', 'rw'],
              ['19', 'apartment'], ['reparto', 'rw'], ['la', 'locality'], ['coronela', 'locality'],
              ['la', 'municipality'], ['lisa', 'municipality'], ['La', 'province'], ['Habana', 'province'], ]],
            [[['calle', 'rw'], ['100', 'principal_street'], ['5907', 'building'], ['bajos', 'rw'], ['entre', 'rw'],
              ['ave', 'rw'], ['59', 'first_side_street'], ['y', 'rw'], ['61', 'second_side_street'],
              ['Marianao', 'municipality'], ['La', 'province'], ['HABANA', 'province'], ]],
            [[['Cisneros', 'principal_street'], ['21', 'building'], ['Altos', 'rw'], ['e', 'rw'], ['entre', 'rw'],
              ['arnao', 'first_side_street'], ['y', 'rw'], ['cortez', 'second_side_street'], ['ARROYO', 'municipality'],
              ['NARANJO', 'municipality'], ['LA', 'province'], ['HABANA', 'province'], ]],
            [[['avenida', 'rw'], ['47', 'principal_street'], ['4003', 'building'], ['e', 'rw'], ['entre', 'rw'],
              ['calle', 'rw'], ['40', 'first_side_street'], ['y', 'rw'], ['avenida', 'rw'],
              ['41', 'second_side_street'], ['reparto', 'rw'], ['kohly', 'locality'], ['playa', 'municipality'],
              ['la', 'province'], ['habana', 'province'], ]],
            [[['calle', 'rw'], ['59', 'principal_street'], ['no', 'rw'], ['10814A', 'building'], ['e', 'rw'],
              ['entre', 'rw'], ['108', 'first_side_street'], ['y', 'rw'], ['110', 'second_side_street'], ['Apto', 'rw'],
              ['3', 'apartment'], ['marianao', 'municipality'], ['la', 'province'], ['habana', 'province']]],
        ]

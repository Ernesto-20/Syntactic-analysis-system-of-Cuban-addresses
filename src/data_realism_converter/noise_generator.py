import math
from pandas import DataFrame
import random as rm
import itertools as itt

from src.data_realism_converter.generator import Generator
from src.tools.lookup import STREET_NAME_PREFIX, LOCALITY_PREFIX, MUNICIPALITY_PREFIX, PROVINCE_PREFIX, BETWEEN_PREFIX, \
    BUILDING_PREFIX, BUILDING_SUBDIVISION_PREFIX, CORNER_CONNECTOR_PREFIX


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
        print('Generate Noise II -- Type One')
        address_number = 0
        address_list = []
        words_list = []
        tags_list = []

        for i in data_set.index:
            if address_amount is not None and address_number == address_amount:
                break
            components = []

            principal_street = str(data_set.iloc[i, 0])
            first_side_street = str(data_set.iloc[i, 1])
            second_side_street = str(data_set.iloc[i, 2])
            locality = str(data_set.iloc[i, 3])
            municipality = str(data_set.iloc[i, 4])
            province = str(data_set.iloc[i, 5])

            # RECORDAR LOS SUFIJOS: 5ta Ave. ; primera avenida
            # Determinar si es tipo 1 o 2:
            if not self.__is_empty(first_side_street) and not self.__is_empty(second_side_street):
                #   Is type one
                principal_street_prefix = super().generate_prefix_randomly(STREET_NAME_PREFIX, 50)
                first_side_street_prefix = super().generate_prefix_randomly(STREET_NAME_PREFIX, 50)
                second_side_street_prefix = super().generate_prefix_randomly(STREET_NAME_PREFIX, 50)

                between_prefix = super().generate_prefix_randomly(BETWEEN_PREFIX, 100)
                conjunction_prefix = [[
                    'e' if (len(second_side_street_prefix) == 0 and second_side_street[0] == 'i') else 'y', 'rw']]

                # create component
                components.append(
                    principal_street_prefix + [[item, 'principal_street'] for item in principal_street.split()]
                )
                flag = False
                if rm.randint(1, 100) < 15:
                    flag = True
                    components.append(
                        between_prefix + first_side_street_prefix + [[item, 'first_side_street'] for item in
                                                                     first_side_street.split()] + conjunction_prefix +
                        second_side_street_prefix + [[item, 'second_side_street'] for item in second_side_street.split()]
                    )

                if rm.randint(1, 100) <= 50:
                    # Contain building
                    identification_building = self.__generate_building_syntetic()
                    identification_building_prefix = super().generate_prefix_randomly(BUILDING_PREFIX, 90)
                    if rm.randint(1, 100) <= 40:
                        components.append(
                            identification_building_prefix + [[item, 'building'] for item in
                                                              identification_building.split()]
                        )
                    else:
                        # Contain apartment
                        identification_apartment = self.__generate_apartment_syntetic()
                        identification_apartment_prefix = super().generate_prefix_randomly(BUILDING_SUBDIVISION_PREFIX,
                                                                                           100)

                        components.append(
                            identification_building_prefix + [[item, 'building'] for item in
                                                              identification_building.split()] +
                            identification_apartment_prefix + [[item, 'apartment'] for item
                                                               in identification_apartment.split()]
                        )
                if not flag:
                    components.append(
                        between_prefix + first_side_street_prefix + [[item, 'first_side_street'] for item in
                                                                     first_side_street.split()] + conjunction_prefix +
                        second_side_street_prefix + [[item, 'second_side_street'] for item in
                                                     second_side_street.split()]
                    )
            elif not self.__is_empty(first_side_street) or not self.__is_empty(second_side_street):
                #   Is type 2
                side_street = first_side_street if self.__is_empty(second_side_street) else second_side_street

                principal_street_prefix = super().generate_prefix_randomly(STREET_NAME_PREFIX, 50)
                side_street_prefix = super().generate_prefix_randomly(STREET_NAME_PREFIX, 50)

                if rm.randint(1, 100) <= 50:
                    # Is type 2.1
                    corner_prefix = super().generate_prefix_randomly(CORNER_CONNECTOR_PREFIX, 100)
                    conjunction_prefix = [['e' if (len(side_street_prefix) == 0 and side_street[0] == 'i') else 'y',
                                           'rw']]

                    if rm.randint(1, 100) <= 50:
                        # Contain Building
                        identification_building = self.__generate_building_syntetic()
                        identification_building_prefix = super().generate_prefix_randomly(BUILDING_PREFIX, 90)

                        if rm.randint(1, 100) <= 50:
                            # Is type 2.1.1 left building
                            components.append(
                                corner_prefix + principal_street_prefix + [[item, 'principal_street'] for item in
                                                                           principal_street.split()] +
                                identification_building_prefix + [[item, 'building'] for item in
                                                                  identification_building.split()] +
                                conjunction_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                           side_street.split()]
                            )
                        else:
                            # Is type 2.1.1 right building
                            components.append(
                                corner_prefix + principal_street_prefix + [[item, 'principal_street'] for item in
                                                                           principal_street.split()] +
                                conjunction_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                           side_street.split()] +
                                identification_building_prefix + [[item, 'building'] for item in
                                                                  identification_building.split()]
                            )
                    else:
                        # Not contain building
                        components.append(
                            corner_prefix + principal_street_prefix + [[item, 'principal_street'] for item in
                                                                       principal_street.split()] +
                            conjunction_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                       side_street.split()]
                        )
                else:
                    # Is type 2.2
                    corner_prefix = super().generate_prefix_randomly(CORNER_CONNECTOR_PREFIX, 100)

                    if rm.randint(1, 100) <= 50:
                        # Contain Building
                        identification_building = self.__generate_building_syntetic()
                        identification_building_prefix = super().generate_prefix_randomly(BUILDING_PREFIX, 90)

                        if rm.randint(1, 100) <= 50:
                            # Is type 2.1.1 left building
                            components.append(
                                principal_street_prefix + [[item, 'principal_street'] for item in
                                                           principal_street.split()] +
                                identification_building_prefix + [[item, 'building'] for item in
                                                                  identification_building.split()] +
                                corner_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                      side_street.split()]
                            )
                        else:
                            # Is type 2.1.1 right building
                            components.append(
                                principal_street_prefix + [[item, 'principal_street'] for item in
                                                           principal_street.split()] +
                                corner_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                      side_street.split()] +
                                identification_building_prefix + [[item, 'building'] for item in
                                                                  identification_building.split()]
                            )
                    else:
                        # Not contain building
                        components.append(
                            principal_street_prefix + [[item, 'principal_street'] for item in
                                                       principal_street.split()] +
                            corner_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                  side_street.split()]
                        )
            else:
                # Is type 3
                principal_street_prefix = super().generate_prefix_randomly(STREET_NAME_PREFIX, 70)
                components.append(
                    principal_street_prefix + [[item, 'principal_street'] for item in principal_street.split()]
                )
                if rm.randint(1, 100) <= 50:
                    # Contain building
                    identification_building = self.__generate_building_syntetic()
                    identification_building_prefix = super().generate_prefix_randomly(BUILDING_PREFIX, 90)
                    if rm.randint(1, 100) <= 30:
                        components.append(
                            identification_building_prefix + [[item, 'building'] for item in
                                                              identification_building.split()]
                        )
                    else:
                        # Contain apartment
                        identification_apartment = self.__generate_apartment_syntetic()
                        identification_apartment_prefix = super().generate_prefix_randomly(BUILDING_SUBDIVISION_PREFIX,100)
                        components.append(
                            identification_building_prefix + [[item, 'building'] for item in
                                                              identification_building.split()] +
                            identification_apartment_prefix + [[item, 'apartment'] for item
                                                               in identification_apartment.split()]
                        )
            # Components Basics
            if not self.__is_empty(locality):
                between_prefix = [[' , ', 'rw']] if rm.randint(1, 100) < 70 else []
                locality_prefix = super().generate_prefix_randomly(LOCALITY_PREFIX, 35)
                components.append(
                    between_prefix + locality_prefix + [[item, 'locality'] for item in locality.split()]
                )
            if not self.__is_empty(municipality):
                between_prefix = [[' , ', 'rw']] if rm.randint(1, 100) < 75 else []
                municipality_prefix = super().generate_prefix_randomly(MUNICIPALITY_PREFIX, 8)
                components.append(
                    between_prefix + municipality_prefix + [[item, 'municipality'] for item in municipality.split()]
                )
            if not self.__is_empty(province):
                province_prefix = super().generate_prefix_randomly(PROVINCE_PREFIX, 3)
                between_prefix = [[' , ', 'rw']] if rm.randint(1, 100) < 85 else []
                components.append(
                    between_prefix + province_prefix + [[item, 'province'] for item in province.split()]
                )

            #  Permutación entre componentes.
            if rm.randint(1, 100) <= 5:
                components = super().generate_non_standardization(components)

            address_number += 1
            self.__add_new_address(components, address_number, address_list, words_list, tags_list)

        # Adding real address
        real_address = self.__add_real_address()
        for address in real_address:
            address_number += 1
            self.__add_new_address(address, address_number, address_list, words_list, tags_list)

        return self.__generate_data_frame(address_list, words_list, tags_list)

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
        amount_errors = var_aleatory if rm.randint(0, 4) == 1 else 0
        for compound_items in georeferential_elements_list:
            if compound_items[0] != 'nan':
                word = str(compound_items[0])
                if amount_errors > 0 and rm.randint(1, 4) == 1:
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
        if random_value <= 45:
            # only numbers
            return str(rm.randint(101, 99999))
        elif random_value <= 55:
            # only letter
            letters = ['A', 'B', 'C', 'D', 'F', 'G', 'H']
            return letters[rm.randint(0, len(letters) - 1)]
        else:
            #  numbers and letters
            letters = ['A', 'B', 'C', 'D', 'F', 'G', 'H']
            letter = letters[rm.randint(0, len(letters) - 1)]
            letter_position = rm.randint(0, 4)
            number = str(rm.randint(101, 9999))

            name = number[0: letter_position] + letter + number[letter_position:]
            return name

    def __generate_apartment_syntetic(self):
        random_value = rm.randint(1, 100)
        if random_value <= 50:
            # only numbers
            return str(rm.randint(10, 101))
        else:
            #  numbers and letters
            letters = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'R', 'S', 'T']
            letter = letters[rm.randint(0, len(letters) - 1)]
            letter_position = rm.randint(0, 4)
            number = str(rm.randint(1, 90))

            return number[0: letter_position] + letter + number[letter_position:]

    def __add_real_address(self):
        return [
            [[['calle', 'rw'], ['30', 'principal_street'], ['959', 'building'], ['e', 'rw'], ['entre', 'rw'], ['avenida', 'rw'], ['26', 'first_side_street'], ['y', 'rw'], ['47', 'second_side_street'], ['Plaza', 'municipality'], ['de', 'municipality'], ['la', 'municipality'], ['Revolucion', 'municipality'], ['La', 'province'], ['Habana', 'province']]],
            [[['ave', 'rw'], ['67', 'principal_street'], ['no', 'rw'], ['13613', 'building'], ['e', 'rw'], ['136', 'first_side_street'], ['y', 'rw'], ['138', 'second_side_street'], ['Marianao', 'municipality'], ['Marianao', 'municipality'], ['La', 'province'], ['HAbana', 'province'],]],
            [[['calle', 'rw'], ['Gomez', 'principal_street'], ['2', 'building'], ['E', 'building'], ['entre', 'rw'], ['calle', 'rw'], ['Marti', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'], ['Washington', 'second_side_street'], ['reparto', 'rw'], ['barrio', 'rw'], ['Azul', 'locality'], ['Arroyo', 'municipality'], ['Naranjo', 'municipality'], ['La', 'province'], ['Habana', 'province']]],
            [[['San', 'principal_street'], ['Juan', 'principal_street'], ['de', 'principal_street'], ['Dios', 'principal_street'], ['Edif', 'rw'], ['108', 'building'], ['apto', 'rw'], ['15', 'apartment'], ['entre', 'rw'], ['aguacate', 'first_side_street'], ['y', 'rw'], ['Compostela', 'second_side_street'], ['La', 'municipality'], ['Habana', 'municipality'], ['Vieja', 'municipality'], ['La', 'province'], ['Habana', 'province']]],
            [[['avenida', 'rw'], ['del', 'principal_street'], ['sur', 'principal_street'], ['entre', 'rw'], ['primelles', 'first_side_street'], ['y', 'rw'], ['Lazada', 'second_side_street'], [',', 'rw'], ['Norte', 'locality'], ['III', 'locality'], [',', 'rw'], ['CERRO', 'municipality'], [',', 'rw'], ['LA', 'province'], ['HABANA', 'province'],]],
            [[['San', 'principal_street'], ['Juan', 'principal_street'], ['DE', 'principal_street'], ['dios', 'principal_street'], ['entre', 'rw'], ['aguacate', 'first_side_street'], ['y', 'rw'], ['compostela', 'second_side_street'], [',', 'rw'], ['La', 'municipality'], ['Habana', 'municipality'], ['Vieja', 'municipality'], [',', 'rw'], ['La', 'province'], ['Habana', 'province'],]],
            [[['27', 'principal_street'], ['b', 'principal_street'], ['entre', 'rw'], ['230', 'first_side_street'], ['y', 'rw'], ['234', 'second_side_street'], [',', 'rw'], ['La', 'locality'], ['Coronela', 'locality'], [',', 'rw'], ['La', 'municipality'], ['Lisa', 'municipality'], [',', 'rw'], ['La', 'province'], ['Habana', 'province'],]],
            [[['calle', 'rw'], ['REYES', 'principal_street'], ['entre', 'rw'], ['c', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'], ['Altarriba', 'second_side_street'], ['Edificio', 'rw'], ['319', 'building'], ['Apto', 'rw'], ['9', 'apartment'], ['Barrio', 'rw'], ['Lawton', 'locality'], ['Diez', 'municipality'], ['de', 'municipality'], ['Octubre', 'municipality'], ['La', 'province'], ['Habana', 'province'],]],
            [[['calle', 'rw'], ['real', 'principal_street'], ['#', 'rw'], ['360', 'building'], ['poblado', 'rw'], ['bacuranao', 'locality'], [',', 'rw'], ['guanabacoa', 'municipality'], [',', 'rw'], ['La', 'province'], ['Habana', 'province'],]],
            [[['calle', 'rw'], ['82', 'principal_street'], ['E', 'rw'], ['/', 'rw'], ['calle', 'rw'], ['5D', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'], ['7', 'second_side_street'], ['Edificio', 'rw'], ['iacc', 'building'], ['#', 'rw'], ['5d14', 'building'], [',', 'rw'], ['apto', 'rw'], ['8', 'apartment'], ['repto', 'rw'], ['villa', 'locality'], ['panamericana', 'locality'], [',', 'rw'], ['La', 'municipality'], ['Habana', 'municipality'], ['del', 'municipality'], ['Este', 'municipality'], [',', 'rw'], ['La', 'province'], ['Habana', 'province'],]],
            [[['calle', 'rw'], ['5ta', 'principal_street'], ['num', 'rw'], ['5800', 'building'], ['Bajo', 'rw'], ['entre', 'rw'], ['calle', 'rw'], ['b', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'], ['c', 'second_side_street'], [',', 'rw'], ['SAN', 'municipality'], ['MIGUEL', 'municipality'], ['DEL', 'municipality'], ['PADRON', 'municipality'], [',', 'rw'], ['LA', 'province'], ['HABANA', 'province'],]],
            [[['calle', 'rw'], ['A', 'principal_street'], ['no', 'rw'], ['48', 'building'], ['y', 'rw'], ['apto', 'rw'], ['1', 'apartment'], ['e', 'rw'], ['entre', 'rw'], ['calle', 'rw'], ['pinar', 'first_side_street'], ['del', 'first_side_street'], ['rio', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'], ['woodberry', 'second_side_street'], ['reparto', 'rw'], ['callejas', 'locality'], ['ARROYO', 'municipality'], ['NARANJO', 'municipality'], ['LA', 'province'], ['HABANA', 'province']]],
            [[['calle', 'rw'], ['7ma', 'principal_street'], ['e', 'rw'], ['entre', 'rw'], ['calle', 'rw'], ['l', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'], ['10', 'second_side_street'], ['edificio', 'rw'], ['10103', 'building'], ['apto', 'rw'], ['23', 'apartment'], ['reparto', 'rw'], ['Altahabana', 'locality'], ['BOYEROS', 'municipality'], ['LA', 'province'], ['HABANA', 'province'],]],
            [[['avenida', 'rw'], ['27', 'principal_street'], ['b', 'principal_street'], ['entre', 'rw'], ['calle', 'rw'], ['230', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'], ['234', 'second_side_street'], ['edificio', 'rw'], ['22', 'building'], ['apto', 'rw'], ['18', 'apartment'], ['reparto', 'rw'], ['la', 'locality'], ['coronela', 'locality'], ['la', 'municipality'], ['lisa', 'municipality'], ['La', 'province'], ['Habana', 'province'],]],
            [[['avenida', 'rw'], ['27', 'principal_street'], ['b', 'principal_street'], ['e', 'rw'], ['entre', 'rw'], ['calle', 'rw'], ['230', 'first_side_street'], ['y', 'rw'], ['calle', 'rw'], ['234', 'second_side_street'], ['Edificio', 'rw'], ['10', 'building'], ['Apto', 'rw'], ['19', 'apartment'], ['reparto', 'rw'], ['la', 'locality'], ['coronela', 'locality'], ['la', 'municipality'], ['lisa', 'municipality'], ['La', 'province'], ['Habana', 'province'],]],
            [[['calle', 'rw'], ['100', 'principal_street'], ['5907', 'building'], ['bajos', 'rw'], ['entre', 'rw'], ['ave', 'rw'], ['59', 'first_side_street'], ['y', 'rw'], ['61', 'second_side_street'], ['Marianao', 'municipality'], ['La', 'province'], ['HABANA', 'province'],]],
            [[['Cisneros', 'principal_street'], ['21', 'building'], ['Altos', 'rw'], ['e', 'rw'], ['entre', 'rw'], ['arnao', 'first_side_street'], ['y', 'rw'], ['cortez', 'second_side_street'], ['ARROYO', 'municipality'], ['NARANJO', 'municipality'], ['LA', 'province'], ['HABANA', 'province'],]],
            [[['avenida', 'rw'], ['47', 'principal_street'], ['4003', 'building'], ['e', 'rw'], ['entre', 'rw'], ['calle', 'rw'], ['40', 'first_side_street'], ['y', 'rw'], ['avenida', 'rw'], ['41', 'second_side_street'], ['reparto', 'rw'], ['kohly', 'locality'], ['playa', 'municipality'], ['la', 'province'], ['habana', 'province'],]],
            [[['calle', 'rw'], ['59', 'principal_street'], ['no', 'rw'], ['10814A', 'building'], ['e', 'rw'], ['entre', 'rw'], ['108', 'first_side_street'], ['y', 'rw'], ['110', 'second_side_street'], ['Apto', 'rw'], ['3', 'apartment'], ['marianao', 'municipality'], ['la', 'province'], ['habana', 'province']]],
        ]

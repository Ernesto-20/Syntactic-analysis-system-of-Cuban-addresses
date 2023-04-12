import math
from abc import ABC, abstractmethod
from pandas import DataFrame
import pandas as pd
from keras.utils import pad_sequences
from keras.utils import to_categorical
import random as rm
import itertools as itt

from src.tools.lookup import STREET_NAME_PREFIX, LOCALITY_PREFIX, MUNICIPALITY_PREFIX, PROVINCE_PREFIX, BETWEEN_PREFIX, \
    BUILDING_PREFIX, BUILDING_SUBDIVISION_PREFIX, CORNER_CONECTOR_PREFIX


class NoiseGenerator:
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

    '''

    # NECESITO metodo que genere casa, edifico y apartamento.

    def generate_noise(self, data_set: DataFrame, address_amount=15333):
        print('Generate Noise II -- Type One')
        address_number = 0
        address_list = []
        words_list = []
        tags_list = []

        for i in data_set.index:
            if address_number == address_amount:
                break

            dictAddress = {}
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
                principal_street_prefix = self.__generate_prefix(STREET_NAME_PREFIX, 65)
                first_side_street_prefix = self.__generate_prefix(STREET_NAME_PREFIX, 65)
                second_side_street_prefix = self.__generate_prefix(STREET_NAME_PREFIX, 65)

                between_prefix = self.__generate_prefix(BETWEEN_PREFIX, 100)
                conjunction_prefix = [[
                    'e' if (len(second_side_street_prefix) == 0 and second_side_street[0]) == 'i' else 'y', 'rw']]

                # create component
                components.append(
                    principal_street_prefix + [[item, 'principal_street'] for item in principal_street.split()]
                )
                components.append(
                    between_prefix + first_side_street_prefix + [[item, 'first_side_street'] for item in
                                                                 first_side_street.split()] + conjunction_prefix +
                    second_side_street_prefix + [[item, 'second_side_street'] for item in second_side_street.split()]
                )

                if rm.randint(1, 100) <= 25:
                    # Contain building
                    identification_building = self.__generate_building_syntetic()
                    identification_building_prefix = self.__generate_prefix(BUILDING_PREFIX, 90)
                    if rm.randint(1, 100) <= 70:
                        components.append(
                            identification_building_prefix + [[item, 'building'] for item in
                                                                                         identification_building.split()]
                        )
                    else:
                        # Contain apartment
                        identification_apartment = self.__generate_apartment_syntetic()
                        identification_apartment_prefix = self.__generate_prefix(BUILDING_SUBDIVISION_PREFIX, 100)

                        components.append(
                            identification_building_prefix + [[item, 'building'] for item in
                                                                                         identification_building.split()] +
                            identification_apartment_prefix + [[item, 'apartment'] for item
                                                                                          in identification_apartment.split()]
                        )
            else:
                #   Is type 2
                side_street = first_side_street + second_side_street

                principal_street_prefix = self.__generate_prefix(self, STREET_NAME_PREFIX, 60)
                side_street_prefix = self.__generate_prefix(self, STREET_NAME_PREFIX, 60)

                if rm.randint(1, 100) <= 50:
                    # Is type 2.1
                    corner_prefix = self.__generate_prefix(CORNER_CONECTOR_PREFIX, 80)
                    conjunction_prefix = [['e' if (len(side_street_prefix) == 0 and side_street[0]) == 'i' else 'y',
                                          'rw']]

                    if rm.randint(1, 100) <= 25:
                        # Contain Building
                        identification_building = self.__generate_building_syntetic()
                        identification_building_prefix = self.__generate_prefix(BUILDING_PREFIX, 90)

                        if rm.randint(1, 100) <= 50:
                            # Is type 2.1.1 left building
                            components.append(
                                corner_prefix + principal_street_prefix + [[item, 'principal_street'] for item in
                                                                           principal_street.split()] +
                                identification_building_prefix + [[item, 'building'] for item in
                                                                  identification_building.split()] +
                                conjunction_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                           first_side_street.split()]
                            )
                        else:
                            # Is type 2.1.1 right building
                            components.append(
                                corner_prefix + principal_street_prefix + [[item, 'principal_street'] for item in
                                                                           principal_street.split()] +
                                conjunction_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                           first_side_street.split()] +
                                identification_building_prefix + [[item, 'building'] for item in
                                                                  identification_building.split()]
                            )
                    else:
                        # Not contain building
                        components.append(
                            corner_prefix + principal_street_prefix + [[item, 'principal_street'] for item in
                                                                       principal_street.split()] +
                            conjunction_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                       first_side_street.split()]
                        )
                else:
                    # Is type 2.2
                    corner_prefix = self.__generate_prefix(CORNER_CONECTOR_PREFIX, 100)

                    if rm.randint(1, 100) <= 25:
                        # Contain Building
                        identification_building = self.__generate_building_syntetic()
                        identification_building_prefix = self.__generate_prefix(BUILDING_PREFIX, 90)

                        if rm.randint(1, 100) <= 50:
                            # Is type 2.1.1 left building
                            components.append(
                                principal_street_prefix + [[item, 'principal_street'] for item in principal_street.split()] +
                                identification_building_prefix + [[item, 'building'] for item in
                                                                  identification_building.split()] +
                                corner_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                      first_side_street.split()]
                            )
                        else:
                            # Is type 2.1.1 right building
                            components.append(
                                principal_street_prefix + [[item, 'principal_street'] for item in principal_street.split()] +
                                corner_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                      first_side_street.split()] +
                                identification_building_prefix + [[item, 'building'] for item in
                                                                  identification_building.split()]
                            )
                    else:
                        # Not contain building
                        components.append(
                            principal_street_prefix + [[item, 'principal_street'] for item in principal_street.split()] +
                            corner_prefix + side_street_prefix + [[item, 'first_side_street'] for item in
                                                                  first_side_street.split()]
                        )

            # Components Basics
            locality_prefix = self.__generate_prefix(LOCALITY_PREFIX, 35)
            municipality_prefix = self.__generate_prefix(MUNICIPALITY_PREFIX, 35)
            province_prefix = self.__generate_prefix(PROVINCE_PREFIX, 35)

            components.append(
                locality_prefix + [[item, 'locality'] for item in locality.split()]
            )
            components.append(
                municipality_prefix + [[item, 'municipality'] for item in municipality.split()]
            )
            components.append(
                province_prefix + [[item, 'province'] for item in province.split()]
            )

            #  Permutación entre componentes.
            components = self.generate_non_standardization(components)

            address_number += 1
            self.__add_new_address(components, address_number, address_list, words_list, tags_list)

            #  Generar ruido gramatical.

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
        list = []
        for element in components:
            list += element

        count = 0
        for compound_items in list:
            if compound_items[0] != 'nan':
                words_list.append(str(compound_items[0]))
                tags_list.append(str(compound_items[1]))

                if count != 0 and len(words_list) == len(address_list) + 1:
                    address_list.append(None)
            count += 1

    def generate_non_standardization(self, components):
        permutations = list(itt.permutations(components))

        amount_permutation = math.factorial(len(components)) - 1
        reorder_components = permutations[rm.randint(0, amount_permutation)]

        return reorder_components

    def __generate_prefix(self, list_prefix, probability):
        if rm.randint(1, 100) <= probability:
            prefix = list_prefix[rm.randint(0, len(list_prefix) - 1)]
            return [[item, 'rw'] for item in prefix.split()]
        return []

    def __is_empty(self, entity):
        return len(entity.split()) == 0

    def __generate_building_syntetic(self):
        random_value = rm.randint(1, 100)
        if random_value <= 33:
            # only numbers
            return str(rm.randint(101, 999))
        elif random_value <= 66:
            # only letter
            letters = ['A', 'B', 'C', 'D', 'F', 'G', 'H']
            return letters[rm.randint(0, len(letters) - 1)]
        else:
            #  numbers and letters
            letters = ['A', 'B', 'C', 'D', 'F', 'G', 'H']
            letter = letters[rm.randint(0, len(letters)-1)]
            letter_position = rm.randint(0, 4)
            number = str(rm.randint(101, 9999))

            name = number[0: letter_position] + letter + number[letter_position:]
            return name

    def __generate_apartment_syntetic(self):
        random_value = rm.randint(1, 100)
        if random_value <= 6:
            # only numbers
            return str(rm.randint(10, 101))
        else:
            #  numbers and letters
            letters = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'R', 'S', 'T']
            letter = letters[rm.randint(0, len(letters)-1)]
            letter_position = rm.randint(0, 4)
            number = str(rm.randint(10, 100))

            return number[0: letter_position] + letter + number[letter_position:]

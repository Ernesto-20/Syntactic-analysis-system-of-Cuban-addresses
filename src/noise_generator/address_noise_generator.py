import pandas as pd
from pandas import DataFrame
from random import randrange
import random as rm

from src.noise_generator.generator_other_schema import Generator
from src.utils.lookup import *


class AddressNoiseGenerator(Generator):
    def generate_noise(self, data_set: DataFrame, model='building', typea=None, address_amount=None):
        '''

                :param data_set: this is the corpus for generate
                :param model: this variable is for specifying the address model like:
                        write 'building' for model two
                        write 'distance' for model three

                :param type: you can specify which kind of addresses examples you want to use it
                        example for using training addresses  = "train"
                        example for using real addresses  = "eval"

                :param address_amount: this value indicates the amount of addresses this method will use

                :return: DataFrame
                '''

        self.address_amount = address_amount
        self.data = data_set
        self.model = model
        self.typea = typea

        address_number = 0
        address_list = []
        words_list = []
        tag_list = []

        if self.model == 'building':
            address_number = 0
            address_list = []
            words_list = []
            tag_list = []
            dict_list = []

            if self.typea == 'train':

                for index in range(self.address_amount):
                    components = self.__generate_real_example_type_two()
                    address_number += 1
                    self.add_address(components, address_number, address_list, words_list, tag_list)

                return self.create_data_frame(address_list, words_list, tag_list)

            elif self.typea == 'eval':

                for _ in range(self.address_amount):
                    components = self.__generate_real_example_type_two()
                    string = self.components_to_string(components)
                    dict_ = self.components_to_dict(components)
                    address_list.append(string)
                    dict_list.append(dict_)
                    address_number += 1

                return self.create_dataframe(address_list, dict_list)


        elif self.model == 'distance':
            address_number = 0
            address_list = []
            words_list = []
            tag_list = []
            dict_list = []

            if self.typea == 'train':

                for index in range(self.address_amount):
                    components = self.__generate_correct_example_type_three()
                    address_number += 1
                    self.add_address(components, address_number, address_list, words_list, tag_list)

                return self.create_data_frame(address_list, words_list, tag_list)

            elif self.typea == 'eval':

                for _ in range(self.address_amount):
                    components = self.__generate_correct_example_type_three()
                    string = self.components_to_string(components)
                    dict_ = self.components_to_dict(components)
                    address_list.append(string)
                    dict_list.append(dict_)
                    address_number += 1

                return self.create_dataframe(address_list, dict_list)

        else:
            raise NotImplementedError('There is no such kind of example')

    def __generate_real_example_type_two(self):

        components = []

        index = rm.randint(1, len(self.data) - 1)
        building = super().create_building_syntetic()
        locality = str(self.data.loc[index, 'locality'])
        municipality = str(self.data.loc[index, 'municipality'])
        province = str(self.data.loc[index, 'province'])

        building_form = self.generate_prefix_randomly(REAL_BUILDING_PREFIX, 100)
        number_form = self.generate_prefix_randomly(REAL_PROPERTY_PREFIX, 100)
        apartment_form = self.generate_prefix_randomly(REAL_APARTMENT_PREFIX, 100)

        # For creating the first component we have to split itself in three sub-components, if the name of the building is alphanum
        # For example: Edif 456 o 34B
        # [reserved word for building]+ [reserved word for number] + [building]
        # then a random number is used to decide whether or not the number component appears
        # And if it's alpha would be like:
        # [reserved word for building] + [name]

        is_name = True if building.isalpha() else False

        # CREATING COMPONENT 1  --- [building_form],[number_form],[building] ---
        if is_name:
            components.append(
                building_form + [[item, 'building'] for item in
                                 building.split()]
            )
        else:
            # Using the random number mentioned above
            # Add property prefix
            add_num_component = True if rm.randint(0, 100) > 50 else False
            if add_num_component:
                components.append(
                    building_form + number_form + [[item, 'building'] for item in
                                                   building.split()]
                )
            else:
                components.append(
                    building_form + [[item, 'building'] for item in
                                     building.split()]
                )

        # CREATING COMPONENT 2  --- [apartment_form],[number_form],[apartment] ---
        # This component is optional

        add_apart_component = rm.randint(0, 100)
        if add_apart_component > 50:
            apartment = self.create_apartment_syntetic()
            is_num = True if apartment.isdigit() else False
            add_num_component = True if rm.randint(0, 100) > 50 else False
            if add_num_component and is_num:
                components.append(
                    apartment_form + number_form + [[item, 'apartment'] for item in
                                                    apartment.split()]
                )
            else:
                components.append(
                    apartment_form + [[item, 'apartment'] for item in
                                      apartment.split()]
                )

        # omit administrative political divisions
        locality, municipality, province = super().omit_administrative_political(locality, municipality, province, 0.04,
                                                                                 0.02, 0.04)

        # permutation between components
        permutation_bool = rm.randint(1, 100) <= 10

        # CREATING COMPONENT 3  --- [locality_form],[locality] ---
        if not self.check_is_empty(locality):
            between_prefix = [[',', 'rw']] if rm.randint(1, 100) < 70 and permutation_bool is False else []
            zone_form = self.generate_prefix_randomly(REAL_ZONE_PREFIX, 100)
            locality_form = self.generate_prefix_randomly(REAL_LOCALITY_PREFIX, 100)
            loc_aux = ''
            loc_zone = ''
            if locality.lower().find('alamar') != -1:
                spl_loc = locality.split()
                if len(spl_loc) != 1:
                    loc_aux = 'Alamar'
                    for word in spl_loc:
                        if word.lower() != 'alamar':
                            loc_zone += word + ' '

                    # Adding the zone
                    if loc_zone.lower().find('micro') != -1:

                        if rm.randint(0, 50) > 25:
                            components.append(
                                between_prefix + locality_form + [[item, 'locality'] for item in
                                                                  loc_aux.split()] + zone_form + [
                                    [item, 'locality'] for item in
                                    loc_zone.split()]
                            )
                        else:
                            components.append(
                                between_prefix + zone_form + [[item, 'locality'] for item in loc_zone.split()]
                                + locality_form + [[item, 'locality'] for item in loc_aux.split()]
                            )

                    else:
                        if rm.randint(0, 50) > 25:
                            components.append(
                                between_prefix + locality_form + [[item, 'locality'] for item in
                                                                  loc_aux.split()] + between_prefix + zone_form + [
                                    [item, 'locality'] for item in
                                    loc_zone.split()]
                            )
                        else:
                            components.append(
                                between_prefix + zone_form + [[item, 'locality'] for item in loc_zone.split()] +
                                between_prefix + locality_form + [[item, 'locality'] for item in loc_aux.split()]
                            )
                else:
                    components.append(
                        between_prefix + locality_form + [[item, 'locality'] for item in locality.split()]
                    )
            else:
                components.append(
                    between_prefix + locality_form + [[item, 'locality'] for item in locality.split()]
                )

        # CREATING COMPONENT 4  --- [municipality_form],[municipality] ---
        if len(municipality) != 0 or not self.check_is_empty(municipality):
            between_prefix = [[',', 'rw']] if rm.randint(1, 100) < 70 and permutation_bool is False else []
            municipality_prefix = self.generate_prefix_randomly(MUNICIPALITY_PREFIX, 10)

            components.append(
                between_prefix + municipality_prefix + [[item, 'municipality'] for item in municipality.split()]
            )

        # CREATING COMPONENT 5  --- [province_form],[province] ---
        if len(province) != 0 or not self.check_is_empty(province):
            between_prefix = [[',', 'rw']] if rm.randint(1, 100) < 70 and permutation_bool is False else []
            province_prefix = self.generate_prefix_randomly(PROVINCE_PREFIX, 5)
            components.append(
                between_prefix + province_prefix + [[item, 'province'] for item in province.split()]
            )
        if permutation_bool:
            #  Permutación entre componentes.
            components = self.generate_non_standardization(components, 30)

        return components

    def __generate_correct_example_type_three(self):
        components = []

        principal_street = str(rm.choice(self.data['principal_street']))
        distance = str(rm.randint(200, 800))

        index = rm.randint(1, len(self.data) - 1)
        locality = str(self.data.loc[index, 'locality'])
        municipality = str(self.data.loc[index, 'municipality'])
        province = str(self.data.loc[index, 'province'])

        principal_street_prefix = super().generate_prefix_randomly(REAL_STREET_NAME_PREFIX, 100)
        number_form = super().generate_prefix_randomly(REAL_PROPERTY_PREFIX, 100)
        distance_specification_form = super().generate_prefix_randomly(DISTANCE_SPECIFICATION_PREFIX, 100)
        distance_form = super().generate_prefix_randomly(DISTANCE_PREFIX, 100)

        if len(principal_street) != 0 or not self.check_is_empty(principal_street):
            # CREATING COMPONENT 1  --- [principal_street_prefix],[number_form],[principal_street] ---
            components.append(
                    principal_street_prefix + [[item, 'principal_street'] for item in
                                               principal_street.split()]
                )

        # DISTANCE COMPONENT
        if len(distance) != 0 or not self.check_is_empty(distance):
            add_specification_component = True if rm.randint(0, 100) > 80 else False
            if add_specification_component:
                add_num_component = True if rm.randint(0, 100) > 80 else False
                if add_num_component:
                    components.append(
                        distance_form + number_form + [[item, 'distance'] for item in
                                                       distance.split()]
                        + distance_specification_form
                    )
                else:
                    components.append(
                        distance_form + [[item, 'distance'] for item in
                                         distance.split()] + distance_specification_form
                    )
            else:
                add_num_component = True if rm.randint(0, 100) > 80 else False
                if add_num_component:
                    components.append(
                        distance_form + number_form + [[item, 'distance'] for item in
                                                       distance.split()]
                    )
                else:
                    components.append(
                        distance_form + [[item, 'distance'] for item in
                                         distance.split()]
                    )

        # Optional Component
        # INTERESTING PLACE COMPONENT
        add_interesting_place_component = True if rm.randint(0, 100) > 75 else False
        if add_interesting_place_component:
            interesting_place_name = str(rm.choice(self.data['interesting_place_name']))
            if len(interesting_place_name) != 0 or not self.check_is_empty(interesting_place_name):
                components.append(
                    [[item, 'interesting_place'] for item in
                     interesting_place_name.split()]
                )
        # omit administrative political divisions
        locality, municipality, province = super().omit_administrative_political(locality, municipality, province, 0.04,
                                                                                 0.02, 0.04)

        # permutation between components
        permutation_bool = rm.randint(1, 100) <= 10

        # Components Basics
        # LOCALITY COMPONENT
        if len(locality) != 0 or not self.check_is_empty(locality):
            between_prefix = [[',', 'rw']] if rm.randint(1, 100) < 70 and permutation_bool is False else []
            locality_form = super().generate_prefix_randomly(LOCALITY_PREFIX, 100)

            components.append(
                between_prefix + locality_form + [[item, 'locality'] for item in locality.split()]
            )

        # CREATING COMPONENT 4  --- [municipality_form],[municipality] ---
        if len(municipality) != 0 or not self.check_is_empty(municipality):
            between_prefix = [[',', 'rw']] if rm.randint(1, 100) < 70 and permutation_bool is False else []
            municipality_prefix = self.generate_prefix_randomly(MUNICIPALITY_PREFIX, 10)

            components.append(
                between_prefix + municipality_prefix + [[item, 'municipality'] for item in municipality.split()]
            )

        # CREATING COMPONENT 5  --- [province_form],[province] ---
        if len(province) != 0 or not self.check_is_empty(province):
            between_prefix = [[',', 'rw']] if rm.randint(1, 100) < 70 and permutation_bool is False else []
            province_prefix = self.generate_prefix_randomly(PROVINCE_PREFIX, 5)
            components.append(
                between_prefix + province_prefix + [[item, 'province'] for item in province.split()])

        return components




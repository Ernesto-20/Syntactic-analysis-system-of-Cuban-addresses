from pandas import DataFrame

import random as rm
import itertools as itt
import math
from src.tools.lookup import *
from noise_generator.generator_other_schema import Generator

from src.tools.correct_prefix import *


class NoiseGeneratorModelThree(Generator):

    def generate_noise(self, data_set: DataFrame, type=None, address_amount=None):
        '''

                :param data_set: this is the corpus for generate

                :param type: you can specify which kind of addresses examples you want to use it
                        example for using correct addresses  = "ce"
                        example for using almost correct addresses  = "ace"
                        example for using uncorrect addresses  = "uce"
                        example for using uncorrect addresses  = "eq"


                :param address_amount: this value indicates the amount of addresses this method will use

                :return: DataFrame
                '''

        self.address_amount = address_amount
        self.data = data_set
        self.type = type

        if self.type == 'ce':
            address_number = 0
            address_list = []
            words_list = []
            tag_list = []
            for _ in range(self.address_amount):
                components = self.__generate_correct_example_type_three()
                address_number += 1
                super().add_address(components, address_number, address_list, words_list, tag_list)

            return super().create_data_frame(address_list, words_list, tag_list)
        elif type == 'ace':
            address_number = 0
            address_list = []
            words_list = []
            tag_list = []

            for _ in range(self.address_amount):
                components = self.__generate_almost_correct_examples_type_three()
                address_number += 1
                super().add_address(components, address_number, address_list, words_list, tag_list)

            return super().create_data_frame(address_list, words_list, tag_list)
        elif type == 'uce':
            address_number = 0
            address_list = []
            words_list = []
            tag_list = []

            for _ in range(self.address_amount):
                components = self.__generate_uncorrect_examples_type_three()
                address_number += 1
                super().add_address(components, address_number, address_list, words_list, tag_list)

            return super().create_data_frame(address_list, words_list, tag_list)
        elif type == 'eq':
            return self.__generate_equilibrated_examples_type_three()
        elif type == 'ea':
            return self.__generate_evaluation_addresses()
        else:
            raise NotImplementedError('There is no such kind of example')

    def __generate_correct_example_type_three(self):
        components = []

        principal_street = str(rm.choice(self.data['principal_street']))
        distance = str(rm.randint(200, 800))
        interesting_place_name = str(rm.choice(self.data['interesting_place_name']))
        locality = str(rm.choice(self.data['locality']))
        municipality = str(rm.choice(self.data['municipality']))
        province = str(rm.choice(self.data['province']))

        principal_street_prefix = super().generate_prefix_randomly(STREET_NAME_PREFIX_CORRECT, 100)
        number_form = super().generate_prefix_randomly(PROPERTY_PREFIX_CORRECT, 100)
        distance_specification_form = super().generate_prefix_randomly(DISTANCE_SPECIFICATION_PREFIX_CORRECT, 100)
        distance_form = super().generate_prefix_randomly(DISTANCE_PREFIX_CORRECT, 100)
        locality_form = super().generate_prefix_randomly(LOCALITY_PREFIX_CORRECT, 100)
        municipality_form = super().generate_prefix_randomly(MUNICIPALITY_PREFIX_CORRECT, 100)
        province_form = super().generate_prefix_randomly(PROVINCE_PREFIX_CORRECT, 100)

        if len(principal_street) != 0 or not self.check_is_empty(principal_street):
            is_name = True if principal_street.isalpha() else False

            # CREATING COMPONENT 1  --- [principal_street_prefix],[number_form],[principal_street] ---
            if is_name:
                components.append(
                    principal_street_prefix + [[item, 'principal_street'] for item in
                                               principal_street.split()]
                )
            else:
                # Using the random number mentioned above
                # Add property prefix
                add_num_component = True if rm.randint(0, 100) > 70 else False
                if add_num_component:
                    components.append(
                        principal_street_prefix + number_form + [[item, 'principal_street'] for item in
                                                                 principal_street.split()]
                    )
                else:
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
            if len(interesting_place_name) != 0 or not self.check_is_empty(interesting_place_name):
                components.append(
                    [[item, 'interesting_place'] for item in
                     interesting_place_name.split()]
                )

        #  Permutación entre componentes.
        components = super().generate_non_standardization(components, 50)


        # Components Basics
        # LOCALITY COMPONENT
        if len(locality) != 0 or not self.check_is_empty(locality):
            components.append(
                locality_form + [[item, 'locality'] for item in locality.split()]
            )
        # CREATING COMPONENT 4  --- [municipality_form],[municipality] ---
        if len(municipality) != 0 or not self.check_is_empty(municipality):
            components.append(
                municipality_form + [[item, 'municipality'] for item in municipality.split()]
            )

        # CREATING COMPONENT 5  --- [province_form],[province] ---
        if len(province) != 0 or not self.check_is_empty(province):
            components.append(
                province_form + [[item, 'province'] for item in province.split()]
            )


        return components

    def __generate_almost_correct_examples_type_three(self):
        components = []

        principal_street = str(rm.choice(self.data['principal_street']))
        distance = str(rm.randint(200, 800))
        interesting_place_name = str(rm.choice(self.data['interesting_place_name']))
        locality = str(rm.choice(self.data['locality']))
        municipality = str(rm.choice(self.data['municipality']))
        province = str(rm.choice(self.data['province']))

        principal_street_prefix = super().generate_prefix_randomly(STREET_NAME_PREFIX, 80)
        number_form = super().generate_prefix_randomly(PROPERTY_PREFIX, 80)
        distance_specification_form = super().generate_prefix_randomly(DISTANCE_SPECIFICATION_PREFIX, 50)
        distance_form = super().generate_prefix_randomly(DISTANCE_PREFIX, 80)
        locality_form = super().generate_prefix_randomly(LOCALITY_PREFIX, 65)
        municipality_form = super().generate_prefix_randomly(MUNICIPALITY_PREFIX, 55)
        province_form = super().generate_prefix_randomly(PROVINCE_PREFIX, 55)

        if len(principal_street) != 0 or not self.check_is_empty(principal_street):
            is_name = True if principal_street.isalpha() else False

            # CREATING COMPONENT 1  --- [principal_street_prefix],[number_form],[principal_street] ---
            if is_name:
                components.append(
                    principal_street_prefix + [[item, 'principal_street'] for item in
                                               principal_street.split()]
                )
            else:
                # Using the random number mentioned above
                # Add property prefix
                add_num_component = True if rm.randint(0, 100) > 70 else False
                if add_num_component:
                    components.append(
                        principal_street_prefix + number_form + [[item, 'principal_street'] for item in
                                                                 principal_street.split()]
                    )
                else:
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
            if len(interesting_place_name) != 0 or not self.check_is_empty(interesting_place_name):
                components.append(
                    [[item, 'interesting_place'] for item in
                     interesting_place_name.split()]
                )

        #  Permutación entre componentes.
        components = super().generate_non_standardization(components, 50)


        # Components Basics
        # LOCALITY COMPONENT
        if len(locality) != 0 or not self.check_is_empty(locality):
            components.append(
                locality_form + [[item, 'locality'] for item in locality.split()]
            )
        # CREATING COMPONENT 4  --- [municipality_form],[municipality] ---
        if len(municipality) != 0 or not self.check_is_empty(municipality):
            components.append(
                municipality_form + [[item, 'municipality'] for item in municipality.split()]
            )

        # CREATING COMPONENT 5  --- [province_form],[province] ---
        if len(province) != 0 or not self.check_is_empty(province):
            components.append(
                province_form + [[item, 'province'] for item in province.split()]
            )



        return components

    def __generate_uncorrect_examples_type_three(self):
        components = []

        principal_street = str(rm.choice(self.data['principal_street']))
        distance = str(rm.randint(200, 800))
        interesting_place_name = str(rm.choice(self.data['interesting_place_name']))
        locality = str(rm.choice(self.data['locality']))
        municipality = str(rm.choice(self.data['municipality']))
        province = str(rm.choice(self.data['province']))

        principal_street_prefix = super().generate_prefix_randomly(STREET_NAME_PREFIX, 55)
        number_form = super().generate_prefix_randomly(PROPERTY_PREFIX, 55)
        distance_specification_form = super().generate_prefix_randomly(DISTANCE_SPECIFICATION_PREFIX, 55)
        distance_form = super().generate_prefix_randomly(DISTANCE_PREFIX, 55)
        place_form = super().generate_prefix_randomly(PLACE_PREFIX, 55)
        locality_form = super().generate_prefix_randomly(LOCALITY_PREFIX, 45)
        municipality_form = super().generate_prefix_randomly(MUNICIPALITY_PREFIX, 35)
        province_form = super().generate_prefix_randomly(PROVINCE_PREFIX, 35)

        if len(principal_street) != 0 or not self.check_is_empty(principal_street):
            is_name = True if principal_street.isalpha() else False

            # CREATING COMPONENT 1  --- [principal_street_prefix],[number_form],[principal_street] ---
            if is_name:
                components.append(
                    principal_street_prefix + [[item, 'principal_street'] for item in
                                               principal_street.split()]
                )
            else:
                # Using the random number mentioned above
                # Add property prefix
                add_num_component = True if rm.randint(0, 100) > 90 else False
                if add_num_component:
                    components.append(
                        principal_street_prefix + number_form + [[item, 'principal_street'] for item in
                                                                 principal_street.split()]
                    )
                else:
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
            if len(interesting_place_name) != 0 or not self.check_is_empty(interesting_place_name):
                components.append(
                    place_form + [[item, 'interesting_place'] for item in
                                  interesting_place_name.split()]
                )

        #  Permutación entre componentes.
        components = super().generate_non_standardization(components, 50)

        # Components Basics
        # LOCALITY COMPONENT
        if len(locality) != 0 or not self.check_is_empty(locality):
            components.append(
                locality_form + [[item, 'locality'] for item in locality.split()]
            )
        # CREATING COMPONENT 4  --- [municipality_form],[municipality] ---
        if len(municipality) != 0 or not self.check_is_empty(municipality):
            components.append(
                municipality_form + [[item, 'municipality'] for item in municipality.split()]
            )

        # CREATING COMPONENT 5  --- [province_form],[province] ---
        if len(province) != 0 or not self.check_is_empty(province):
            components.append(
                province_form + [[item, 'province'] for item in province.split()]
            )


        return components

    def __generate_equilibrated_examples_type_three(self):

        print('Generate_random_noise_type_three')
        address_number = 0
        address_list = []
        words_list = []
        tag_list = []

        correct, almost_correct, uncorrect = super().divide_equally(self.address_amount)
        for _ in range(correct):
            components = self.__generate_correct_example_type_three()
            address_number += 1
            self.add_address(components, address_number, address_list, words_list, tag_list)

        for _ in range(almost_correct):
            components = self.__generate_almost_correct_examples_type_three()
            address_number += 1
            self.add_address(components, address_number, address_list, words_list, tag_list)

        for _ in range(uncorrect):
            components = self.__generate_uncorrect_examples_type_three()
            address_number += 1
            self.add_address(components, address_number, address_list, words_list, tag_list)

        return self.create_data_frame(address_list, words_list, tag_list)

    def __generate_evaluation_addresses(self):
        print('Generate_random_noise_type_two')
        address_number = 0
        address_list = []
        dict_list = []

        correct, almost_correct, uncorrect = super().divide_equally(self.address_amount)

        for _ in range(correct):
            components = self.__generate_correct_example_type_three()
            string = self.components_to_string(components)
            dict_ = self.components_to_dict(components)
            address_list.append(string)
            dict_list.append(dict_)
            address_number += 1

        for _ in range(almost_correct):
            components = self.__generate_almost_correct_examples_type_three()
            string = self.components_to_string(components)
            dict_ = self.components_to_dict(components)
            address_list.append(string)
            dict_list.append(dict_)
            address_number += 1

        for _ in range(uncorrect):
            components = self.__generate_uncorrect_examples_type_three()
            string = self.components_to_string(components)
            dict_ = self.components_to_dict(components)
            address_list.append(string)
            dict_list.append(dict_)
            address_number += 1

        return self.create_dataframe(address_list, dict_list)
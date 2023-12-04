from pandas import DataFrame
from random import randrange
import random as rm
import itertools as itt
import math
import src.tools.lookup
from noise_generator.generator_other_schema import Generator

from src.tools.correct_prefix import *

class SchemeTwoNoiseGenerator(Generator):

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
            for index in range(self.address_amount):
                components = self.__generate_correct_example_type_two()
                address_number += 1
                self.add_address(components, address_number, address_list, words_list, tag_list)

            return self.create_data_frame(address_list, words_list, tag_list)
        elif type == 'ace':
            address_number = 0
            address_list = []
            words_list = []
            tag_list = []

            for index in range(self.address_amount):
                components = self.__generate_almost_correct_examples_type_two()
                address_number += 1
                self.add_address(components, address_number, address_list, words_list, tag_list)

            return self.create_data_frame(address_list, words_list, tag_list)
        elif type == 'uce':
            address_number = 0
            address_list = []
            words_list = []
            tag_list = []

            for index in range(self.address_amount):
                components = self.__generate_uncorrect_examples_type_two()
                address_number += 1
                super().add_address(components, address_number, address_list, words_list, tag_list)

            return super().create_data_frame(address_list, words_list, tag_list)
        elif type == 'eq':
            return self.__generate_equilibrated_examples_type_two()
        elif type == 'ea':
            return self.__generate_evaluation_addresses()
        else:
            raise NotImplementedError('There is no such kind of example')

    def __generate_equilibrated_examples_type_two(self):

        print('Generate_random_noise_type_two')
        address_number = 0
        address_list = []
        words_list = []
        tag_list = []

        correct, almost_correct, uncorrect = super().divide_equally(self.address_amount)

        for _ in range(correct):
            components = self.__generate_correct_example_type_two()
            address_number += 1
            super().add_address(components, address_number, address_list, words_list, tag_list)

        for _ in range(almost_correct):
            components = self.__generate_almost_correct_examples_type_two()
            address_number += 1
            super().add_address(components, address_number, address_list, words_list, tag_list)

        for _ in range(uncorrect):
            components = self.__generate_uncorrect_examples_type_two()
            address_number += 1
            super().add_address(components, address_number, address_list, words_list, tag_list)

        return super().create_data_frame(address_list, words_list, tag_list)

    def __generate_correct_example_type_two(self):
        components = []

        building = super().create_building_syntetic()
        locality = str(rm.choice(self.data['locality']))
        municipality = str(rm.choice(self.data['municipality']))
        province = str(rm.choice(self.data['province']))

        building_form = self.generate_prefix_randomly(BUILDING_PREFIX_CORRECT, 100)
        number_form = self.generate_prefix_randomly(PROPERTY_PREFIX_CORRECT, 100)
        apartment_form = self.generate_prefix_randomly(APARTMENT_PREFIX_CORRECT, 100)
        zone_form = self.generate_prefix_randomly(ZONE_PREFIX_CORRECT, 100)
        locality_form = self.generate_prefix_randomly(LOCALITY_PREFIX_CORRECT, 100)
        municipality_prefix = self.generate_prefix_randomly(MUNICIPALITY_PREFIX_CORRECT, 100)
        province_prefix = self.generate_prefix_randomly(PROVINCE_PREFIX_CORRECT, 100)

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
            apartment_num = self.create_apartment_syntetic()

            add_num_component = True if rm.randint(0, 100) > 50 else False
            if add_num_component:
                components.append(
                    apartment_form + number_form + [[item, 'apartment'] for item in
                                                    apartment_num.split()]
                )
            else:
                components.append(
                    apartment_form + [[item, 'apartment'] for item in
                                      apartment_num.split()]
                )

        # CREATING COMPONENT 3  --- [locality_form],[locality] ---
        if locality != '':
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
                                locality_form + [[item, 'locality'] for item in loc_aux.split()] + zone_form + [
                                    [item, 'locality'] for item in
                                    loc_zone.split()]
                            )
                        else:
                            components.append(
                                zone_form + [[item, 'locality'] for item in loc_zone.split()]
                                + locality_form + [[item, 'locality'] for item in loc_aux.split()]
                            )

                    else:
                        add_num_component = True if rm.randint(0, 100) > 50 else False
                        if add_num_component:
                            if rm.randint(0, 50) > 25:
                                components.append(
                                    locality_form + [[item, 'locality'] for item in loc_aux.split()]
                                    + zone_form + number_form + [[item, 'locality'] for item in
                                                                 loc_zone.split()]
                                )
                            else:
                                components.append(
                                    zone_form + number_form + [[item, 'locality'] for item in loc_zone.split()]
                                    + locality_form + [[item, 'locality'] for item in loc_aux.split()]
                                )

                        else:
                            if rm.randint(0, 50) > 25:
                                components.append(
                                    locality_form + [[item, 'locality'] for item in loc_aux.split()] + zone_form + [
                                        [item, 'locality'] for item in
                                        loc_zone.split()]
                                )
                            else:
                                components.append(
                                    zone_form + [[item, 'locality'] for item in loc_zone.split()]
                                    + locality_form + [[item, 'locality'] for item in loc_aux.split()]
                                )
                else:
                    components.append(
                        locality_form + [[item, 'locality'] for item in locality.split()]
                    )
            else:
                components.append(
                    locality_form + [[item, 'locality'] for item in locality.split()]
                )

        # CREATING COMPONENT 4  --- [municipality_form],[municipality] ---
        if len(municipality) != 0 or not self.check_is_empty(municipality):
            components.append(
                municipality_prefix + [[item, 'municipality'] for item in municipality.split()]
            )

        # CREATING COMPONENT 5  --- [province_form],[province] ---
        if len(province) != 0 or not self.check_is_empty(province):
            components.append(
                province_prefix + [[item, 'province'] for item in province.split()]
            )

            #  Permutación entre componentes.
            components = self.generate_non_standardization(components, 30)

        return components

    def __generate_almost_correct_examples_type_two(self):
        components = []

        building = super().create_building_syntetic()
        locality = str(rm.choice(self.data['locality']))
        municipality = str(rm.choice(self.data['municipality']))
        province = str(rm.choice(self.data['province']))

        building_form = super().generate_prefix_randomly(src.tools.lookup.BUILDING_PREFIX, 70)
        number_form = super().generate_prefix_randomly(src.tools.lookup.PROPERTY_PREFIX, 70)
        apartment_form = super().generate_prefix_randomly(src.tools.lookup.APARTMENT_PREFIX, 70)
        zone_form = super().generate_prefix_randomly(src.tools.lookup.ZONE_PREFIX, 60)
        locality_form = super().generate_prefix_randomly(src.tools.lookup.LOCALITY_PREFIX, 60)
        municipality_prefix = super().generate_prefix_randomly(src.tools.lookup.MUNICIPALITY_PREFIX, 60)
        province_prefix = super().generate_prefix_randomly(src.tools.lookup.PROVINCE_PREFIX, 40)

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
            apartment_num = super().create_apartment_syntetic()

            # para variante num, letra+num
            add_num_component = True if rm.randint(0, 100) > 50 else False
            if add_num_component:
                components.append(
                    apartment_form + number_form + [[item, 'apartment'] for item in
                                                    apartment_num.split()]
                )
            else:
                components.append(
                    apartment_form + [[item, 'apartment'] for item in
                                      apartment_num.split()]
                )

        # CREATING COMPONENT 3  --- [locality_form],[locality] ---
        if not self.check_is_empty(locality):
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
                                locality_form + [[item, 'locality'] for item in loc_aux.split()] + zone_form + [
                                    [item, 'locality'] for item in
                                    loc_zone.split()]
                            )
                        else:
                            components.append(
                                zone_form + [[item, 'locality'] for item in loc_zone.split()]
                                + locality_form + [[item, 'locality'] for item in loc_aux.split()]
                            )

                    else:
                        add_num_component = True if rm.randint(0, 100) > 50 else False
                        if add_num_component:
                            if rm.randint(0, 50) > 25:
                                components.append(
                                    locality_form + [[item, 'locality'] for item in loc_aux.split()]
                                    + zone_form + number_form + [[item, 'locality'] for item in
                                                                 loc_zone.split()]
                                )
                            else:
                                components.append(
                                    zone_form + number_form + [[item, 'locality'] for item in loc_zone.split()]
                                    + locality_form + [[item, 'locality'] for item in loc_aux.split()]
                                )

                        else:
                            if rm.randint(0, 50) > 25:
                                components.append(
                                    locality_form + [[item, 'locality'] for item in loc_aux.split()] + zone_form + [
                                        [item, 'locality'] for item in
                                        loc_zone.split()]
                                )
                            else:
                                components.append(
                                    zone_form + [[item, 'locality'] for item in loc_zone.split()]
                                    + locality_form + [[item, 'locality'] for item in loc_aux.split()]
                                )
                else:
                    components.append(
                        locality_form + [[item, 'locality'] for item in locality.split()]
                    )
            else:
                components.append(
                    locality_form + [[item, 'locality'] for item in locality.split()]
                )

        # CREATING COMPONENT 4  --- [municipality_form],[municipality] ---
        if len(municipality) != 0 or not self.check_is_empty(municipality):
            components.append(
                municipality_prefix + [[item, 'municipality'] for item in municipality.split()]
            )

        # CREATING COMPONENT 5  --- [province_form],[province] ---
        if len(province) != 0 or not self.check_is_empty(province):
            components.append(
                province_prefix + [[item, 'province'] for item in province.split()]
            )

            #  Permutación entre componentes.
            components = super().generate_non_standardization(components, 40)

        return components

    def __generate_uncorrect_examples_type_two(self):
        components = []

        building = super().create_building_syntetic()
        locality = str(rm.choice(self.data['locality']))
        municipality = str(rm.choice(self.data['municipality']))
        province = str(rm.choice(self.data['province']))

        building_form = super().generate_prefix_randomly(src.tools.lookup.BUILDING_PREFIX, 55)
        number_form = super().generate_prefix_randomly(src.tools.lookup.PROPERTY_PREFIX, 55)
        apartment_form = super().generate_prefix_randomly(src.tools.lookup.APARTMENT_PREFIX, 55)
        zone_form = super().generate_prefix_randomly(src.tools.lookup.ZONE_PREFIX, 45)
        locality_form = super().generate_prefix_randomly(src.tools.lookup.LOCALITY_PREFIX, 45)
        municipality_prefix = super().generate_prefix_randomly(src.tools.lookup.MUNICIPALITY_PREFIX, 35)
        province_prefix = super().generate_prefix_randomly(src.tools.lookup.PROVINCE_PREFIX, 35)

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
            apartment_num = super().create_apartment_syntetic()

            # para variante num, letra+num
            add_num_component = True if rm.randint(0, 100) > 50 else False
            if add_num_component:
                components.append(
                    apartment_form + number_form + [[item, 'apartment'] for item in
                                                    apartment_num.split()]
                )
            else:
                components.append(
                    apartment_form + [[item, 'apartment'] for item in
                                      apartment_num.split()]
                )

        # CREATING COMPONENT 3  --- [locality_form],[locality] ---
        if locality != '':
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
                                locality_form + [[item, 'locality'] for item in loc_aux.split()] + zone_form + [
                                    [item, 'locality'] for item in
                                    loc_zone.split()]
                            )
                        else:
                            components.append(
                                zone_form + [[item, 'locality'] for item in loc_zone.split()]
                                + locality_form + [[item, 'locality'] for item in loc_aux.split()]
                            )

                    else:
                        add_num_component = True if rm.randint(0, 100) > 50 else False
                        if add_num_component:
                            if rm.randint(0, 50) > 25:
                                components.append(
                                    locality_form + [[item, 'locality'] for item in loc_aux.split()]
                                    + zone_form + number_form + [[item, 'locality'] for item in
                                                                 loc_zone.split()]
                                )
                            else:
                                components.append(
                                    zone_form + number_form + [[item, 'locality'] for item in loc_zone.split()]
                                    + locality_form + [[item, 'locality'] for item in loc_aux.split()]
                                )

                        else:
                            if rm.randint(0, 50) > 25:
                                components.append(
                                    locality_form + [[item, 'locality'] for item in loc_aux.split()] + zone_form + [
                                        [item, 'locality'] for item in
                                        loc_zone.split()]
                                )
                            else:
                                components.append(
                                    zone_form + [[item, 'locality'] for item in loc_zone.split()]
                                    + locality_form + [[item, 'locality'] for item in loc_aux.split()]
                                )
                else:
                    components.append(
                        locality_form + [[item, 'locality'] for item in locality.split()]
                    )
            else:
                components.append(
                    locality_form + [[item, 'locality'] for item in locality.split()]
                )

        # CREATING COMPONENT 4  --- [municipality_form],[municipality] ---
        if len(municipality) != 0 or not self.check_is_empty(municipality):
            components.append(
                municipality_prefix + [[item, 'municipality'] for item in municipality.split()]
            )

        # CREATING COMPONENT 5  --- [province_form],[province] ---
        if len(province) != 0 or not self.check_is_empty(province):
            components.append(
                province_prefix + [[item, 'province'] for item in province.split()]
            )

        #  Permutación entre componentes.
        components = super().generate_non_standardization(components, 40)

        return components

    def __generate_evaluation_addresses(self):
        print('Generate_random_noise_type_two')
        address_number = 0
        address_list = []
        dict_list = []

        correct, almost_correct, uncorrect = super().divide_equally(self.address_amount)

        for _ in range(correct):
            components = self.__generate_correct_example_type_two()
            string = self.components_to_string(components)
            dict_ = self.components_to_dict(components)
            address_list.append(string)
            dict_list.append(dict_)
            address_number += 1

        for _ in range(almost_correct):
            components = self.__generate_almost_correct_examples_type_two()
            string = self.components_to_string(components)
            dict_ = self.components_to_dict(components)
            address_list.append(string)
            dict_list.append(dict_)
            address_number += 1

        for _ in range(uncorrect):
            components = self.__generate_uncorrect_examples_type_two()
            string = self.components_to_string(components)
            dict_ = self.components_to_dict(components)
            address_list.append(string)
            dict_list.append(dict_)
            address_number += 1

        return self.create_dataframe(address_list, dict_list)



from pandas import DataFrame
import random as rm


from src.data_realism_converter.noise_generator import NoiseGenerator

from src.tools.lookup import *


class PDModelTypeSelector(NoiseGenerator):
    def generate_noise(self, data_set: DataFrame, type=None, address_amount=None):
        '''

        :param data_set: this is the corpus for generate

        :param type: you can specify which model you want to use it
                Example for using address model based on buildings type = "build"
                example for using address model based on distances type = "dist"
        :param address_amount: this value indicates the amount of addresses this method will use
                IMPORTANTE: In case of establishing a value greater than the amount of data entered,
                            after that number they begin to be generated randomly
        :return: DataFrame
        '''
        self.address_amount = address_amount
        self.data = data_set
        self.type = type

        if self.type == 'build' and address_amount==None:
            return self.__generate_noise_type_two()
        elif self.type == 'build':
            return self.__generate_random_noise_type_two(address_amount)
        elif type == 'dist':
            return self.__generate_random_noise_type_three(address_amount)
        else:
            raise NotImplementedError('There is no such cleaning method')


    def __generate_noise_type_two(self):

        print('Generate_noise_type_two')
        address_number = 0
        address_list = []
        words_list = []
        tag_list = []


        for index,row in self.data.iterrows():

            components = []

            building = str(row['building'])
            locality = str(row['locality'])
            municipality = str(row['municipality'])
            province = str(row['province'])

            building_form = super().generate_prefix_randomly(BUILDING_PREFIX, 55)
            number_form = super().generate_prefix_randomly(PROPERTY_PREFIX, 55)
            apartment_form = super().generate_prefix_randomly(APARTMENT_PREFIX, 55)
            zone_form = super().generate_prefix_randomly(ZONE_PREFIX, 45)
            locality_form = super().generate_prefix_randomly(LOCALITY_PREFIX, 45)
            municipality_prefix = super().generate_prefix_randomly(MUNICIPALITY_PREFIX, 35)
            province_prefix = super().generate_prefix_randomly(PROVINCE_PREFIX, 35)

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
                apartment_num = self.__generate_apartment_syntetic()

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
            if len(municipality) != 0 or not self.__is_empty(municipality):
                components.append(
                    municipality_prefix + [[item, 'municipality'] for item in municipality.split()]
                )

            # CREATING COMPONENT 5  --- [province_form],[province] ---
            if len(province) != 0 or not self.__is_empty(province):
                components.append(
                    province_prefix + [[item, 'province'] for item in province.split()]
                )

                #  Permutación entre componentes.
                components = super().generate_non_standardization(components)
                print(components)

                address_number += 1
                self.__add_new_address(components, address_number, address_list, words_list, tag_list)

                #  Generar ruido gramatical.

            return self.__generate_data_frame(address_list, words_list, tag_list)

    def __generate_random_noise_type_two(self, address_amount=None):

        print('Generate_random_noise_type_two')
        address_number = 0
        address_list = []
        words_list = []
        tag_list = []

        for index in range(address_amount):

            components = []

            building = self.__generate_building_syntetic()
            locality = str(rm.choice(self.data['locality']))
            municipality = str(rm.choice(self.data['municipality']))
            province = str(rm.choice(self.data['province']))

            building_form = super().generate_prefix_randomly(BUILDING_PREFIX, 55)
            number_form = super().generate_prefix_randomly(PROPERTY_PREFIX, 55)
            apartment_form = super().generate_prefix_randomly(APARTMENT_PREFIX, 55)
            zone_form = super().generate_prefix_randomly(ZONE_PREFIX, 45)
            locality_form = super().generate_prefix_randomly(LOCALITY_PREFIX, 45)
            municipality_prefix = super().generate_prefix_randomly(MUNICIPALITY_PREFIX, 35)
            province_prefix = super().generate_prefix_randomly(PROVINCE_PREFIX, 35)

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
                apartment_num = self.__generate_apartment_syntetic()

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
            if len(municipality) != 0 or not self.__is_empty(municipality):
                components.append(
                    municipality_prefix + [[item, 'municipality'] for item in municipality.split()]
                )

            # CREATING COMPONENT 5  --- [province_form],[province] ---
            if len(province) != 0 or not self.__is_empty(province):
                components.append(
                    province_prefix + [[item, 'province'] for item in province.split()]
                )

                #  Permutación entre componentes.
                components = super().generate_non_standardization(components)
                print(components)

                address_number += 1
                self.__add_new_address(components, address_number, address_list, words_list, tag_list)

                #  Generar ruido gramatical.

            return self.__generate_data_frame(address_list, words_list, tag_list)

    def __generate_random_noise_type_three(self, address_amount=10000):
        print('Generate Noise II -- Type One')
        address_number = 0
        address_list = []
        words_list = []
        tag_list = []

        for index in range(address_amount):
            if address_amount is not None and address_number == address_amount:
                break
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


            if len(principal_street) != 0 or not self.__is_empty(principal_street):
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
                            principal_street_prefix + ' ' + number_form + ' ' + [[item, 'principal_street'] for item in
                                                                       principal_street.split()]
                        )
                    else:
                        components.append(
                            principal_street_prefix + [[item, 'principal_street'] for item in
                                                       principal_street.split()]
                        )
            # DISTANCE COMPONENT
            if len(distance) != 0 or not self.__is_empty(distance):
                add_specification_component = True if rm.randint(0, 100) > 80 else False
                if add_specification_component:
                    add_num_component = True if rm.randint(0, 100) > 80 else False
                    if add_num_component:
                        components.append(
                            distance_form + ' ' + number_form + ' ' + [[item, 'distance'] for item in
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
                            distance_form + ' ' + number_form + ' ' + [[item, 'distance'] for item in
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
                if len(interesting_place_name) != 0 or not self.__is_empty(interesting_place_name):
                    components.append(
                    place_form + [[item, 'interesting_place'] for item in
                              interesting_place_name.split()]
                    )


            # Components Basics
            #LOCALITY COMPONENT
            if len(locality) != 0 or not self.__is_empty(locality):
                components.append(
                    locality_form + [[item, 'locality'] for item in locality.split()]
                )
            # CREATING COMPONENT 4  --- [municipality_form],[municipality] ---
            if len(municipality) != 0 or not self.__is_empty(municipality):
                components.append(
                    municipality_form + [[item, 'municipality'] for item in municipality.split()]
                )

            # CREATING COMPONENT 5  --- [province_form],[province] ---
            if len(province) != 0 or not self.__is_empty(province):
                components.append(
                    province_form + [[item, 'province'] for item in province.split()]
                )

            #  Permutación entre componentes.
            components = super().generate_non_standardization(components)
            print(components)

            address_number += 1
            self.__add_new_address(components, address_number, address_list, words_list, tag_list)



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
        amount_errors = var_aleatory if rm.randint(0, 2) == 1 else 0
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
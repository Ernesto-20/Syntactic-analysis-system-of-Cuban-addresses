import math
import string

from pandas import DataFrame
import random as rm
import itertools as itt

from src.data_realism_converter.noise_generator import NoiseGenerator

from src.tools.lookup import *


class PDModelTypeTwo(NoiseGenerator):
    def generate_noise(self, data_set: DataFrame):

        print('Generate some noise -- Type Two')
        address_number = 0
        address_list = []
        words_list = []
        tag_list = []

        for line in data_set.index:

            dictAddress = {}
            components = []

            building = str(data_set.iloc[line, 0])
            locality = str(data_set.iloc[line, 2])
            municipality = str(data_set.iloc[line, 4])
            province = str(data_set.iloc[line, 6])

            # For creating the first component we have to split itself in three sub-components, if the name of the building is alphanum
            # For example: Edif 456 o 34B
            # [reserved word for building]+ [reserved word for number] + [number]
            # then a random number is used to decide whether or not the number component appears
            # And if it's alpha would be like:
            # [reserved word for building] + [name]

            is_name = True if building.isalpha() else False

            # CREATING COMPONENT 1  --- [building_form],[number_form],[building] ---
            if is_name:
                building_form = self.__generate_type_reserved_word(RW_BUILDING, components, 20)
                component_1_str = building_form + ' ' + building
                components += [[item, 'building'] for item in building.split()]
                dictAddress[component_1_str] = components

            else:
                # Using the random number mentioned above

                add_num_component = True if rm.randint(0, 100) > 90 else False
                if add_num_component:
                    building_form = self.__generate_type_reserved_word(RW_BUILDING, components, 20)
                    number_form = self.__generate_type_reserved_word(RW_NUMBER, components, 20)
                    component_1_str = building_form + ' ' + number_form + ' ' + building
                    components += [[item, 'building'] for item in building.split()]
                    dictAddress[component_1_str] = components
                else:
                    building_form = self.__generate_type_reserved_word(RW_BUILDING, components, 20)
                    component_1_str = building_form + ' ' + building
                    components += [[item, 'building'] for item in building.split()]
                    dictAddress[component_1_str] = components

            # CREATING COMPONENT 2  --- [apartment_form],[number_form],[apartment] ---
            # This component is optional
            components = []
            component_2_str = ''

            add_apart_component = rm.randint(0, 100)
            if add_apart_component > 50:
                apartment_num = rm.randint(0, 101)

                add_num_component = True if rm.randint(0, 100) > 90 else False
                if add_num_component:

                    apartment_form = self.__generate_type_reserved_word(RW_APARTMENT_2, components, 10)
                    number_form = self.__generate_type_reserved_word(RW_NUMBER, components, 20)
                    components += [[item, 'apartment'] for item in str(apartment_num).split()]
                    component_2_str += ' ' + apartment_form + ' ' + number_form + ' ' + str(apartment_num)
                    dictAddress[component_2_str] = components

                else:
                    apartment_form = self.__generate_type_reserved_word(RW_APARTMENT_2, components, 10)

                    components += [[item, 'apartment'] for item in str(apartment_num).split()]
                    component_2_str += ' ' + apartment_form + ' ' + str(apartment_num)
                    dictAddress[component_2_str] = components

            # CREATING COMPONENT 3  --- [locality_form],[locality] ---
            components = []
            component_3_str = ''
            if locality != '':
                loc_aux = ''
                loc_zone = ''
                if locality.lower().find('alamar') != -1:
                    spl_loc = locality.split()
                    if len(spl_loc) != 1:
                        loc_aux = 'Alamar'
                        for word in spl_loc:
                            if word.lower() != 'alamar':
                                loc_zone += word
                        # Adding the zone
                        zone_form = self.__generate_type_reserved_word(RW_ZONE, components, 14)
                        locality_form = self.__generate_type_reserved_word(RW_LOCALITY, components, 14)
                        number_form = self.__generate_type_reserved_word(RW_NUMBER, components, 20)
                        components += [[item, 'locality'] for item in loc_zone.split()]
                        if loc_zone.lower().find('micro') != -1:
                            zone = zone_form + ' ' + loc_zone
                        else:
                            zone = zone_form + ' ' + number_form + ' ' + loc_zone

                        if rm.randint(0, 50) > 25:
                            component_3_str = locality_form + ' ' + loc_aux + ' ' + zone
                            components += [[item, 'locality'] for item in loc_aux.split()]
                            dictAddress[component_3_str] = components
                        else:
                            component_3_str = zone + ' ' + locality_form + ' ' + loc_aux
                            components += [[item, 'locality'] for item in loc_aux.split()]
                            dictAddress[component_3_str] = components

                    else:
                        component_3_str = self.__generate_type_reserved_word(RW_LOCALITY, components, 14)
                        components += [[item, 'locality'] for item in locality.split()]
                        component_3_str += locality
                        dictAddress[component_3_str] = components

                else:
                    component_3_str = self.__generate_type_reserved_word(RW_LOCALITY, components, 14)
                    components += [[item, 'locality'] for item in locality.split()]
                    component_3_str += locality
                    dictAddress[component_3_str] = components

            # CREATING COMPONENT 4  --- [municipality_form],[municipality] ---
            municipality_form = self.__generate_type_reserved_word(RW_MUNICIPALITY, components, 20)
            components = [[item, 'municipality'] for item in municipality.split()]
            component_4_str = municipality_form + ' '+ municipality
            dictAddress[component_4_str] = components

            # CREATING COMPONENT 5  --- [province_form],[province] ---
            province_form = self.__generate_type_reserved_word(RW_PROVINCE, components, 20)
            components = [[item, 'province'] for item in province.split()]
            component_5_str = province_form + ' '+ province
            dictAddress[component_5_str] = components

            datasAddress = [component_1_str]
            if component_2_str != '':
                datasAddress += [component_2_str]
            datasAddress += [component_3_str, component_4_str, component_5_str]
            permutations = list(itt.permutations(datasAddress))

            amount_permutation = math.factorial(len(datasAddress)) - 1
            datasAddress = permutations[rm.randint(0, amount_permutation)]

            result_list = []
            for item in datasAddress:
                result_list += dictAddress[item]

            address_number += 1
            self.__add_address(result_list, address_number, address_list, words_list, tag_list)

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

    def __generate_type_reserved_word(self, types, rw_list, top):
        """ Randomly generates a street type and assigns it to the list.

            param rw_list: List of components of an address

            param top: integer indicating a probability margin for not choosing any type.
            As top increases, the probability of not choosing a street type increases.

            :return: The list with the new street type incorporated if it was the case, otherwise, it is returned unchanged.
            In addition, the type of street is returned if it has been generated.
        """
        num_random = rm.randint(0, top)
        amount_types = len(types)
        noise_type = ''

        # Creating and adding the street type
        noise_type = types[amount_types - 1 if num_random >= amount_types - 1 else num_random]
        rw_list += [[item, 'rw'] for item in noise_type.split()]

        noise_type = ' ' + noise_type

        return noise_type

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

    def __generate_write_error(word):
        """ This function randomly generates a write error given a word entered by parameter,
            the types of errors established,(with their range) were:

            -Omission of characters(0-20)
            -Spelling mistake(20-45)
            -Addition of other characters(45-50)
            -character duplication(50-60)
          ** if the value is -1, the word is returned in its original state

        :param word: string that will be subjected to the error generation process

        :return: string with write error
        """
        error_value = rm.randint(-2, 60)
        if word != '' or word != ' ':
            # Character Omission
            if error_value in range(0, 20):
                o_index = rm.randint(len(word))
                return word[:o_index] + '' + word[o_index + 1:]
            # Spelling Mistakes
            elif error_value in range(20, 45):
                return word
            # Addition of other characters
            elif error_value in range(45, 50):
                char_list = string.printable[10: 62] # This range corresponds only to alphabetic characters
                random_char = rm.randint(len(char_list))
                r_index = rm.randint(len(word))
                char_added = char_list[random_char]
                return word[:r_index] + '' + char_added + '' + word[r_index:]
            # Character duplication
            elif error_value in range(50, 60):
                r_index = rm.randint(len(word))
                return word[:r_index] + '' + word[r_index] + '' + word[r_index:]









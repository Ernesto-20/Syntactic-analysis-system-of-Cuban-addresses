import math
from abc import ABC, abstractmethod
from random import randrange
from random import choice
import itertools as itt
import random as rm

import numpy as np
import pandas as pd
from pandas import DataFrame

class Generator(ABC):
    @abstractmethod
    def generate_noise(self):
        pass

    def generate_non_standardization(self, components,probability):
        reorder_components = components

        if rm.randint(1, 100) <= probability:
            permutations = list(itt.permutations(components))

            amount_permutation = math.factorial(len(components)) - 1
            reorder_components = permutations[rm.randint(0, amount_permutation)]

        return reorder_components

    def generate_prefix_randomly(self, list_prefix, probability):
        if rm.randint(1, 100) <= probability:
            prefix = list_prefix[rm.randint(0, len(list_prefix) - 1)]
            return [[item, 'rw'] for item in prefix.split()]
        return []

    def generate_suffix_randomly(self, list_suffix, probability):
        if rm.randint(1, 100) <= probability:
            suffix = list_suffix[rm.randint(0, len(list_suffix) - 1)]
            return [[item, 'rw'] for item in suffix.split()]
        return []

    def omit_administrative_political(self, locality, municipality, province, loc_probability, mun_probability, prov_probability):

        if rm.randint(1, 100) <= loc_probability:
            province = ''
        if rm.randint(1, 100) <= mun_probability:
            municipality = ''
        if rm.randint(1, 100) <= prov_probability:
            locality = ''

        return locality, municipality, province

    def generate_spelling_errors(self, word):
        apply_value = randrange(100)
        if apply_value > 65:
            rand = randrange(100)
            if rand < 25:
                # Duplicate character
                word = self._duplicate_character(word)
            elif rand < 50 and len(word) > 2:
                # Omit character
                word = self._omit_character(word)
            else:
                # Replace similar character
                word = self._similar_character(word)

        return word

    def _duplicate_character(self, word):
        char_index = randrange(len(word))
        return word[:char_index] + word[char_index] + word[char_index:]

    def _omit_character(self, word):
        char_index = randrange(len(word))
        return word[:char_index] + word[char_index + 1:]

    def _similar_character(self, word):
        ret_word = word
        char_index = randrange(len(word))
        similar_chars = {'a': 'e', 'e': 'a', 'i': 'l', 'l': 'i', 'o': 'u', 'u': 'o', 'a': '@', '0': '@', 'm': 'n',
                         'n': 'm',
                         'b': 'v', 's': 'z', 'v': 'b', 'z': 's'}
        if word[char_index].lower() in similar_chars:
            new_char = similar_chars[word[char_index].lower()]
            ret_word = word[:char_index] + new_char + word[char_index + 1:]

        return ret_word

    def divide_equally(self,number):
        part = number // 3
        remainder = number % 3
        if remainder == 0:
            return part, part, part
        elif remainder == 1:
            return part + 1, part, part
        else:
            return part + 1, part , part + 1


    def create_data_frame(self, address_list, words_list, tags_list):
        return DataFrame({
            'Sentence #': address_list,
            'Word': words_list,
            'Tag': tags_list
        })

    def add_address(self, components, address_number, address_list, words_list, tags_list):
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
                    word = self.generate_spelling_errors(word)

                words_list.append(word)
                tags_list.append(str(compound_items[1]))

                if count != 0 and len(words_list) == len(address_list) + 1:
                    address_list.append(None)
            count += 1

    def check_is_empty(self, entity):

        return len(entity) == 0 or len(entity.split()) == 0 or entity == 'nan' or entity is None

    def create_building_syntetic(self):
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
            temp = rm.randint(1, 100)
            if temp <= 90:
                # one letter
                return letters[rm.randint(1, len(letters) - 1)]
            else:
                # two letters
                return letters[rm.randint(1, len(letters) - 1)] + letters[rm.randint(1, len(letters) - 1)]

        else:
            #  numbers and letters
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'R', 'S', 'T']
            letter = letters[rm.randint(1, len(letters) - 1)]
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
            else:
                number = str(rm.randint(10000, 99999))

            letter_position = rm.randint(0, len(number)-1)
            building_name = number[0: letter_position] + letter + number[letter_position:]

            # two letter
            if rm.randint(1, 100) < 5:
                letter = letters[rm.randint(0, len(letters) - 1)]
                letter_position = rm.randint(0, len(number) - 1)
                building_name = building_name[0: letter_position] + letter + building_name[letter_position:]

            return building_name

    def create_apartment_syntetic(self):
        random_value = rm.randint(1, 100)
        if random_value <= 50:
            # only numbers
            return str(rm.randint(10, 101))
        elif random_value <= 75:
            # only letters
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'R', 'S', 'T']
            return letters[rm.randint(1, len(letters) - 1)]
        else:
            #  numbers and letters
            letters = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'R', 'S', 'T']
            letter = letters[rm.randint(1, len(letters) - 1)]
            letter_position = rm.randint(1, 2)
            number = str(rm.randint(1, 90))

            return number[0: letter_position] + letter + number[letter_position:]

    def components_to_string(self,components):
        result = []
        for component in components:
            for subcomponent in component:
                word, tag = subcomponent
                result.append(f"{word}")
        return ' '.join(result)

    def components_to_dict(self, components):
          result_dict = {}
          for component in components:
              for subcomponent in component:
                  word, tag = subcomponent
                  if tag not in result_dict:
                      result_dict[tag] = []
                  result_dict[tag].append(str(word).lower())
          return result_dict

    def create_dataframe(self, string_list, dict_list):
        # Crear un DataFrame vacío con las columnas correspondientes a las claves del primer diccionario en dict_list y una columna adicional para la cadena de caracteres

        df = pd.DataFrame(columns=['full_address'] + list(dict_list[0].keys()))
         # Añadir cada cadena y cada diccionario en dict_list como una nueva fila en el DataFrame
        for string, dict_ in zip(string_list, dict_list):

            # df = df.append(pd.Series(row, index=df.columns), ignore_index=True)
            #  df = pd.concat([df, pd.DataFrame([dict_], columns=columns + ['string'])])
            df = pd.concat([df, pd.DataFrame([{'full_address': string, **dict_}])])

        columns_to_clean = list(dict_list[0].keys())
        for column in columns_to_clean:
            #df[column] = df[column].apply(lambda x: str(x).strip("[]'"))
            df[column] = df[column].replace(r'^\s*$', np.nan, regex=True)

        return df

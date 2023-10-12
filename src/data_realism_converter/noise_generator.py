from abc import abstractmethod, ABC
from random import randrange
from random import choice
import itertools as itt
import math
import random as rm

from pandas import DataFrame
# from spellchecker import SpellChecker
# from fuzzywuzzy import fuzz


class NoiseGenerator(ABC):
    @abstractmethod
    def generate_noise(self):
        pass

    def generate_non_standardization(self, components):
        permutations = list(itt.permutations(components))

        amount_permutation = math.factorial(len(components)) - 1
        reorder_components = permutations[rm.randint(0, amount_permutation)]

        return reorder_components


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

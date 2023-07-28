from random import randrange
from random import choice
import itertools as itt
import math
import random as rm
from spellchecker import SpellChecker
from fuzzywuzzy import fuzz


class Generator:
    def __init__(self):
        rm.seed(155)
    def generate_non_standardization(self, components):
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

    def generate_spelling_errors(self, word):
        apply_value = randrange(100)
        if apply_value > 65:
            rand = randrange(100)
            if rand < 25:
                # Duplicate character
                word = self.__duplicate_character(word)
            elif rand < 50 and len(word) > 1:
                # Omit character
                word = self.__omit_character(word)
            # elif rand < 75:
                # Misspelling
                # To fix this function
                # word = self.__misspelling(word)
            else:
                # Replace similar character
                word = self.__similar_character(word)

        return word



    def __duplicate_character(self, word):
        char_index = randrange(len(word))
        return word[:char_index] + word[char_index] + word[char_index:]

    def __omit_character(self,word):
        char_index = randrange(len(word))
        return word[:char_index] + word[char_index + 1:]

    def __misspelling(self,word):
        print('Word: ', word)
        spell = SpellChecker()
        ret_word =''
        if word.lower() in spell:
            suggestions = list(spell.candidates(word.lower()))
            print(suggestions)
            if len(suggestions) > 0:
                new_word = choice(suggestions)
                print('New word: ', new_word)
                if fuzz.ratio(word.lower(), new_word) < 75:
                    print('AQUI NUNCA ENTRA')
                    ret_word = new_word

        print('Ret_word: ', ret_word)
        return ret_word

    def __similar_character(self,word):
        ret_word = ''
        char_index = randrange(len(word))
        similar_chars = {'a': 'e', 'e': 'a', 'i': 'l', 'l': 'i', 'o': 'u', 'u': 'o', 'a': '@', '0': '@', 'm':'n', 'n':'m',
                         'b':'v', 's':'z', 'v': 'b', 'z':'s'}
        if word[char_index].lower() in similar_chars:
            new_char = similar_chars[word[char_index].lower()]
            ret_word = word[:char_index] + new_char + word[char_index + 1:]
        return ret_word
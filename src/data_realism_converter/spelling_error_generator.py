from random import randrange
from random import choice
from spellchecker import SpellChecker
from fuzzywuzzy import fuzz


class SpellingErrorGenerator:


    def generate_spelling_errors(self,text):

        words = text.split()
        for i in range(len(words)):
            word = words[i]
            apply_value = randrange(100)
            if apply_value > 65:
                rand = randrange(100)
                if rand < 25:
                    # Duplicate character
                    words[i] =self.__duplicate_character(word)
                elif rand < 50:
                    # Omit character
                    words[i] = self.__omit_character(word)
                elif rand < 75:
                    # Misspelling
                    words[i] = self.__misspelling(word)
                else:
                    # Replace similar character
                    words[i] = self.__similar_character(word)

        return ' '.join(words)

    def __duplicate_character(self,word):
        char_index = randrange(len(word))
        return word[:char_index] + word[char_index] + word[char_index:]

    def __omit_character(self,word):
        char_index = randrange(len(word))
        return word[:char_index] + word[char_index + 1:]

    def __misspelling(self,word):
        spell = SpellChecker()
        ret_word =''
        if word.lower() in spell:
            suggestions = list(spell.candidates(word.lower()))
            if len(suggestions) > 0:
                new_word = choice(suggestions)
                if fuzz.ratio(word.lower(), new_word) < 75:
                    ret_word = new_word
        return ret_word

    def __similar_character(self,word):
        ret_word = ''
        char_index = randrange(len(word))
        similar_chars = {'a': 'e', 'e': 'a', 'i': 'l', 'l': 'i', 'o': 'u', 'u': 'o', 'a': '@', '0': '@'}
        if word[char_index].lower() in similar_chars:
            new_char = similar_chars[word[char_index].lower()]
            ret_word = word[:char_index] + new_char + word[char_index + 1:]
        return ret_word
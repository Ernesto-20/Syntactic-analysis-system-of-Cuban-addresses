import numpy as np

from src.structured_direction.classified_address import ClassifiedAddress


class Decoder:

    def __init__(self, id_to_cat: dict, cleaner_method):
        self.cat_to_id = {v: k for k, v in id_to_cat.items()}
        self.cleaner_method = cleaner_method

    def decoder_to_classified_address(self, matrix_probability, text_address_list):
        list_address_classified = []
        index_address = 0
        for raw_address in matrix_probability:
            components = {value: [] for key, value in self.cat_to_id.items()}

            pre_presses_text = self.cleaner_method(text_address_list[index_address])
            words = str(pre_presses_text.numpy().decode('utf-8')).split()

            for i in range(len(words)):  # Lista de probabilidades
                index_tag = list(raw_address[i]).index(max(list(raw_address[i])))
                components[index_tag] += [words[i]]

            principal_street = None
            first_side_street = None
            second_side_street = None
            building = None
            apartment = None
            locality = None
            municipality = None
            province = None
            reserve_word = None

            for cat in self.cat_to_id:
                if cat == 'principal_street':
                    principal_street = components[self.cat_to_id[cat]]
                elif cat == 'first_side_street':
                    first_side_street = components[self.cat_to_id[cat]]
                elif cat == 'second_side_street':
                    second_side_street = components[self.cat_to_id[cat]]
                elif cat == 'building':
                    building = components[self.cat_to_id[cat]]
                elif cat == 'apartment':
                    apartment = components[self.cat_to_id[cat]]
                elif cat == 'locality':
                    locality = components[self.cat_to_id[cat]]
                elif cat == 'municipality':
                    municipality = components[self.cat_to_id[cat]]
                elif cat == 'province':
                    province = components[self.cat_to_id[cat]]
                elif cat == 'rw':
                    reserve_word = components[self.cat_to_id[cat]]

            list_address_classified.append(
                ClassifiedAddress(principal_street=principal_street, first_side_street=first_side_street, second_side_street=second_side_street,
                                  locality=locality, municipality=municipality, province=province,
                                  building=building, apartment=apartment, reserve_word=reserve_word))
            index_address += 1

        return list_address_classified
from src.parser.tools.address_scheme_two import AddressSchemeTwo
from src.parser.tools.address_scheme_three import AddressSchemeThree
from src.parser.tools.address_scheme_one import AddressSchemeOne


class Decoder:

    def __init__(self, id_to_cat: dict, cleaner_method):
        self.cat_to_id = {v: k for k, v in id_to_cat.items()}
        self.cleaner_method = cleaner_method

    def decode_to_scheme_one(self, matrix_probability, text_address_list):
        list_address_classified = []
        index_address = 0
        for raw_address in matrix_probability:
            components = {value: [] for key, value in self.cat_to_id.items()}

            pre_presses_text = self.cleaner_method(text_address_list[index_address])
            words = str(pre_presses_text.numpy().decode('utf-8')).split()

            for i in range(len(words)):  # Lista de probabilidades
                index_tag = list(raw_address[i]).index(max(list(raw_address[i])))
                components[index_tag] += [words[i]]

            principal_street = components[self.cat_to_id['principal_street']]
            first_side_street = components[self.cat_to_id['first_side_street']]
            second_side_street = components[self.cat_to_id['second_side_street']]
            building = components[self.cat_to_id['building']]
            apartment = components[self.cat_to_id['apartment']]
            locality = components[self.cat_to_id['locality']]
            municipality = components[self.cat_to_id['municipality']]
            province = components[self.cat_to_id['province']]
            reserve_word = components[self.cat_to_id['rw']]
            padding = components[self.cat_to_id['padding']]

            list_address_classified.append(
                AddressSchemeOne(principal_street=principal_street, first_side_street=first_side_street,
                                 second_side_street=second_side_street,
                                 locality=locality, municipality=municipality, province=province,
                                 building=building, apartment=apartment, reserve_word=reserve_word,
                                 padding=padding))
            index_address += 1

        return list_address_classified

    def decode_to_scheme_one_v2(self, matrix_probability, text_address_list):
        list_address_classified = []
        index_address = 0
        for raw_address in matrix_probability:
            components = {value: [] for key, value in self.cat_to_id.items()}

            pre_presses_text = self.cleaner_method(text_address_list[index_address])
            words = str(pre_presses_text.numpy().decode('utf-8')).split()
            print(text_address_list[index_address])
            for i in range(len(words)):  # Lista de probabilidades
                index_tag = list(raw_address[i]).index(max(list(raw_address[i])))
                if raw_address[i][index_tag] > 0.5:
                    components[index_tag] += [words[i]]
                else:
                    print('*****************************************************************************************')
                    print('No es estoy seguro concho e tumadre')
                    print('palabra: ', words[i])

            principal_street = components[self.cat_to_id['principal_street']]
            first_side_street = components[self.cat_to_id['first_side_street']]
            second_side_street = components[self.cat_to_id['second_side_street']]
            building = components[self.cat_to_id['building']]
            apartment = components[self.cat_to_id['apartment']]
            locality = components[self.cat_to_id['locality']]
            municipality = components[self.cat_to_id['municipality']]
            province = components[self.cat_to_id['province']]
            reserve_word = components[self.cat_to_id['rw']]
            padding = components[self.cat_to_id['padding']]

            list_address_classified.append(
                AddressSchemeOne(principal_street=principal_street, first_side_street=first_side_street,
                                 second_side_street=second_side_street,
                                 locality=locality, municipality=municipality, province=province,
                                 building=building, apartment=apartment, reserve_word=reserve_word,
                                 padding=padding))
            index_address += 1

        return list_address_classified
    def decode_to_scheme_two(self, matrix_probability, text_address_list):
        list_address_classified = []

        for raw_address, text_address in zip(matrix_probability, text_address_list):
            components = {value: [] for key, value in self.cat_to_id.items()}

            try:
                pre_processed_text = self.cleaner_method(text_address)
                words = pre_processed_text.numpy().decode('utf-8').split()
            except (AttributeError, UnicodeDecodeError) as e:
                print(f"Error while preprocessing text address: {e}")
                continue

            component_tags = []

            for raw_prob in raw_address:
                max_probability = max(raw_prob)
                prob_list = list(raw_prob)
                index_tag = prob_list.index(max_probability)
                component_tags.append(index_tag)

            print("Length of words:", len(words))
            print("Length of component_tags:", len(component_tags))

            for i, index_tag in enumerate(component_tags):

                if i >= len(words):
                    break
                components[index_tag].append(words[i])

            building = components.get(self.cat_to_id.get('building'), None)
            apartment = components.get(self.cat_to_id.get('apartment'), None)
            locality = components.get(self.cat_to_id.get('locality'), None)
            municipality = components.get(self.cat_to_id.get('municipality'), None)
            province = components.get(self.cat_to_id.get('province'), None)
            reserve_word = components.get(self.cat_to_id.get('rw'), None)

            try:
                list_address_classified.append(
                    AddressSchemeTwo(locality, municipality, province, building, apartment, reserve_word)
                )
            except TypeError as e:
                print(f"Error while creating ClassifiedAddressTwo object: {e}")
                continue

        return list_address_classified

    def decode_to_scheme_three(self, matrix_probability, text_address_list):
        list_address_classified = []

        for raw_address, text_address in zip(matrix_probability, text_address_list):
            components = {value: [] for key, value in self.cat_to_id.items()}

            try:
                pre_processed_text = self.cleaner_method(text_address)
                words = pre_processed_text.numpy().decode('utf-8').split()
            except (AttributeError, UnicodeDecodeError) as e:
                print(f"Error while preprocessing text address: {e}")
                continue

            component_tags = []

            for raw_prob in raw_address:
                max_probability = max(raw_prob)
                prob_list = list(raw_prob)
                index_tag = prob_list.index(max_probability)
                component_tags.append(index_tag)

            print("Length of words:", len(words))
            print("Length of component_tags:", len(component_tags))

            for i, index_tag in enumerate(component_tags):

                if i >= len(words):
                    break
                components[index_tag].append(words[i])

            principal_street = components.get(self.cat_to_id.get('principal_street'), None)
            distance = components.get(self.cat_to_id.get('distance'), None)
            interesting_place = components.get(self.cat_to_id.get('interesting_place'), None)
            locality = components.get(self.cat_to_id.get('locality'), None)
            municipality = components.get(self.cat_to_id.get('municipality'), None)
            province = components.get(self.cat_to_id.get('province'), None)
            reserve_word = components.get(self.cat_to_id.get('rw'), None)

            try:
                list_address_classified.append(
                    AddressSchemeThree(principal_street, distance, interesting_place, locality,
                                       municipality, province, reserve_word)
                )
            except TypeError as e:
                print(f"Error while creating ClassifiedAddressThree object: {e}")
                continue

        return list_address_classified


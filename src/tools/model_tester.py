import numpy as np
from pandas import DataFrame

from parser.tools.address_scheme_three import AddressSchemeThree
from parser.tools.address_scheme_two import AddressSchemeTwo


def import_address_list_two(df: DataFrame):
    address_list = []
    for index, row in df.iterrows():
        reserve_word = row['rw']
        locality = row['locality']
        municipality = row['municipality']
        province = row['province']
        building = row['building']
        apartment = row['apartment']

        print(apartment)

        if building is np.nan:
            building = [' ']
        elif apartment is np.nan:
            apartment = [' ']
        elif locality is np.nan:
            locality = [' ']
        elif municipality is np.nan:
            municipality = [' ']
        elif province is np.nan:
            province = [' ']
        elif reserve_word is np.nan:
            reserve_word = [' ']

        address = AddressSchemeTwo(
            locality=locality,
            municipality=municipality,
            province=province,
            building=building,
            apartment=apartment,
            reserve_word=reserve_word
        )
        address_list.append(address)
    return address_list


def import_address_list_three(df: DataFrame):
    address_list = []
    for index, row in df.iterrows():
        reserve_word = row['rw']
        locality = row['locality']
        municipality = row['municipality']
        province = row['province']
        principal_street = row['principal_street']
        distance = row['distance']
        interesting_place = row['interesting_place']

        if principal_street is np.nan:
            principal_street = [' ']
        elif distance is np.nan:
            distance = [' ']
        elif interesting_place is np.nan:
            interesting_place = [' ']
        elif locality is np.nan:
            locality = [' ']
        elif municipality is np.nan:
            municipality = [' ']
        elif province is np.nan:
            province = [' ']
        elif reserve_word is np.nan:
            reserve_word = [' ']

        address = AddressSchemeThree(
            principal_street=principal_street,
            distance=distance,
            interesting_place=interesting_place,
            locality=locality,
            municipality=municipality,
            province=province,
            reserve_word=reserve_word
        )
        address_list.append(address)
    return address_list


def calculate_results_two(y_predict: list, y_real: list):
    print('Accurracy')
    matches = 0
    no_matches = 0

    temp_3 = 0  # para ver los resultados por direccion
    count_correct_parsing = 0
    for i in range(len(y_predict)):

        print("locality")
        print(f'y_predict: {y_predict[i].locality[:]} , y_real: {y_real[i].locality[:]} ')
        temp = number_of_matches(y_predict[i].locality[:], y_real[i].locality[:])
        matches += temp
        no_matches += len(y_predict[i].locality) - temp

        print("municipality")
        print(f'y_predict: {y_predict[i].municipality[:]} , y_real: {y_real[i].municipality[:]} ')
        temp = number_of_matches(y_predict[i].municipality[:], y_real[i].municipality[:])
        matches += temp
        no_matches += len(y_predict[i].municipality) - temp

        print("province")
        print(f'y_predict: {y_predict[i].province[:]} , y_real: {y_real[i].province[:]} ')
        temp = number_of_matches(y_predict[i].province[:], y_real[i].province[:])
        matches += temp
        no_matches += len(y_predict[i].province) - temp

        print("building")
        print(f'y_predict: {y_predict[i].building[:]} , y_real: {y_real[i].building[:]} ')
        temp = number_of_matches(y_predict[i].building[:], y_real[i].building[:])
        matches += temp
        no_matches += len(y_predict[i].building) - temp

        print("apartment")
        print(f'y_predict: {y_predict[i].apartment[:]} , y_real: {y_real[i].apartment[:]} ')
        temp = number_of_matches(y_predict[i].apartment[:], y_real[i].apartment[:])
        matches += temp
        no_matches += len(y_predict[i].apartment) - temp

        print("reserve_word")
        print(f'y_predict: {y_predict[i].reserve_word[:]} , y_real: {y_real[i].reserve_word[:]} ')
        temp = number_of_matches(y_predict[i].reserve_word[:], y_real[i].reserve_word[:])
        matches += temp
        no_matches += len(y_predict[i].reserve_word) - temp

        temp_3 = no_matches - temp_3
        if temp_3 > 0:
            print('address #', (i + 1), ' --- ( ', temp_3, ' )')
        if temp_3 == 0:
            count_correct_parsing += 1

        temp_3 = no_matches

    VP = matches
    FN = no_matches
    FP = FN
    VN = matches + no_matches  # Aqui estoy contando el padding tag
    print('Total number of errrors: ', FN)
    result = {'accuracy': (VP + VN) / (VP + FN + FP + VN),
              'precision': VP / (VP + FP),
              'recall': VP / (VP + FN),
              'amount_parsing_correct_address': count_correct_parsing
              }

    return result


def calculate_results_three(y_predict: list, y_real: list):
    print('Accurracy')
    matches = 0
    no_matches = 0

    temp_3 = 0  # para ver los resultados por direccion
    count_correct_parsing = 0
    for i in range(len(y_predict)):

        print("locality")
        print(f'y_predict: {y_predict[i].locality[:]} , y_real: {y_real[i].locality[:]} ')
        temp = number_of_matches(y_predict[i].locality[:], y_real[i].locality[:])
        matches += temp
        no_matches += len(y_predict[i].locality) - temp

        print("municipality")
        print(f'y_predict: {y_predict[i].municipality[:]} , y_real: {y_real[i].municipality[:]} ')
        temp = number_of_matches(y_predict[i].municipality[:], y_real[i].municipality[:])
        matches += temp
        no_matches += len(y_predict[i].municipality) - temp

        print("province")
        print(f'y_predict: {y_predict[i].province[:]} , y_real: {y_real[i].province[:]} ')
        temp = number_of_matches(y_predict[i].province[:], y_real[i].province[:])
        matches += temp
        no_matches += len(y_predict[i].province) - temp

        print("principal_street")
        print(f'y_predict: {y_predict[i].principal_street[:]} , y_real: {y_real[i].principal_street[:]} ')
        temp = number_of_matches(y_predict[i].principal_street[:], y_real[i].principal_street[:])
        matches += temp
        no_matches += len(y_predict[i].principal_street) - temp

        print("distance")
        print(f'y_predict: {y_predict[i].distance[:]} , y_real: {y_real[i].distance[:]} ')
        temp = number_of_matches(y_predict[i].distance[:], y_real[i].distance[:])
        matches += temp
        no_matches += len(y_predict[i].distance) - temp

        print("interesting_place")
        print(f'y_predict: {y_predict[i].interesting_place[:]} , y_real: {y_real[i].interesting_place[:]} ')
        temp = number_of_matches(y_predict[i].interesting_place[:], y_real[i].interesting_place[:])
        matches += temp
        no_matches += len(y_predict[i].interesting_place) - temp

        print("reserve_word")
        print(f'y_predict: {y_predict[i].reserve_word[:]} , y_real: {y_real[i].reserve_word[:]} ')
        temp = number_of_matches(y_predict[i].reserve_word[:], y_real[i].reserve_word[:])
        matches += temp
        no_matches += len(y_predict[i].reserve_word) - temp

        temp_3 = no_matches - temp_3
        if temp_3 > 0:
            print('address #', (i + 1), ' --- ( ', temp_3, ' )')
        if temp_3 == 0:
            count_correct_parsing += 1

        temp_3 = no_matches

    VP = matches
    FN = no_matches
    FP = FN
    VN = matches + no_matches  # Aqui estoy contando el padding tag
    print('Total number of errors: ', FN)
    result = {'accuracy': (VP + VN) / (VP + FN + FP + VN),
              'precision': VP / (VP + FP),
              'recall': VP / (VP + FN),
              'amount_parsing_correct_address': count_correct_parsing
              }

    return result


def number_of_matches(list_a: list, list_b: list):
    number = 0
    for element_a in list_a:
        if element_a in list_b:
            number += 1
            list_b.remove(element_a) if isinstance(list_b, list) else list_b.replace(element_a, '')

    return number

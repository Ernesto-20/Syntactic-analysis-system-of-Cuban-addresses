from src.structured_direction.classified_address_one import ClassifiedAddressOne


def calculate_results(y_predict: list, y_real: list):
    print('Accurracy')
    matches = 0
    no_matches = 0

    temp_3 = 0 # para ver los resultados por direccion
    count_correct_parsing = 0
    for i in range(len(y_predict)):
        temp = number_of_matches(y_predict[i].principal_street[:], y_real[i].principal_street[:])
        matches += temp
        no_matches += len(y_predict[i].principal_street) - temp

        temp = number_of_matches(y_predict[i].first_side_street[:], y_real[i].first_side_street[:])
        matches += temp
        no_matches += len(y_predict[i].first_side_street) - temp

        temp = number_of_matches(y_predict[i].second_side_street[:], y_real[i].second_side_street[:])
        matches += temp
        no_matches += len(y_predict[i].second_side_street) - temp

        temp = number_of_matches(y_predict[i].locality[:], y_real[i].locality[:])
        matches += temp
        no_matches += len(y_predict[i].locality) - temp

        temp = number_of_matches(y_predict[i].municipality[:], y_real[i].municipality[:])
        matches += temp
        no_matches += len(y_predict[i].municipality) - temp

        temp = number_of_matches(y_predict[i].province[:], y_real[i].province[:])
        matches += temp
        no_matches += len(y_predict[i].province) - temp

        temp = number_of_matches(y_predict[i].building[:], y_real[i].building[:])
        matches += temp
        no_matches += len(y_predict[i].building) - temp

        temp = number_of_matches(y_predict[i].apartment[:], y_real[i].apartment[:])
        matches += temp
        no_matches += len(y_predict[i].apartment) - temp

        temp = number_of_matches(y_predict[i].reserve_word[:], y_real[i].reserve_word[:])
        matches += temp
        no_matches += len(y_predict[i].reserve_word) - temp

        temp_3 = no_matches - temp_3
        if temp_3 > 0:
            print('address #', (i+1), ' --- ( ', temp_3, ' )')
        if temp_3 == 0:
            count_correct_parsing += 1

        temp_3 = no_matches

    VP = matches
    FN = no_matches
    FP = FN
    VN = matches*9+no_matches*8 # Aqui estoy contando el padding tag
    print('Total number of errrors: ', FN)
    result = {'accuracy': (VP+VN)/(VP+FN+FP+VN),
              'precision': VP/(VP+FP),
              'recall': VP/(VP+FN),
              'amount_parsing_correct_address': count_correct_parsing
              }

    return result

# others methods
def number_of_matches(list_a: list, list_b:list):
    number = 0
    for element_a in list_a:
        if element_a in list_b:
            number += 1
            list_b.remove(element_a)

    return number




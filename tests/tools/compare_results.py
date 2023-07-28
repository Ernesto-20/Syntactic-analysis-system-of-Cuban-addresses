from src.structured_direction.classified_address_one import ClassifiedAddressOne


def accurracy(y_predict: list, y_real: list):
    print('Accurracy')
    matches = 0
    no_matches = 0

    temp_2 = 0 # para ver los resultados por direccion
    temp_3 = 0 # para ver los resultados por direccion
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

        temp_2 = matches - temp_2
        temp_3 = no_matches - temp_3
        print('address #',(i+1))
        print('VP: ', temp_2)
        print('FN: ', temp_3)
        print('FP: ', temp_3)
        print('VN:', temp_2*8+temp_3*7)

        temp_2 = matches
        temp_3 = no_matches

    VP = matches
    FN = no_matches
    FP = FN
    VN = matches*8+no_matches*7

    return (VP+VN)/(VP+FN+FP+VN)





def precision(y_predict: list, y_real: list):
    print('Precision')

def recall(y_predict: list, y_real: list):
    print('recall')

def amount_correct_address_parser(y_predict: list, y_real: list):
    print('Amount correct address parser')


# others methods
def number_of_matches(list_a: list, list_b:list):
    number = 0
    for element_a in list_a:
        if element_a in list_b:
            number += 1
            list_b.remove(element_a)

    return number




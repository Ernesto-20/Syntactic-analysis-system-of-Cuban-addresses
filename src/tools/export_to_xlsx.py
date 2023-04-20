from src.structured_direction.classified_address import ClassifiedAddress
import pandas as pd
from pandas import DataFrame


def export_to_xlsx(list_address: list, name_file='Results'):
    principal_street_list = []
    first_side_street_list = []
    second_side_street_list = []
    locality_list = []
    municipality_list = []
    province_list = []
    buildings_list = []
    apartment_list = []
    reserve_words_list = []

    for address in list_address:
        principal_street_list.append(' '.join(address.principal_street))
        first_side_street_list.append(' '.join(address.first_side_street))
        second_side_street_list.append(' '.join(address.second_side_street))
        locality_list.append(' '.join(address.locality))
        municipality_list.append(' '.join(address.municipality))
        province_list.append(' '.join(address.province))
        buildings_list.append(' '.join(address.building))
        apartment_list.append(' '.join(address.apartment))
        reserve_words_list.append(' '.join(address.reserve_word))

    df = DataFrame({
        'Principal Street': principal_street_list,
        'First Side Street': first_side_street_list,
        'Second Side Street': second_side_street_list,
        'Building': buildings_list,
        'Apartment': apartment_list,
        'Locality': locality_list,
        'Municipality': municipality_list,
        'Province': province_list,
        'Reserved Word': reserve_words_list,
    })

    writer = pd.ExcelWriter(name_file+'.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Results')
    writer.save()

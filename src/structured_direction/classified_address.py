

class ClassifiedAddress:

    def __init__(self, principal_street, first_side_street, second_side_street, locality, municipality,
                 province, building, apartment, reserve_word):
        self.principal_street = principal_street
        self.first_side_street = first_side_street
        self.second_side_street = second_side_street
        self.locality = locality
        self.municipality = municipality
        self.province = province
        self.building = building
        self.apartment = apartment
        self.reserve_word = reserve_word

    def __str__(self):
        address = 'Calle principal: ' + ' '.join(self.principal_street) + '\n' \
        'Primera calle lateral : ' + ' '.join(self.first_side_street) + '\n' \
        'Segunda calle lateral: ' + ' '.join(self.second_side_street) + '\n' \
        'Edificio: ' + ' '.join(self.building) + '\n' \
        'Apartamento: ' + ' '.join(self.apartment) + '\n'\
        'Localidad: ' + ' '.join(self.locality) + '\n' \
        'Municipio: ' + ' '.join(self.municipality) + '\n' \
        'Provincie: ' + ' '.join(self.province) + '\n' \
        'Palabras reservadas: ' + ' '.join(self.reserve_word) + '\n'

        return address



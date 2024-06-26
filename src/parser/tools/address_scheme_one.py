class AddressSchemeOne:

    def __init__(self, principal_street:list, first_side_street:list, second_side_street:list, locality:list, municipality:list,
                 province:list, building:list, apartment:list, reserve_word:list, padding=[]):
        self.principal_street = principal_street
        self.first_side_street = first_side_street
        self.second_side_street = second_side_street
        self.locality = locality
        self.municipality = municipality
        self.province = province
        self.building = building
        self.apartment = apartment
        self.reserve_word = reserve_word
        self.padding = padding

    def __str__(self):
        address = 'Calle principal: ' + ' '.join(self.principal_street) + '\n' \
        'Primera calle lateral : ' + ' '.join(self.first_side_street) + '\n' \
        'Segunda calle lateral: ' + ' '.join(self.second_side_street) + '\n' \
        'Edificio: ' + ' '.join(self.building) + '\n' \
        'Apartamento: ' + ' '.join(self.apartment) + '\n'\
        'Localidad: ' + ' '.join(self.locality) + '\n' \
        'Municipio: ' + ' '.join(self.municipality) + '\n' \
        'Provincia: ' + ' '.join(self.province) + '\n' \
        'Palabras reservadas: ' + ' '.join(self.reserve_word) + '\n'
        'Padding: ' + ' '.join(self.padding) + '\n'

        return address

    def __eq__(self, other):
        if not isinstance(other, AddressSchemeOne): return False
        if not set(self.principal_street) == set(other.principal_street): return False
        if not set(self.first_side_street) == set(other.first_side_street): return False
        if not set(self.second_side_street) == set(other.second_side_street): return False
        if not set(self.building) == set(other.building): return False
        if not set(self.apartment) == set(other.apartment): return False
        if not set(self.locality) == set(other.locality): return False
        if not set(self.municipality) == set(other.municipality): return False
        if not set(self.province) == set(other.province): return False
        if not set(self.reserve_word) == set(other.reserve_word): return False
        if not set(self.padding) == set(other.padding): return False

        return True


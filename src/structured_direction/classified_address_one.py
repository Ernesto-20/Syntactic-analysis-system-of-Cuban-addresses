

class ClassifiedAddressOne:

    def __init__(self, principal_street:list, first_side_street:list, second_side_street:list, locality:list, municipality:list,
                 province:list, building:list, apartment:list, reserve_word:list):
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
        'Provincia: ' + ' '.join(self.province) + '\n' \
        'Palabras reservadas: ' + ' '.join(self.reserve_word) + '\n'

        return address

    def __eq__(self, other):
        if not isinstance(other, ClassifiedAddressOne): return False
        if not set(self.principal_street) == set(other.principal_street): return False
        if not set(self.first_side_street) == set(other.first_side_street): return False
        if not set(self.second_side_street) == set(other.second_side_street): return False
        if not set(self.building) == set(other.building): return False
        if not set(self.apartment) == set(other.apartment): return False
        if not set(self.locality) == set(other.locality): return False
        if not set(self.municipality) == set(other.municipality): return False
        if not set(self.province) == set(other.province): return False
        if not set(self.reserve_word) == set(other.reserve_word): return False

        return True

    def __classified_address_two(self, locality, municipality,province, building, apartment, reserve_word):
        self.locality = locality
        self.municipality = municipality
        self.province = province
        self.building = building
        self.apartment = apartment
        self.reserve_word = reserve_word

    def __str__address_two(self):
        address_two = 'Edificio: ' + ' '.join(self.building) + '\n' \
        'Apartamento: ' + ' '.join(self.apartment) + '\n'\
        'Localidad: ' + ' '.join(self.locality) + '\n' \
        'Municipio: ' + ' '.join(self.municipality) + '\n' \
        'Provincia: ' + ' '.join(self.province) + '\n' \
        'Palabras reservadas: ' + ' '.join(self.reserve_word) + '\n'

        return address_two

    def __classified_address_three(self, principal_street, distance, interesting_place, locality,
                                   municipality, province, reserve_word):
        self.principal_street = principal_street
        self.distance = distance
        self.interesting_place = interesting_place
        self.locality = locality
        self.municipality = municipality
        self.province = province
        self.reserve_word = reserve_word

    def __str__adress_three(self):
        address_three ='Calle principal: ' + ' '.join(self.principal_street) + '\n' \
        'Distancia en km : ' + ' '.join(self.distance) + '\n' \
        'Lugar de interes: ' + ' '.join(self.interesting_place) + '\n' \
        'Localidad: ' + ' '.join(self.locality) + '\n' \
        'Municipio: ' + ' '.join(self.municipality) + '\n' \
        'Provincia: ' + ' '.join(self.province) + '\n' \
        'Palabras reservadas: ' + ' '.join(self.reserve_word) + '\n'

        return address_three

    def delegate_address_two(self,locality, municipality,province, building, apartment, reserve_word):
        return self.__classified_address_two(locality, municipality,province, building, apartment, reserve_word)

    def show_address_two(self):
        return self.__str__address_two()

    def delegate_address_three(self, principal_street, distance, interesting_place, locality,
                               municipality, province, reserve_word):
        return self.__classified_address_three(principal_street, distance, interesting_place, locality,
                                               municipality, province, reserve_word)

    def show_address_three(self):
        return self.__str__address_three()
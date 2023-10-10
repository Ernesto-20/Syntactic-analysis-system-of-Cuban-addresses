
class AddressSchemeThree:

    def __init__(self, principal_street, distance, interesting_place, locality,
                                   municipality, province, reserve_word):
        self.principal_street = principal_street
        self.distance = distance
        self.interesting_place = interesting_place
        self.locality = locality
        self.municipality = municipality
        self.province = province
        self.reserve_word = reserve_word

    def __str__(self):
        address_three = 'Calle principal: ' + ' '.join(self.principal_street) + '\n' \
            'Distancia en km : ' + ' '.join(self.distance) + '\n' \
            'Lugar de interes: ' + ' '.join(self.interesting_place) + '\n' \
            'Localidad: ' + ' '.join(self.locality) + '\n' \
            'Municipio: ' + ' '.join(self.municipality) + '\n' \
            'Provincia: ' + ' '.join(self.province) + '\n' \
            'Palabras reservadas: ' + ' '.join(self.reserve_word) + '\n'

        return address_three


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
        address_three = 'Calle principal: ' + f'{self.principal_street}' + '\n' \
            'Distancia en km : ' + f'{self.distance}' + '\n' \
            'Lugar de interes: ' + f'{self.interesting_place}' + '\n' \
            'Localidad: ' + f'{self.locality}' + '\n' \
            'Municipio: ' + f'{self.municipality}' + '\n' \
            'Provincia: ' + f'{self.province}' + '\n' \
            'Palabras reservadas: ' + f'{self.reserve_word}' + '\n'

        return address_three
